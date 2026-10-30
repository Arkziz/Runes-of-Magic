from __future__ import annotations
import ast,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
from rom_v2.domain.class_catalog import DEFAULT_CLASS_CATALOG
from rom_v2.presentation.registration_flow import TelegramRegistrationFlow
class RegistrationClassCatalogParityTest(unittest.TestCase):
 def flow(self,character=None):
  accounts=SimpleNamespace(register=Mock(return_value=SimpleNamespace(account=SimpleNamespace(account_id="a1"))))
  characters=SimpleNamespace(create=Mock(return_value=SimpleNamespace(character=character,reason="",status=None)))
  return TelegramRegistrationFlow(accounts,characters)
 def test_registration_buttons_use_all_canonical_display_names(self):
  flow=self.flow();flow.start(42);view=flow.message(42,"Oleh")
  buttons=[row[0] for row in view.reply_markup["inline_keyboard"][:-1]]
  expected=[(item.display_name,f"v2:register:class:{item.key}") for item in DEFAULT_CLASS_CATALOG.all()]
  self.assertEqual([(button["text"],button["callback_data"]) for button in buttons],expected)
  self.assertIn(("🏹 Скаут","v2:register:class:scout"),expected)
 def test_creation_result_uses_canonical_display_name(self):
  character=SimpleNamespace(name="Oleh",class_key="scout");flow=self.flow(character);flow.start(42);flow.message(42,"Oleh")
  view=flow.callback(42,"v2:register:class:scout")
  self.assertIn("🏹 Скаут",view.text);self.assertNotIn("Розвідник",view.text)
 def test_registration_module_has_no_parallel_six_class_label_catalog(self):
  root=Path(__file__).resolve().parents[1];path=root/"rom_v2"/"presentation"/"registration_flow.py";source=path.read_text(encoding="utf-8");tree=ast.parse(source)
  self.assertNotIn("CLASS_LABELS",source)
  keys={"warrior","knight","scout","rogue","mage","priest"}
  for node in ast.walk(tree):
   if isinstance(node,ast.Dict):
    found={item.value for item in node.keys if isinstance(item,ast.Constant) and isinstance(item.value,str)}
    self.assertFalse(keys.issubset(found),"parallel class display catalog is forbidden")
if __name__=="__main__":unittest.main()
