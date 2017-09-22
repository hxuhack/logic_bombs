import sys
import os
import run_tests
from termcolor import colored
from subprocess import Popen, call, PIPE


lib_path = '/home/klee/klee_build/klee/lib/'

print(colored('[+] Compiling %s ...' % sys.argv[1], 'green'))

os.system('sh /home/klee/ConcTrignr/klee/run_program.sh')
os.system('gcc -L ' + lib_path + ' ' + sys.argv[1] + ' -lkleeRuntest')

running_res = set()
for file in os.listdir(os.path.join(sys.argv[2], 'klee-last')):
    if file.endswith('.ktest'):
        cmd = 'KTEST_FILE=klee-last/%s' % file
        os.system(cmd + ' ./a.out')
        pipe = Popen(['echo', '$?'], stdout=PIPE)
        res = pipe.wait()
        running_res.add(res)

if len(running_res) == 2:
    exit(run_tests.CORRECT)
elif len(running_res) == 0:
    exit(run_tests.ERROR)
else:
    exit(running_res.PARTIAL_CORRECT)
