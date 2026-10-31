from __future__ import annotations
import ast,unittest
from pathlib import Path
from rom_v2.presentation import navigation
class NavigationOwnershipTest(unittest.TestCase):
 def test_canonical_owner_builders(self):
  self.assertEqual(navigation.main_reply_keyboard()["keyboard"],[[{"text":"👤 Профіль"}]])
  self.assertEqual(navigation.profile_reply_keyboard()["keyboard"],[[{"text":"🎒 Інвентар"}],[{"text":"🔙 Назад"}]])
  labels=[b["text"] for r in navigation.shell_inline_keyboard()["inline_keyboard"] for b in r]
  self.assertEqual(labels,["Стан V2"])
 def test_removed_player_actions_absent_from_public_owners(self):
  base=Path(__file__).resolve().parents[1]
  for rel in ("rom_v2/presentation/development_shell.py","rom_v2/presentation/profile_flow.py","rom_v2/presentation/inventory_flow.py","rom_v2/app/development_bot.py"):
   source=(base/rel).read_text(encoding="utf-8");ast.parse(source)
   self.assertNotIn("Скинути персонажа",source);self.assertNotIn("За ID",source);self.assertNotIn("v2:character:reset:request",source);self.assertNotIn("v2:inventory:sort:inventory_id",source)
if __name__=="__main__":unittest.main()
