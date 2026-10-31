import ast,unittest
from types import SimpleNamespace
from rom_v2.presentation.inventory_flow import TelegramInventoryEquipmentFlow,PAGE_SIZE,DEFAULT_SORT,ALLOWED_SORT_KEYS
class S:
 def __init__(self,rows=()):self.rows=rows
 def list_inventory(self,u):return SimpleNamespace(instances=tuple(self.rows))
class E:
 def list_slots(self,u):return SimpleNamespace(status="ok",slots=())
 def equip(self,*a):return SimpleNamespace(status="ok",reason=None)
 def unequip(self,*a):return SimpleNamespace(status="ok",reason=None)
class P:
 def get_by_telegram_user_id(self,u):return SimpleNamespace(level=10,class_key="warrior")
class TelegramInventoryEquipmentSliceTest(unittest.TestCase):
 def test_contract_constants_are_single(self):self.assertEqual(PAGE_SIZE,8);self.assertEqual(DEFAULT_SORT,"inventory_id");self.assertEqual(ALLOWED_SORT_KEYS,("inventory_id","item_id","quantity"))
 def test_empty_inventory_and_stale_identity_fail_closed(self):
  f=TelegramInventoryEquipmentFlow(S(),E(),P());self.assertIn("Інвентар",f.callback(7,"v2:inventory:open").text);self.assertIn("більше не доступний",f.callback(7,"v2:inventory:item:999").text)
 def test_no_sql_or_policy_duplication(self):
  import rom_v2.presentation.inventory_flow as m
  from pathlib import Path
  src=Path(m.__file__).read_text(encoding="utf-8").lower();self.assertNotIn("select ",src);self.assertNotIn("execute(",src)
if __name__=="__main__":unittest.main()
