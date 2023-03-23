import sys
import subprocess
import os

while True:
    proc = subprocess.Popen([sys.executable, 'Arwen.py'])
    proc.wait()

    print("=======================================================run complete=======================================================")
    os.system('sudo service tor reload')