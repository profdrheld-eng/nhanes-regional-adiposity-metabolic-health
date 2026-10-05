"""Reproduce in a new external work directory; never reuse reference outputs."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def prepare_work(work, root):
    work, root = work.resolve(), root.resolve()
    if work == root or root in work.parents:
        raise ValueError('Work directory must be outside the released repository')
    work.mkdir(parents=True, exist_ok=False)
    for name in ('01_project', '03_analysis'):
        shutil.copytree(root/name, work/name, ignore=shutil.ignore_patterns('__pycache__', 'matplotlib-cache', 'models'))
    for name in ('source', 'quality_control'):
        shutil.copytree(root/'05_manuscript'/name, work/'05_manuscript'/name)
    shutil.copytree(root/'02_data/manifests', work/'02_data/manifests')
    (work/'04_outputs/results').mkdir(parents=True)
    # This documented historical aggregate is not an input to any study estimate.
    shutil.copy2(root/'04_outputs/results/revision_population_comparison.csv',work/'04_outputs/results/revision_population_comparison.csv')
    return work

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work-dir',type=Path,required=True)
    parser.add_argument('--data-dir',type=Path,help='Existing directory containing the 69 public XPT files; without it, download from CDC')
    args=parser.parse_args()
    subprocess.run([sys.executable,str(ROOT/'verify_release.py')],check=True)
    subprocess.run([sys.executable,str(ROOT/'03_analysis/environment/check_environment.py')],check=True)
    if args.data_dir and not args.data_dir.is_dir():parser.error('Data directory does not exist')
    work=prepare_work(args.work_dir,ROOT)
    if args.data_dir:
        import csv
        (work/'02_data/raw_public').mkdir(parents=True)
        with (work/'02_data/manifests/raw-public-file-manifest.csv').open() as f:
            for row in csv.DictReader(f):
                if row['download_status']=='downloaded':shutil.copy2(args.data_dir/row['file'],work/'02_data/raw_public'/row['file'])
    env=os.environ.copy();env['PYTHON_BIN']=sys.executable;env['DOCX_PYTHON_BIN']=sys.executable
    with (work/'reproduction.log').open('w') as log:
        subprocess.run([sys.executable,str(work/'03_analysis/code/00_download_sources.py')],check=True,stdout=log,stderr=subprocess.STDOUT,env=env)
        subprocess.run(['sh',str(work/'03_analysis/run_analysis.sh')],check=True,stdout=log,stderr=subprocess.STDOUT,env=env)
        subprocess.run([sys.executable,str(ROOT/'06_validation/compare_results.py'),str(work)],check=True,stdout=log,stderr=subprocess.STDOUT)
    (work/'pipeline_complete.json').write_text(json.dumps({'status':'PASS','release_manifest':str(ROOT/'release-manifest.json')},indent=2))
    print('PASS: complete reproduction; outputs and log are in',work)

if __name__=='__main__':main()
