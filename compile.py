import os
import subprocess
import json
import re
import shutil

from template_parser import TemplateParser


class Compile:
    @staticmethod
    def parse_dependencies(cmd: str, dependencies: dict, iters_on: list, root: str):
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
            p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE)
        rt_value = p.wait()
        return rt_value


class ConfigParser:
    def __init__(self, json_path, root='.'):
        self.config = json.load(open(json_path))
        self.root = os.path.abspath(root)
        self.__load_config__()
        self.sign_pattern = re.compile(r'#([a-zA-Z0-9_ ]+)')
        self.general = self.config.get('general')

    def __load_config__(self):
        pass

    def combine(self, file_path: str, tp_path: str, func_name='sym_checker'):
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
            print(res)
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
                os.mkdir(mkdir)

        for cmd in cmds:
            signs = self.sign_pattern.findall(cmd)
            mode = 'SINGLE'
            if len(signs) > 1:
                raise SyntaxError(cmd)
            elif len(signs) == 1:
                if signs[0].lower() == 'batch':
                    mode = 'BATCH'
                cmd = self.sign_pattern.sub('', cmd).strip()

            iters_on, ands_on = Compile.split_loop(cmd)
            iter_params = Compile.parse_dependencies(cmd, dependencies, iters_on, self.root)

            if mode == 'SINGLE':
                cmds_templates = Compile.iteration_cmd_generator(cmd, iter(iters_on), iter_params)
            else:
                for iter_on in iters_on:
                    cmd = cmd.replace('{!%s}' % iter_on, ' '.join(iter_params[iter_on]))
                cmds_templates = [cmd, ]

            dependencies['CC'] = self.general['CC']

            for and_on in ands_on:
                value = dependencies[and_on]
                vp = os.path.split(value)[-1].split('.')
                cmds_templates = list(map(lambda x: x.replace('{&%s}' % and_on,
                                          vp[-2] if len(vp) > 1 else vp[0]), cmds_templates))

            cmd_list = list(map(lambda x: x.format(**dependencies), cmds_templates))

            for gonna_run in cmd_list:
                Compile.run_cmd(gonna_run)

        rms = config.get('rm', [])
        for rm in rms:
            shutil.rmtree(rm)
        return True

if __name__ == '__main__':
    c = ConfigParser('config.json')
    c.normal_compiler('crypto_lib')
    c.normal_compiler('utils_lib')
