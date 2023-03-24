import sys
import subprocess
import os

while True:
    procs = []
    for i in range(10):
        proc = subprocess.Popen([sys.executable, 'Aragorn.py'])
        procs.append(proc)

    for proc in procs:
        proc.wait()

    print("=======================================================run complete=======================================================")
    os.system('sudo service tor reload')