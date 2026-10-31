from __future__ import annotations
import ast,unittest
from rom_v2.presentation.development_shell import build_start_view
class InventoryMenuEntryTest(unittest.TestCase):
 def test_start_view_keeps_canonical_inline_menu(self):
  markup=build_start_view().reply_markup;self.assertIn("inline_keyboard",markup)
  callbacks=[button["callback_data"] for row in markup["inline_keyboard"] for button in row]
  self.assertIn("v2:profile:root",callbacks)
 def test_bot_sends_persistent_profile_keyboard_on_start(self):
  from pathlib import Path
  import rom_v2.app.development_bot as module
  source=Path(module.__file__).read_text(encoding="utf-8")
  self.assertIn('"is_persistent": True',source);self.assertIn('"resize_keyboard": True',source)
  self.assertIn('{"text": "👤 Профіль"}',source);self.assertIn('text == "/start"',source)
 def test_bot_routes_persistent_inventory_text_to_canonical_callback(self):
  from pathlib import Path
  import rom_v2.app.development_bot as module
  source=Path(module.__file__).read_text(encoding="utf-8");tree=ast.parse(source)
  self.assertIn('text == "👤 Профіль"',source);self.assertIn('text == "🎒 Інвентар"',source);self.assertIn('text == "🔙 Назад"',source);self.assertIn('callback(user_id, "v2:inventory:open")',source)
  self.assertNotIn('text == "Інвентар"',source)
if __name__=="__main__":unittest.main()
