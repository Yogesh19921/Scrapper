import sys
import subprocess

while True:
    proc = subprocess.Popen([sys.executable, 'Aragorn.py'])

    proc.wait()

    print("=======================================================run complete=======================================================")