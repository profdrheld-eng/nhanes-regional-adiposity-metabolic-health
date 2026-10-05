"""Verify the exact released inventory, including unexpected files outside .git."""
from pathlib import Path
import hashlib
import json
ROOT=Path(__file__).resolve().parent

def main():
    expected=json.loads((ROOT/'release-manifest.json').read_text())
    actual={str(p.relative_to(ROOT)):p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.relative_to(ROOT).parts and '__pycache__' not in p.relative_to(ROOT).parts and p.name!='release-manifest.json'}
    if set(actual)!=set(expected):raise RuntimeError('Release inventory differs: '+str(sorted(set(actual)^set(expected))))
    for name,path in actual.items():
        if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected[name]:raise RuntimeError('Release file differs: '+name)
    print('PASS:',len(actual),'release file hashes verified')
if __name__=='__main__':main()
