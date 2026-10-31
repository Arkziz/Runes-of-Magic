from __future__ import annotations
import unittest
from pathlib import Path
from rom_v2.presentation.development_shell import build_start_view
from rom_v2.presentation.navigation import main_reply_keyboard,profile_reply_keyboard
class InventoryMenuEntryTest(unittest.TestCase):
 def test_start_view_has_only_status_inline_action(self):
  markup=build_start_view().reply_markup;callbacks=[b["callback_data"] for row in markup["inline_keyboard"] for b in row]
  self.assertEqual(callbacks,["v2:shell:status"]);self.assertNotIn("v2:profile:root",callbacks)
 def test_persistent_keyboards_are_owned_by_navigation(self):
  self.assertTrue(main_reply_keyboard()["is_persistent"]);self.assertTrue(main_reply_keyboard()["resize_keyboard"])
  self.assertEqual(main_reply_keyboard()["keyboard"],[[{"text":"👤 Профіль"}]])
  self.assertEqual(profile_reply_keyboard()["keyboard"],[[{"text":"🎒 Інвентар"}],[{"text":"🔙 Назад"}]])
 def test_bot_consumes_navigation_owner(self):
  import rom_v2.app.development_bot as module
  source=Path(module.__file__).read_text(encoding="utf-8")
  self.assertIn("main_reply_keyboard()",source);self.assertIn("profile_reply_keyboard()",source)
if __name__=="__main__":unittest.main()
