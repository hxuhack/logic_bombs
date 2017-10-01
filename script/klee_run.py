import sys
import os
import run_tests
from termcolor import colored
from subprocess import Popen, call, PIPE
import argparse


os.environ['LD_LIBRARY_PATH'] = '/home/klee/klee_build/klee/lib/:$LD_LIBRARY_PAT'
lib_path = '/home/klee/klee_build/klee/lib/'

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--expected", type=int, help="Expected amount of results")
args = parser.parse_args()
print(colored('[+] Compiling ...', 'green'))

os.system('sh /home/klee/ConcTrignr/klee/run_program.sh')
os.system('gcc -L ' + lib_path + ' -o klee/a.out klee/a.c -lkleeRuntest')

running_res = set()
for file in os.listdir(os.path.join(sys.argv[2], 'klee-last')):
    if file.endswith('.ktest'):
        cmd = 'KTEST_FILE=klee/klee-last/%s' % file
        os.system(cmd + ' klee/a.out')
        pipe = Popen(['echo', '$?'], stdout=PIPE)
        res = pipe.wait()
        running_res.add(res)

tests = running_res
if args.expected is None:
    standard = {0, 1}
elif args.expected == 2:
    standard = {0, 1}
elif args.expected == 1:
    standard = {0, }
else:
    exit(-1)

for i in tests:
    if i in standard:
        standard.remove(i)
exit(2 - len(standard))
