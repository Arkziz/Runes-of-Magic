from __future__ import annotations
import subprocess,sys,tempfile,unittest
from pathlib import Path
from rom_v2.app.runtime_launcher import _allowed_ids
class MinimalEntrypointTest(unittest.TestCase):
 def test_main_is_thin_and_delegates_composition(self):
  root=Path(__file__).resolve().parents[1];source=(root/"rom_v2"/"main.py").read_text(encoding="utf-8")
  self.assertLessEqual(len(source.splitlines()),20);self.assertIn("rom_v2.app.runtime_launcher import main",source)
  self.assertNotIn("V2ConnectionFactory",source);self.assertNotIn("TelegramBotApi",source)
 def test_direct_file_execution_resolves_package(self):
  root=Path(__file__).resolve().parents[1]
  with tempfile.TemporaryDirectory() as d:
   cp=subprocess.run([sys.executable,str(root/"rom_v2"/"main.py")],cwd=d,text=True,capture_output=True,env={**__import__("os").environ,"ROM_V2_BOT_TOKEN":""})
  self.assertNotIn("ModuleNotFoundError",cp.stderr);self.assertIn("ROM_V2_BOT_TOKEN is missing",cp.stderr)
 def test_short_package_entrypoint_imports(self):
  root=Path(__file__).resolve().parents[1];cp=subprocess.run([sys.executable,"-c","import rom_v2.__main__"],cwd=root,text=True,capture_output=True)
  self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
 def test_allowlist_remains_optional(self):self.assertEqual(_allowed_ids(""),frozenset())
if __name__=="__main__":unittest.main()
