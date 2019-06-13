import os
import re
import subprocess
import template_parser as tpp
import script_runner as sr
import shutil
import json
import psutil

from config.test_settings import TRITON_INSTALLATION_PATH, FUNC_NAME


def kill_all(process):
    parent = psutil.Process(process.pid)
    for child in parent.children(recursive=True):
        child.kill()
    parent.kill()


def ATKrun(target, func_name='logic_bomb', default_stdin_len=10, maxtime=60, source=None, skip=False, folder=None):
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

    cmds_tp, tp_path, prefix, src_dirs = target
    if folder:
        src_dirs = (folder, )
    if not os.path.exists(prefix):
        os.mkdir(prefix)

    if source and not os.path.exists(source):
        os.mkdir(source)

    ERROR = 0
    CORRECT = 1
    COMPILE_ERROR = 3
    TLE = 4
    RUNTIME_ERROR = 255

    MAX_TIME = maxtime
    test_results = {}

    func_pattern = re.compile(r'int[ \t\n]+%s\(([^)]*)\);*' % func_name)

    for src_dir in src_dirs:
        print('===========')
        print('In dir ' + src_dir)
        for root, dirs, files in sorted(os.walk(src_dir)):
            for file in sorted(files):
                cmds = []
                fp = os.path.join(root, file)
                print('-----------------------------')
                print(fp)
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
                    params_list_with_length = []
                    comments_pattern = re.compile(r'//(.*)\n[ \t]*' + r'int[ \t\n]+%s\(([^)]*)\);*' % func_name)
                    cmts = comments_pattern.findall(content)
                    cmt = cmts[0] if len(cmts) > 0 else ('{}', )
                    cmt_dict = json.loads(cmt[0])
                    for var_type, var_name in params_list:
                        length = cmt_dict.get(var_name, {}).get('length', 0)
                        params_list_with_length.append((var_type, var_name, length))

                init_vars = dict(vp=params_list_with_length, params=params, func_name=FUNC_NAME)
                tp = tpp.TemplateParser(tp_path)
                sruner = sr.ScriptRunner(init_vars)
                res = sruner.run(tp.parse()[0])
                res = '\n'.join(res[1])
                res = tp.replace([res, ])
                print(res)
                res = '\n'.join([content, res])
                outname = file if len(file.split('.')) == 1 else file.split('.')[0]
                if source:
                    with open(os.path.join(source, file), 'w') as f:
                        f.write(res)
                    if skip:
                        continue
                if prefix == 'angr':
                    cmds.append(cmds_tp[0] % outname)
                    cmds.append(cmds_tp[1] % (default_stdin_len, outname))

                    # Compile
                    p = subprocess.Popen(cmds[0].split(' '), stdin=subprocess.PIPE)
                    p.communicate(res.encode('utf8'))
                    cp_value = p.wait()
                    if cp_value:
                        test_results[fp] = COMPILE_ERROR
                        print('========= Compile Error! ==========')
                        continue
                    # Run test
                    p = subprocess.Popen(cmds[1].split(' '))
                    print(p.pid)
                    try:
                        rt_vale = p.wait(timeout=MAX_TIME)
                        test_results[fp] = rt_vale
                    except subprocess.TimeoutExpired:
                        test_results[fp] = TLE
                        kill_all(p)

                if prefix == 'mcore':
                    cmds.append(cmds_tp[0] % outname)
                    cmds.append(cmds_tp[1] % (MAX_TIME-30, default_stdin_len, outname))

                    # Compile
                    p = subprocess.Popen(cmds[0].split(' '), stdin=subprocess.PIPE)
                    p.communicate(res.encode('utf8'))
                    cp_value = p.wait()
                    if cp_value:
                        test_results[fp] = COMPILE_ERROR
                        print('========= Compile Error! ==========')
                        continue
                    # Run test
                    p = subprocess.Popen(cmds[1].split(' '))
                    print(p.pid)
                    try:
                      rt_vale = p.wait(timeout=MAX_TIME)
                      test_results[fp] = rt_vale
                    except:
                        test_results[fp] = TLE
                        kill_all(p)

                elif prefix == 'klee':
                    if not os.path.exists('klee'):
                        os.mkdir('klee')

                    with open('klee/a.c', 'w') as f:
                        f.write(res)

                    cmds.append(cmds_tp[0] % outname)
                    cmds.append(cmds_tp[1] % outname)
                    cmds.append(cmds_tp[2] % (2, outname))
                    p = subprocess.Popen(cmds[0].split(' '), stdin=subprocess.PIPE)
                    p.communicate(res.encode('utf8'))
                    cp_value = p.wait()
                    if cp_value:
                        test_results[fp] = COMPILE_ERROR
                        print('========= Compile Error! ==========')
                        continue
                    try:
                        p = subprocess.Popen(cmds[1].split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        errored = False
                        out, err = p.communicate(timeout=MAX_TIME)
                        rt_vale = p.wait(timeout=MAX_TIME)
                    except subprocess.TimeoutExpired:
                        test_results[fp] = TLE
                        kill_all(p)
                        continue

                    p = subprocess.Popen(cmds[2].split(' '))
                    try:
                        rt_vale = p.wait(timeout=MAX_TIME)
                        test_results[fp] = rt_vale
                    except subprocess.TimeoutExpired:
                        test_results[fp] = TLE
                        kill_all(p)
                    shutil.rmtree('klee')
                elif prefix == 'triton':
                    cmds.append(cmds_tp[0] % outname)
                    cmds.append(cmds_tp[1] % (default_stdin_len, MAX_TIME, FUNC_NAME, 
                            TRITON_INSTALLATION_PATH , outname))

                    # Compile
                    p = subprocess.Popen(cmds[0].split(' '), stdin=subprocess.PIPE)
                    p.communicate(res.encode('utf8'))
                    cp_value = p.wait()
                    if cp_value:
                        test_results[fp] = COMPILE_ERROR
                        print('========= Compile Error! ==========')
                        continue

                    # Run test
                    print("=== Run test!", outname, "===")
                    p = subprocess.Popen(cmds[1].split(' '))
                    rt_vale = p.wait()
                    test_results[fp] = rt_vale

    return test_results


if __name__ == '__main__':
    from config.test_settings import switches, FUNC_NAME
    from collections import OrderedDict
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--engine", required=True, type=str, help="Symbolic execution engine")
    parser.add_argument("-t", "--maxtime", required=False, default=60, type=int, help="Max running time for a program")
    parser.add_argument("-s", "--source", required=False, type=str, help="Output source code into a directory")
    parser.add_argument("-n", "--no_test", action="store_true", help="Don't do the test")
    parser.add_argument("-f", "--folder", type=str, help="Overide test dir in config")
    args = parser.parse_args()
    
    if args.source:
        print("Saving output results in ", args.source)

    try:
        res = ATKrun(switches[args.engine], func_name=FUNC_NAME, maxtime=args.maxtime, source=args.source, skip=args.no_test, folder=args.folder)
        if args.source and args.no_test:
            exit(0)
    except KeyError:
        print('Invalid symbolic engine!')
        exit(1)

    results = {}
    for key, item in res.items():
        parent = os.path.split(key)[0].split('/')[-1]
        name = os.path.split(key)[-1].split('.')[0]
        if parent not in results:
            results[parent] = {name: item,}
        else:
            results[parent][name] = item

    for parent in results:
        results[parent] = OrderedDict(sorted(results[parent].items()))
    results = OrderedDict(sorted(results.items()))
    print(results)

    import csv

    with open('results-{}-{}.csv'.format(args.engine, args.maxtime), 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        for parent in results:
            for name in results[parent]:
                writer.writerow([parent, name, results[parent][name]])
