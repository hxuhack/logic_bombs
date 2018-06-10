import sys
import os
import re
import subprocess
from termcolor import colored
from subprocess import Popen, call, PIPE
import argparse
import csv


os.environ['LD_LIBRARY_PATH'] = '/home/klee/klee_build/klee/lib/:$LD_LIBRARY_PAT'
lib_path = '/home/klee/klee_build/klee/lib/'

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--expected", type=int, help="Expected amount of results")
parser.add_argument("-p", "--program", type=str, help="Binary program")
args = parser.parse_args()
print(colored('[+] Compiling ...', 'green'))

cmd = 'clang -Iinclude -L ' + lib_path + ' -Lbuild -o klee/a.out klee/a.c -lkleeRuntest -lpthread -lutils -lcrypto -lm'
p = Popen(cmd.split(' '))
rt_value = p.wait()
if rt_value != 0:
    exit(3)

pattern = re.compile(r"data:(.*)\n")
tests = []
running_res = set()
for file in sorted(os.listdir(os.path.join('klee', 'klee-last'))):
    if file.endswith('.ktest'):
        cmd = 'KTEST_FILE=klee/klee-last/%s' % file
        res = os.system(cmd + ' klee/a.out') >> 8
        running_res.add(res)
        p = subprocess.Popen(str.split("ktest-tool --write-ints klee/klee-last/%s" % file, ' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        out = out.decode('utf8')
        print(out)
        res = pattern.findall(out)[0].strip()
        tests.append(res)

tests = running_res

if 3 in tests:
    exit(1)
elif 139 in tests:
    exit(-1)
elif 0 in tests:
    exit(0)
else:
    exit(-1)
