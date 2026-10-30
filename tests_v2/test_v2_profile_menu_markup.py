from __future__ import annotations
import unittest
from rom_v2.presentation.development_shell import build_start_view
class ProfileMenuMarkupTest(unittest.TestCase):
 def test_inline_keyboard_is_telegram_valid_matrix(self):
  markup=build_start_view().reply_markup;keyboard=markup["inline_keyboard"]
  self.assertIsInstance(keyboard,list);self.assertGreaterEqual(len(keyboard),2)
  for row in keyboard:
   self.assertIsInstance(row,list);self.assertTrue(row)
   for button in row:
    self.assertIsInstance(button,dict);self.assertIsInstance(button.get("text"),str);self.assertIsInstance(button.get("callback_data"),str)
  callbacks=[button["callback_data"] for row in keyboard for button in row]
  self.assertIn("v2:shell:status",callbacks);self.assertIn("v2:profile:root",callbacks)
if __name__=="__main__":unittest.main()
