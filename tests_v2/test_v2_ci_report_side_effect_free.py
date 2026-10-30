from __future__ import annotations
import hashlib,importlib.util,sys,tempfile,unittest
from pathlib import Path
class SideEffectFreeCiTest(unittest.TestCase):
 def load(self):
  root=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location("v2_ci_under_test",root/"tools"/"run_v2_ci.py");module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
 def test_report_restored_on_failure(self):
  module=self.load()
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/"reports").mkdir();report=root/"reports"/"stage_21_16_2_direct_code_migration_anti_overlay.json";report.write_bytes(b"immutable\n");before=hashlib.sha256(report.read_bytes()).hexdigest()
   def failing():report.write_text("changed",encoding="utf-8");raise RuntimeError("expected")
   module._main_with_report_side_effects=failing;old=sys.argv;sys.argv=["run_v2_ci.py","--project-root",str(root)]
   try:
    with self.assertRaisesRegex(RuntimeError,"expected"):module.main()
   finally:sys.argv=old
   self.assertEqual(hashlib.sha256(report.read_bytes()).hexdigest(),before)
 def test_generated_report_removed_when_initially_absent(self):
  module=self.load()
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/"reports").mkdir();report=root/"reports"/"stage_21_16_2_direct_code_migration_anti_overlay.json"
   def passing():report.write_text("generated",encoding="utf-8");return 0
   module._main_with_report_side_effects=passing;old=sys.argv;sys.argv=["run_v2_ci.py","--project-root",str(root)]
   try:self.assertEqual(module.main(),0)
   finally:sys.argv=old
   self.assertFalse(report.exists())
if __name__=="__main__":unittest.main()
