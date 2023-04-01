import sys
import subprocess


procs = []
for i in range(10):
    proc = subprocess.Popen([sys.executable, 'Aragorn_Mid_Layer.py'])
    procs.append(proc)

for proc in procs:
    proc.wait()
