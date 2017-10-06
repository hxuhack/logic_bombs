import os
import template_parser as tpp
import script_runner as sr

CORRECT = 0
PARTIAL_CORRECT = 1
ERROR = 2

test_results = {}
cmds_tp = ["gcc -Iinclude -Lbin -o angr/%s.out -xc - -lutils",
        "python script/angr_run.py -r -l%d angr/%s.out"]

func_pattern = re.compile(r'int[ \t\n]+%s\(([^)]*)\);*' % func_name)

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

for file, dirs, files in os.walk('src'):
    for file in files:
        cmds = []
        fp = os.path.join(root, file)
        with open(fp) as f:
            content = f.read()
        finds = func_pattern.findall(content)
        if len(finds) > 1:
            raise SyntaxError(repr(finds) + '. Duplicated definition!')
        elif len(finds) == 0:
            continue
        else:
            params = finds[0].strip()
            params_list = params_list_parser(params)
            vars_list = [_[1] for _ in params_list]
            params = ', '.join(vars_list)

        init_vars = dict(vp=params_list, vars=vars_list, params=params)
        tp = tpp.TemplateParser('templates/angr.c')
        sruner = sr.ScriptRunner(init_vars)
        res = sruner.run(tp.parse()[0])
        res = '\n'.join(res[1])
        res = tp.replace([res, ])
        res = '\n'.join([content, res])
        print(res)
        outname = file if len(file.split('.')) == 1 else file.split('.')[0]
        cmds.append(cmds_tp[0] % outname)
        cmds.append(cmds_tp[1] % (4, outname))

        # Compile
        p = subprocess.Popen(cmds[0].split(' '), stdin=subprocess.PIPE)
        p.communicate(res.encode('utf8'))
        # Run test
        p = subprocess.Popen(cmds[1].split(' '))
        rt_vale = p.wait()

        test_results[fp] = rt_vale
