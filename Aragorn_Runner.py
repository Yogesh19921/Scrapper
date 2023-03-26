import sys
import subprocess
import os


procs = []
for i in range(10):
    proc = subprocess.Popen([sys.executable, 'Aragorn.py', str(i)])
    procs.append(proc)

while True:
    for proc in procs:
        proc.wait()
        procs.remove(proc)
        new_proc = subprocess.Popen([sys.executable, 'Aragorn.py', "0"])
        procs.append(new_proc)

    print("=======================================================run complete=======================================================")
    #os.system('sudo service tor reload')