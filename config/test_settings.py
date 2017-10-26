# ============ run_tests Setting ==============
FUNC_NAME = 'logic_bomb'

src_dirs = [
    'src/covert_propogation',

    # 'src/exception_handling',

    # 'src/external_functions',
    # 'src/floatpoint',
    'src/hash',
    # 'src/overflow',
    # 'src/parallel_program',
    # 'src/symbolic_array',
    # 'src/symbolic_jump',
    # 'src/symbolic_value',

    # 'src/symbolic_variable',
]

cmds_tp_angr = ["gcc -Iinclude -Lbin -o angr/%s.out -xc - -lutils -lpthread -lcrypto -lm",
            "python script/angr_run.py -r -l%d angr/%s.out"]

cmds_tp_klee = [
    "clang -Iinclude -Lbin -emit-llvm -o klee/%s.bc -c -g klee/a.c -lpthread -lutils -lcrypto -lm",
    "klee klee/%s.bc",
    "python3 script/klee_run.py -e%d"
]

cmds_tp_triton = [
    "gcc -Iinclude -Lbin -o triton/%s.out -xc - -lutils -lpthread -lcrypto -lm",
    "python script/triton_caller.py -l%d -m%d -f%s -i%s -p triton/%s.out"
]

angr_tp_path = 'templates/default.c'
triton_tp_path = 'templates/default.c'
klee_tp_path = 'templates/klee.c'

switches = {
    'angr': [cmds_tp_angr, angr_tp_path, 'angr'],
    'triton': [cmds_tp_triton, triton_tp_path, 'triton'],
    'klee': [cmds_tp_klee, klee_tp_path, 'klee']
}

# ============ triton Setting ==============
TRITON_INSTALLATION_PATH = '/home/neil/Triton/build/triton' # For example, /home/zzrcxb/Triton/build/triton
