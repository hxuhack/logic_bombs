import os
import subprocess
import json
import re
import shutil
import template_parser as tpp
import script_runner as sr
import argparse

from template_parser import TemplateParser
from termcolor import colored

class Compile:
    sign_pattern = re.compile(r'#([a-zA-Z0-9_ ]+)$')

    @staticmethod
    def parse_dependencies(cmd: str, dependencies: dict, root='.', iters_on=None, ands_on=None):
        if not iters_on:
            iters_on, ands_on = Compile.split_loop(cmd)

        replacment = {key: [] for key in iters_on}
        patterns = {key: [re.compile(os.path.join(root, rep)) for rep in dependencies[key]]
                    for key in iters_on}
        for root, dirs, files in os.walk(root):
            for file in files:
                path = os.path.join(root, file)
                for key, pt_list in patterns.items():
                    for pt in pt_list:
                        if pt.search(path) is not None:
                            replacment[key].append(path)

        return replacment

    @staticmethod
    def split_loop(cmd: str):
        iter_pt =  re.compile(r'\{\!([^}\n]*)\}')
        fn_pt = re.compile(r'\{\&([^}\n]*)\}')

        iters_on = iter_pt.findall(cmd)
        iters_on = list(map(str.strip, iters_on))

        ands_on = fn_pt.findall(cmd)
        ands_on = list(map(str.strip, ands_on))
        ands_on = list(filter(lambda x: x not in iters_on, ands_on))
        return iters_on, ands_on

    @staticmethod
    def iteration_cmd_generator(cmd: str, iter_on, replacment):
        try:
            var = next(iter_on)
        except StopIteration:
            return [cmd, ]

        cmd_tps = []
        for value in replacment[var]:
            tmp = cmd.replace('{!%s}' % var, value)
            vp = os.path.split(value)[-1].split('.')
            tmp = tmp.replace('{&%s}' % var, vp[-2] if len(vp) > 1 else vp[0])
            cmd_tps.extend(Compile.iteration_cmd_generator(tmp, iter_on, replacment))
        return cmd_tps

    @staticmethod
    def run_cmd(cmd: str, PIPE_IN=None, echo=True):
        print(cmd)
        if PIPE_IN:
            p = subprocess.Popen(cmd.split(' '), stdin=subprocess.PIPE)
            p.communicate(PIPE_IN)
        else:
            p = subprocess.Popen(cmd.split(' '))
        rt_value = p.wait()
        return rt_value

    @staticmethod
    def get_cmd_templates(cmd: str, iter_params, root='.', iters_on=None, ands_on=None):
        signs = Compile.sign_pattern.findall(cmd)
        mode = 'SINGLE'
        if len(signs) > 1:
            raise SyntaxError(cmd)
        elif len(signs) == 1:
            signs = list(map(str.lower, signs[0].split(' ')))
            if 'batch' in signs:
                mode = 'BATCH'
            cmd = Compile.sign_pattern.sub('', cmd).strip()

        if not iters_on:
            iters_on, ands_on = Compile.split_loop(cmd)

        if mode == 'SINGLE':
            cmd_templates = Compile.iteration_cmd_generator(cmd, iter(iters_on), iter_params)
        else:
            for iter_on in iters_on:
                cmd = cmd.replace('{!%s}' % iter_on, ' '.join(iter_params[iter_on]))
            cmd_templates = [cmd, ]

        return cmd_templates, signs

    @staticmethod
    def replace_normal_and(cmd_templates, dependencies, ands_on):
        for and_on in ands_on:
            value = dependencies[and_on]
            vp = os.path.split(value)[-1].split('.')
            cmd_templates = list(map(lambda x: x.replace('{&%s}' % and_on,
                                vp[-2] if len(vp) > 1 else vp[0]), cmd_templates))

        return cmd_templates

    @staticmethod
    def process_cmd(cmd: str, dependencies, root='.'):
        iters_on, ands_on = Compile.split_loop(cmd)
        iter_params = Compile.parse_dependencies(cmd, dependencies, root, iters_on)
        cmd_templates, signs = Compile.get_cmd_templates(cmd, iter_params, root)
        cmd_templates = Compile.replace_normal_and(cmd_templates, dependencies, ands_on)
        cmd_list = list(map(lambda x: x.format(**dependencies), cmd_templates))

        return cmd_list, signs


class ConfigParser:
    def __init__(self, json_path, root='.'):
        self.config = json.load(open(json_path))
        self.root = os.path.abspath(root)
        self.general = self.config.get('general')
        self.__load_config__()

    def __load_config__(self):
        pass

    def combine(self, file_path: str, tp_path: str, func_name='logic_bomb'):
        def params_list_parser(params):
            if len(params.strip()) == 0:
                return []
            else:
                params = params.split(',')
                params = list(map(str.strip, params))
                res = []
                var_pattern = re.compile(r'([a-zA-Z_][a-zA-Z0-9_*]*|\*+)')
                for param in params:
                    tmp = var_pattern.findall(param)
                    if len(tmp) < 2:
                        raise SyntaxError(', '.join(params))
                    var_name = tmp[-1]
                    var_type = ' '.join(tmp[:-1])
                    var_type = re.sub(r'[ \t\n]*\*', '*', var_type)
                    res.append((var_type, var_name))
                return res

        func_pattern = re.compile(r'int[ \t\n]+%s\(([^)]*)\);*' % func_name)
        with open(file_path) as f:
            pg = f.read()
        finds = func_pattern.findall(pg)
        if len(finds) == 0:
            return None
        elif len(finds) > 1:
            raise SyntaxError(repr(finds) + '. Duplicated definition!')
        else:
            params = finds[0].strip()
            params_list = params_list_parser(params)
            # Generate definitions
            defs = []
            call_params = []
            for v_type, var in params_list:
                defs.append(' '.join([v_type, var]) + ';')
                call_params.append(var)
            params = dict(
                vars=call_params,
                params=', '.join(call_params),
                defs='\n'.join(defs)
            )
            res = TemplateParser.appender_parser(tp_path, params)
            res = '\n'.join([pg, res])
            return res

    def normal_compiler(self, prefix: str):
        config = self.config.get(prefix, None)
        if not config:
            return None
        cmds = config.get('cmd', None)
        dependencies = config.get('dependencies', None)
        if not cmds or not dependencies:
            return None

        mkdirs = config.get('mkdir', [])
        for mkdir in mkdirs:
            if not os.path.exists(mkdir):
                os.makedirs(mkdir)

        for cmd in cmds:
            dependencies['CC'] = self.general['CC']
            cmd_list, signs = Compile.process_cmd(cmd, dependencies, self.root)
            for gonna_run in cmd_list:
                Compile.run_cmd(gonna_run)

        rms = config.get('rm', [])
        for rm in rms:
            shutil.rmtree(rm)
        return True

    def pipe_compile(self, prefix: str, func_name='logic_bomb', echo=False):
        def params_list_parser(params):
            if len(params.strip()) == 0:
                return []
            else:
                params = params.split(',')
                params = list(map(str.strip, params))
                res = []
                var_pattern = re.compile(r'([a-zA-Z_][a-zA-Z0-9_*]*|\*+)')
                for param in params:
                    tmp = var_pattern.findall(param)
                    if len(tmp) < 2:
                        raise SyntaxError(', '.join(params))
                    var_name = tmp[-1]
                    var_type = ' '.join(tmp[:-1])
                    var_type = re.sub(r'[ \t\n]*\*', '*', var_type)
                    res.append((var_type, var_name))
                return res

        def combine(path, tp_path):
            func_pattern = re.compile(r'int[ \t\n]+%s\(([^)]*)\);*' % func_name)
            fp = path
            print('-----------------------------')
            print(fp)
            with open(fp) as f:
                content = f.read()
            finds = func_pattern.findall(content)
            if len(finds) > 1:
                raise SyntaxError(repr(finds) + '. Duplicated definition!')
            elif len(finds) == 0:
                return None
            else:
                params = finds[0].strip()
                params_list = params_list_parser(params)
                vars_list = [_[1] for _ in params_list]
                params = ', '.join(vars_list)
                params_list_with_length = []
                comments_pattern = re.compile(r'//(.*)\n[ \t]*' + r'int[ \t\n]+%s\(([^)]*)\);*' % func_name)
                cmts = comments_pattern.findall(content)
                cmt = cmts[0] if len(cmts) > 0 else ('{}', )
                cmt_dict = json.loads(cmt[0])
                for var_type, var_name in params_list:
                    length = cmt_dict.get(var_name, {}).get('length', 0)
                    params_list_with_length.append((var_type, var_name, length))

            init_vars = dict(vp=params_list_with_length, params=params)
            tp = tpp.TemplateParser(tp_path)
            sruner = sr.ScriptRunner(init_vars)
            res = sruner.run(tp.parse()[0])
            res = '\n'.join(res[1])
            res = tp.replace([res, ])
            if echo:
                print(res)
            res = '\n'.join([content, res])
            return res

        config = self.config.get(prefix, None)
        if not config:
            return None

        cmds = config.get('cmd', None)
        dependencies = config.get('dependencies', None)
        if not cmds or not dependencies:
            return None

        TP = dependencies.get('TEMPLATE', None)
        FNAME = dependencies.get('FILENAME', 'FILENAME')
        PATH = dependencies.get('PATH', None)
        if not TP or not PATH:
            print('here', 3)
            return None

        for mkdir in config.get('mkdir', []):
            if not os.path.exists(mkdir):
                os.makedirs(mkdir)

        excepts = config.get('exceptions', [])

        for root, dirs, files in os.walk(PATH):
            for file in files:
                path = os.path.join(root, file)
                flag = False
                for exct in excepts:
                    if path.startswith(exct):
                        flag = True
                        break
                if flag:
                    continue

                for cmd in cmds:
                    dependencies['CC'] = self.general['CC'] if not config.get('CC', False) else config.get('CC')
                    dependencies[FNAME] = path
                    cmd_list, signs = Compile.process_cmd(cmd, dependencies)
                    combined = combine(os.path.join(root, file), TP)
                    for gonna_run in cmd_list:
                        if combined is None:
                            continue
                        if 'pipe' in signs:
                            Compile.run_cmd(gonna_run, PIPE_IN=combined.encode('utf8'))

        for rm in config.get('rm', []):
            shutil.rmtree(rm)

        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all_code", help="compile all", action="store_true")
    parser.add_argument("-l", "--lib", help="compile lib", action="store_true")
    parser.add_argument("-s", "--src", help="compile src", action="store_true")
    parser.add_argument("-e", "--echo", help="echo main", action="store_true")
    args = parser.parse_args()

    all_code = args.all_code
    lib = args.lib
    src = args.src
    echo = args.echo

    c = ConfigParser('config/compile.json')

    if lib or all_code:
        c.normal_compiler('crypto_lib')
        c.normal_compiler('utils_lib')

    if src or all_code:
        c.pipe_compile('src', echo=echo)
        c.pipe_compile('src_cpp', echo=echo)
