import subprocess
import argparse
import os
import re
import sys
import time


parser = argparse.ArgumentParser()
parser.add_argument("-e", "--expected", type=int, help="Expected amount of results")
parser.add_argument("-p", "--program", type=str, help="Binary program")
parser.add_argument("-l", "--length", type=int, help="STDIN length")
parser.add_argument("-m", "--max_time", type=int, help="max time")
parser.add_argument("-f", "--func_name", type=str, help="function name")
parser.add_argument("-i", "--triton_path", type=str, help="triton_path")
args = parser.parse_args()

TRITON_INSTALLATION_PATH = args.triton_path
FUNC_NAME = args.func_name
prog = args.program

pt = re.compile(r'New input: \{([\d]+L: [\d]*L, *)*[\d]+L: [\d]*L\}')
case_pt = re.compile(r'[\d]+L: ([\d]*)L')

with open('script/triton_run.py', 'r') as f:
    content = f.read()
    
content = content.format(path=prog, length=args.length, func_name=FUNC_NAME)

with open('triton/triton_run.py', 'w') as f:
    f.write(content)

print(' '.join([TRITON_INSTALLATION_PATH, 'triton/triton_run.py', prog]))

p = subprocess.Popen([TRITON_INSTALLATION_PATH, 'triton/triton_run.py', prog, '0' * args.length], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
start = time.time()
while time.time() - start < args.max_time:
    rt_value = p.poll()
    if rt_value is not None:
        print(rt_value)
        break
    time.sleep(0.1)
print(time.time() - start)
if time.time() - start > args.max_time:
    p.kill()
    print('timeout!!!!')
    exit(4)

out, err = p.communicate()
out = out.decode('utf8', 'ignore')
err = err.decode('utf8', 'ignore')

print(out)
print(err)
reses = ['0' * args.length, ]
for testcase in pt.finditer(out):
    tmp = case_pt.findall(out)
    tmp = ''.join(list(map(chr, map(int, tmp))))
    print(repr(list(tmp)))
    tmp = tmp.replace('\x00', '')
    reses.append(tmp)

print(reses)

tests = set()
for res in reses:
    p = subprocess.Popen([prog, res])
    rt_value = p.wait()
    tests.add(rt_value)

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
    elif i == 139:
        exit(-1)
exit(2 - len(standard))
