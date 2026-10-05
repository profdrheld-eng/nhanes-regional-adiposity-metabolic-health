"""Compare regenerated aggregate CSVs with the frozen published results."""
from pathlib import Path
import json
import sys
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def compare(work):
    checked=[]
    for folder in ('results','tables'):
        for ref in sorted((ROOT/'04_outputs'/folder).glob('*.csv')):
            if ref.name=='revision_population_comparison.csv':continue
            actual=work/'04_outputs'/folder/ref.name
            a=pd.read_csv(ref);b=pd.read_csv(actual)
            pd.testing.assert_frame_equal(a,b,check_exact=False,rtol=1e-9,atol=1e-11)
            checked.append(str(ref.relative_to(ROOT)))
    (work/'numerical_comparison.json').write_text(json.dumps({'status':'PASS','rtol':1e-9,'atol':1e-11,'files':checked},indent=2))
    print('PASS:',len(checked),'aggregate files reproduced')
if __name__=='__main__':compare(Path(sys.argv[1]))
