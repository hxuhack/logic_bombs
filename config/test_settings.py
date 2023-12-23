# ============ run_tests Setting ==============
FUNC_NAME = 'logic_bomb'

cmds_tp_angr = ["clang -Iinclude -Lbuild -o angr/%s.out -xc - -lutils -lpthread -lcrypto -lm",
            "python script/angr_run.py -r -l%d angr/%s.out"]

cmds_tp_angr_cpp = ["clang++ -Iinclude -Lbuild -o angr/%s.out -xc++ - -lutils -lpthread -lcrypto -lm",
            "python script/angr_run.py -r -l%d angr/%s.out"]

cmds_tp_klee = [
    "clang -Iinclude -Lbuild -Wno-unused-parameter -emit-llvm -o klee/%s.bc -c -g klee/a.c -lpthread -lutils -lcrypto -lm",
    "klee --libc=uclibc --posix-runtime klee/%s.bc",
    "python3 script/klee_run.py -e%d -p%s"
]

cmds_tp_triton = [
    "clang -Iinclude -Lbuild -o triton/%s.out -xc - -lutils -lpthread -lcrypto -lm",
    "python script/triton_caller.py -l%d -m%d -f%s -i%s -p triton/%s.out"
]

cmds_tp_triton_cpp = [
    "clang++ -Iinclude -Lbuild -o triton/%s.out -xc++ - -lutils -lpthread -lcrypto -lm",
    "python script/triton_caller.py -l%d -m%d -f%s -i%s -p triton/%s.out"
]

cmds_tp_mcore = ["clang -static -O0 -Iinclude -Lbuild -o mcore/%s.out -xc - -lutils -lpthread -lcrypto -lm",
            "python3 script/mcore_run.py -t%d -r -l%d mcore/%s.out"]

cmds_tp_mcore_cpp = ["clang++ -static -O0 -Iinclude -Lbuild -o mcore/%s.out -xc++ - -lutils -lpthread -lcrypto -lm",
            "python3 script/mcore_run.py -t%d -r -l%d mcore/%s.out"]

angr_tp_path = 'templates/default_no_printf.c'
triton_tp_path = 'templates/default_no_printf.c'
klee_tp_path = 'templates/klee.c'
mcore_tp_path = 'templates/default_no_printf.c'

switches = {
    'angr': [cmds_tp_angr, angr_tp_path, 'angr', ('src/', )],
    'angr_cpp': [cmds_tp_angr_cpp, angr_tp_path, 'angr', ('src_cpp/', )],
    'triton': [cmds_tp_triton, triton_tp_path, 'triton', ('src/', )],
    'triton_cpp': [cmds_tp_triton_cpp, triton_tp_path, 'triton', ('src_cpp/', )],
    'klee': [cmds_tp_klee, klee_tp_path, 'klee', ('src/', )],
    'mcore': [cmds_tp_mcore, mcore_tp_path, 'mcore', ('src/', )],
    'mcore_cpp': [cmds_tp_mcore_cpp, mcore_tp_path, 'mcore', ('src_cpp/', )],
}

# ============ triton Setting ==============
TRITON_INSTALLATION_PATH = '/home/neil/Triton/build/triton' # For example, /home/zzrcxb/Triton/build/triton
