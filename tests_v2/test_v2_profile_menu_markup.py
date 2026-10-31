from __future__ import annotations
import unittest
from rom_v2.presentation.development_shell import build_start_view
class ProfileMenuMarkupTest(unittest.TestCase):
 def test_inline_keyboard_is_valid_single_status_row(self):
  markup=build_start_view().reply_markup;keyboard=markup["inline_keyboard"]
  self.assertIsInstance(keyboard,list);self.assertEqual(len(keyboard),1)
  self.assertIsInstance(keyboard[0],list);self.assertEqual(len(keyboard[0]),1)
  button=keyboard[0][0];self.assertEqual(button["text"],"Стан V2");self.assertEqual(button["callback_data"],"v2:shell:status")
 def test_inline_profile_entry_is_absent(self):
  callbacks=[b["callback_data"] for row in build_start_view().reply_markup["inline_keyboard"] for b in row]
  self.assertNotIn("v2:profile:root",callbacks)
if __name__=="__main__":unittest.main()
