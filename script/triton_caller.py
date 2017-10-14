import subprocess
import argparse
import os
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--expected", type=int, help="Expected amount of results")
parser.add_argument("-p", "--program", type=str, help="Binary program")
parser.add_argument("-l", "--length", type=int, help="STDIN length")
args = parser.parse_args()

prog = args.program

pt = re.compile(r'New input: \{([\d]+L: [\d]*L, *)*[\d]+L: [\d]*L\}')
case_pt = re.compile(r'[\d]+L: ([\d]*)L')

with open('script/triton_run.py', 'r') as f:
    content = f.read()
    
content = content.format(path=prog, length=args.length)

with open('triton/triton_run.py', 'w') as f:
    f.write(content)

print(' '.join(['/home/neil/Triton/build/triton', 'triton/triton_run.py', prog]))

p = subprocess.Popen(['/home/neil/Triton/build/triton', 'triton/triton_run.py', prog, '0' * args.length], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

out, err = p.communicate()
out = out.decode('utf8', 'ignore')
err = err.decode('utf8', 'ignore')
p.wait()
print(out, err)
reses = ['0' * args.length, ]
for testcase in pt.finditer(out):
    tmp = case_pt.findall(out)
    tmp = ''.join(list(map(lambda x: '\\x' + '%02x' % x, map(int, tmp))))
    print(tmp)
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
