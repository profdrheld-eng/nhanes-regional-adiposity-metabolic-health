"""Check the recorded analysis environment without installing packages."""
from pathlib import Path
import importlib.metadata
import os
import subprocess
import sys
P=Path(__file__).resolve().parent
if sys.version_info[:2]!=(3,12):raise RuntimeError('This release was reproduced with Python 3.12')
for line in (P/'requirements-lock-python312.txt').read_text().splitlines():
    name,version=line.split('==')
    actual=importlib.metadata.version(name)
    if actual!=version:raise RuntimeError(f'{name}: expected {version}, found {actual}')
subprocess.run([os.environ.get('R_BIN','Rscript'),'--vanilla',str(P/'check_environment.R')],check=True)
print('PASS: Python dependency versions match')
