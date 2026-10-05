import importlib.util
from pathlib import Path
import tempfile
import unittest
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class ReleaseTests(unittest.TestCase):
 def test_refuses_existing_work(self):
  runner=load('runner',ROOT/'run_reproduction.py')
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(FileExistsError):runner.prepare_work(Path(d),ROOT)
 def test_refuses_work_inside_release(self):
  runner=load('runner2',ROOT/'run_reproduction.py')
  with self.assertRaises(ValueError):runner.prepare_work(ROOT/'forbidden_test_work',ROOT)
 def test_bootstrap_psu_clusters(self):
  b=load('bootstrap',ROOT/'03_analysis/code/survey_bootstrap.py');s=np.array([1,1,1,1,2,2,2,2]);p=np.array([1,1,2,2,1,1,2,2]);f=b.rescaled_psu_factors(s,p,np.random.default_rng(7))
  self.assertEqual(set(f),{0,2});self.assertEqual(f.sum(),8)
  for a in [1,2]:
   for c in [1,2]:self.assertEqual(len(set(f[(s==a)&(p==c)])),1)
 def test_bootstrap_refuses_single_psu(self):
  b=load('bootstrap2',ROOT/'03_analysis/code/survey_bootstrap.py')
  with self.assertRaises(ValueError):b.rescaled_psu_factors(np.array([1,1]),np.array([1,1]),np.random.default_rng(1))
 def test_download_checksum_rejects_corruption(self):
  b=load('download',ROOT/'03_analysis/code/00_download_sources.py')
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'input';p.write_bytes(b'abc');self.assertTrue(b.valid(p,{'bytes':3,'md5':'900150983cd24fb0d6963f7d28e17f72'}));p.write_bytes(b'bad');self.assertFalse(b.valid(p,{'bytes':3,'md5':'900150983cd24fb0d6963f7d28e17f72'}))
if __name__=='__main__':unittest.main()
