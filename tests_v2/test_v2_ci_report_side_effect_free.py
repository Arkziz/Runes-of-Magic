from __future__ import annotations
import ast,unittest
from pathlib import Path
class SideEffectFreeCiContractTest(unittest.TestCase):
 def test_ci_does_not_reference_historical_report(self):
  root=Path(__file__).resolve().parents[1];source=(root/"tools"/"run_v2_ci.py").read_text(encoding="utf-8");tree=ast.parse(source)
  main=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=="main")
  body=ast.unparse(main)
  self.assertNotIn("stage_21_16_2_direct_code_migration_anti_overlay",body)
  self.assertNotIn("write_bytes",body);self.assertNotIn("unlink",body)
 def test_direct_ownership_check_uses_temporary_output(self):
  root=Path(__file__).resolve().parents[1];source=(root/"tests_v2"/"test_direct_code_ownership.py").read_text(encoding="utf-8")
  self.assertIn("TemporaryDirectory",source)
  self.assertIn("before_stat.st_mtime_ns",source)
if __name__=="__main__":unittest.main()
