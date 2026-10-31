from __future__ import annotations
import json,subprocess,sys,tempfile,unittest
from pathlib import Path
class DirectCodeOwnershipTest(unittest.TestCase):
 def test_direct_code_ownership_verifier_passes(self)->None:
  root=Path(__file__).resolve().parents[1]
  immutable=root/"reports"/"stage_21_16_2_direct_code_migration_anti_overlay.json"
  before_bytes=immutable.read_bytes();before_stat=immutable.stat()
  with tempfile.TemporaryDirectory(prefix="rom_v2_direct_ownership_") as directory:
   report=Path(directory)/"direct_code_migration_anti_overlay.json"
   cp=subprocess.run([sys.executable,"-m","tools.verify_v2_direct_code_ownership","--project-root",str(root),"--baseline",str(root/"reports"/"stage_21_16_2_direct_code_ownership_baseline.json"),"--json",str(report)],cwd=root,text=True,capture_output=True)
   self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
   self.assertEqual(json.loads(report.read_text(encoding="utf-8"))["status"],"PASS")
  after_stat=immutable.stat()
  self.assertEqual(immutable.read_bytes(),before_bytes)
  self.assertEqual(after_stat.st_mtime_ns,before_stat.st_mtime_ns)
  self.assertEqual(getattr(after_stat,"st_ctime_ns",None),getattr(before_stat,"st_ctime_ns",None))
if __name__=="__main__":unittest.main()
