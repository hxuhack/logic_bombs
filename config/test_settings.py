# ============ run_tests Setting ==============
FUNC_NAME = 'logic_bomb'

src_dirs = [
    # 'src/buffer_overflow',
    'src/contextual_symbolic_value',
    # 'src/covert_propogation',
    # 'src/crypto_functions',
    # 'src/data_overflow',
    # 'src/external_functions',
    # 'src/floating_point',
    # 'src/loop',
    # 'src/parallel_program',
    # 'src/symbolic_jump',
    # 'src/symbolic_memory',

    # 'src_cpp/covert_propagation',
    # 'src_cpp/symbolic_jump',
    # 'src_cpp/symbolic_memory',

    # 'sick/'
    # 'src/symbolic_variable_declaration',
]

cmds_tp_angr = ["clang -Iinclude -Lbuild -o angr/%s.out -xc - -lutils -lpthread -lcrypto -lm",
            "python script/angr_run.py -r -l%d angr/%s.out"]

cmds_tp_angr_cpp = ["clang++ -Iinclude -Lbuild -o angr/%s.out -xc++ - -lutils -lpthread -lcrypto -lm",
            "python script/angr_run.py -r -l%d angr/%s.out"]

cmds_tp_klee = [
    "clang -Iinclude -Lbuild -emit-llvm -o klee/%s.bc -c -g klee/a.c -lpthread -lutils -lcrypto -lm",
    "klee klee/%s.bc",
    "python3 script/klee_run.py -e%d"
]

cmds_tp_klee_cpp = [
    "clang++ -Iinclude -Lbuild -emit-llvm -o klee/%s.bc -c -g klee/a.c -lpthread -lutils -lcrypto -lm",
    "klee klee/%s.bc",
    "python3 script/klee_run_cpp.py -e%d"
]

cmds_tp_triton = [
    "clang -Iinclude -Lbuild -o triton/%s.out -xc - -lutils -lpthread -lcrypto -lm",
    "python script/triton_caller.py -l%d -m%d -f%s -i%s -p triton/%s.out"
]

cmds_tp_triton_cpp = [
    "clang++ -Iinclude -Lbuild -o triton/%s.out -xc++ - -lutils -lpthread -lcrypto -lm",
    "python script/triton_caller.py -l%d -m%d -f%s -i%s -p triton/%s.out"
]

angr_tp_path = 'templates/default_no_printf.c'
triton_tp_path = 'templates/default_no_printf.c'
klee_tp_path = 'templates/klee.c'

switches = {
    'angr': [cmds_tp_angr, angr_tp_path, 'angr'],
    'angr_cpp': [cmds_tp_angr_cpp, angr_tp_path, 'angr'],
    'triton': [cmds_tp_triton, triton_tp_path, 'triton'],
    'triton_cpp': [cmds_tp_triton_cpp, triton_tp_path, 'triton'],
    'klee': [cmds_tp_klee, klee_tp_path, 'klee'],
    'klee_cpp': [cmds_tp_klee_cpp, klee_tp_path, 'klee']
}

# ============ triton Setting ==============
TRITON_INSTALLATION_PATH = '/home/neil/Triton/build/triton' # For example, /home/zzrcxb/Triton/build/triton
