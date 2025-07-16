import os
import subprocess

for root, dirs, files in os.walk('.'):
    for d in dirs:
        if d == '__pycache__':
            path = os.path.join(root, d)
            print(f"Removing from git: {path}")
            subprocess.run(["git", "rm", "-r", "--cached", path])

    for f in files:
        if f.endswith('.pyc'):
            path = os.path.join(root, f)
            print(f"Removing from git: {path}")
            subprocess.run(["git", "rm", "--cached", path])
