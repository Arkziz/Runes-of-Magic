from __future__ import annotations
import os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from rom_v2.app.runtime_launcher import build_runtime
class InventoryEquipmentUowRuntimeWiringTest(unittest.TestCase):
 def test_isolated_runtime_inventory_and_equipment_services_open_real_uows(self):
  with tempfile.TemporaryDirectory() as temp,patch.dict(os.environ,{"ROM_V2_BOT_TOKEN":"test-token","ROM_V2_ALLOWED_USER_IDS":""},clear=False):
   root=Path(temp);bot=build_runtime(root)
   inventory=bot._inventory_flow._inventory.list_inventory(4242)
   equipment=bot._inventory_flow._equipment.list_slots(4242)
   self.assertEqual(inventory.status,"ok");self.assertEqual(inventory.instances,())
   self.assertEqual(equipment.status,"ok");self.assertEqual(equipment.slots,())
   self.assertTrue((root/".runtime"/"rom_v2"/"rom_v2.db").is_file())
 def test_runtime_passes_connect_read_write_to_both_uow_factories(self):
  import rom_v2.app.runtime_launcher as module
  source=Path(module.__file__).read_text(encoding="utf-8")
  self.assertIn("SQLiteInventoryUnitOfWorkFactory(factory.connect_read_write)",source)
  self.assertIn("SQLiteEquipmentUnitOfWorkFactory(factory.connect_read_write)",source)
  self.assertNotIn("SQLiteInventoryUnitOfWorkFactory(factory)",source)
  self.assertNotIn("SQLiteEquipmentUnitOfWorkFactory(factory)",source)
if __name__=="__main__":unittest.main()
