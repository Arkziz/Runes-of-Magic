from __future__ import annotations
import ast,unittest
from pathlib import Path
from rom_v2.domain.inventory import InventoryAggregate
from rom_v2.domain.item import ItemInstance
class InventoryEquipmentApplicationCompletionTest(unittest.TestCase):
 def test_unique_identity_owner_and_capacity(self):
  rows=(ItemInstance(1,7,10,2,{}),ItemInstance(2,7,11,1,{}))
  bag=InventoryAggregate(7,2,rows);self.assertEqual(bag.require_instance(2).item_id,11)
  with self.assertRaises(ValueError):InventoryAggregate(7,2,(rows[0],rows[0]))
  with self.assertRaises(ValueError):InventoryAggregate(7,2,(ItemInstance(3,8,10,1,{}),))
  with self.assertRaises(OverflowError):bag.plan_addition(12,1,20)
 def test_addition_plan_is_deterministic_and_pure(self):
  row=ItemInstance(4,7,10,7,{"q":"kept"});bag=InventoryAggregate(7,3,(row,))
  plan=bag.plan_addition(10,18,10)
  self.assertEqual(plan.stack_updates,((row,10),));self.assertEqual(plan.new_stack_quantities,(10,5));self.assertEqual(row.quantity,7)
 def test_production_public_owners_are_unique(self):
  root=Path(__file__).resolve().parents[1];owners={}
  for path in (root/"rom_v2").rglob("*.py"):
   if "__pycache__" in path.parts:continue
   tree=ast.parse(path.read_text(encoding="utf-8-sig"),filename=str(path))
   for node in tree.body:
    if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and not node.name.startswith("_"):
     if node.name in {"InventoryAggregate","InventoryAdditionPlan"}:owners.setdefault(node.name,[]).append(path.relative_to(root).as_posix())
  self.assertEqual(owners,{"InventoryAdditionPlan":["rom_v2/domain/inventory.py"],"InventoryAggregate":["rom_v2/domain/inventory.py"]})
if __name__=="__main__":unittest.main()
