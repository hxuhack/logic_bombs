import subprocess
import shutil
import json
import re
import os


class MakeMakefile:
    sign_pattern = re.compile(r'#([\w\d ]+)(\{[\w\d ]+\})?$')
    var_pattern = re.compile(r'\{([^}]+)\}')

    @staticmethod
    def __fetch_config__(config, prefix, key, exception_name='exceptions'. global_name='global'):
        pref_config = config[prefix]
        global_config = config.get(global_name, {})
        excpt_config = pref_config.get(exception_name, {})
        if key in excpt_config:
            pass
        elif key in pref_config:
            return pref_config[key]
        elif key in global_config:
            return global_config[key]
        else:
            raise KeyError

    @staticmethod
    def __var_parser__(var, value, root_path):
        var = var.strip()
        iters_on = var[0] == '!'
        get_name = var[0] == '&'
        joined = var[0] == '@'
        res = []
        pattern = re.compile(value)
        for root, dirs, files in os.walk(root_path):
            for file in files:
                fp = os.abspath(os.path.join(root, file))
                if pattern.search(fp) is not None:
                    res.append(fp)

        def process(fp):
            folder, file = os.path.split(fp)
            file = file if len(file.split('.')) == 1 else file.split('.')[:-1]
            return os.path.join(folder, file)

        if get_name:
            res = list(map(process, res))
        elif joined:
            res = ' '.join(res)

        return res, iters_on

    @staticmethod
    def __parse__(stm, dependencies):
        n_vars = []
        iter_vars = []
        variables = {}
        for var in var_pattern.finditer(stm):
            v_name = var.group().strip()
            if v_name not in variables:
                variables[v_name] = [var.group(), ]
            else:
                variables[v_name].append(var.group())
            if v_name[0] == '!':
                iter_vars.append(v_name)

        def parse_iters_on(stm, iters_on)

        results = []




    @classmethod
    def make(cls, config_path, root_path='.'):
        with open(config_path) as f:
            cls.config = json.load(f)

    @classmethod
    def run(cls, cmds):
        pass
