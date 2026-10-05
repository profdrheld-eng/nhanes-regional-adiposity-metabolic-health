"""Download frozen public NHANES inputs and verify them before use."""
import csv
import hashlib
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[2]

def valid(path, row):
    return (path.is_file() and path.stat().st_size == int(row['bytes'])
            and hashlib.md5(path.read_bytes()).hexdigest() == row['md5'])

def main():
    target = ROOT / '02_data/raw_public'
    target.mkdir(parents=True, exist_ok=True)
    with (ROOT / '02_data/manifests/raw-public-file-manifest.csv').open() as f:
        rows = [row for row in csv.DictReader(f) if row['download_status'] == 'downloaded']
    if len(rows) != 69:
        raise ValueError('Expected exactly 69 frozen available source files')
    for row in rows:
        name = row['file']
        if Path(name).name != name or not row['url'].startswith('https://wwwn.cdc.gov/'):
            raise ValueError('Unexpected source manifest entry')
        dest = target / name
        if dest.exists():
            if not valid(dest, row):
                raise RuntimeError(f'Existing source differs from frozen manifest: {name}; not overwritten')
            continue
        temp = dest.with_suffix('.download')
        try:
            request = urllib.request.Request(row['url'], headers={'User-Agent': 'NHANES-reproducibility/1.0'})
            with urllib.request.urlopen(request, timeout=90) as response, temp.open('wb') as out:
                while chunk := response.read(1024 * 1024):
                    out.write(chunk)
            if not valid(temp, row):
                raise RuntimeError(f'Size/checksum mismatch: {name}')
            temp.rename(dest)
            print('Verified', name, flush=True)
        finally:
            if temp.exists(): temp.unlink()
    print(f'PASS: {len(rows)} source files verified')

if __name__ == '__main__':
    main()
