from __future__ import annotations
import tempfile, unittest
from pathlib import Path
from rom_v2.application.account_service import AccountService
from rom_v2.application.character_service import CharacterService
from rom_v2.infrastructure.persistence import SQLiteAccountUnitOfWorkFactory, SQLiteCharacterUnitOfWorkFactory, V2ConnectionFactory, V2Migrator
from rom_v2.presentation.registration_flow import TelegramRegistrationFlow
class TelegramRegistrationFlowTest(unittest.TestCase):
    def _flow(self,d):
        root=Path(d)/"runtime"; db=root/"rom_v2.db"; V2Migrator(db).recreate(); f=V2ConnectionFactory(db,runtime_root=root)
        return f,TelegramRegistrationFlow(AccountService(SQLiteAccountUnitOfWorkFactory(f)),CharacterService(SQLiteCharacterUnitOfWorkFactory(f)))
    def test_complete_repeat_back_cancel(self):
        with tempfile.TemporaryDirectory() as d:
            f,flow=self._flow(d); self.assertIn("Введіть",flow.start(77).text); self.assertIn("Оберіть",flow.message(77,"Тест").text); self.assertIn("створено",flow.callback(77,"v2:register:class:warrior").text)
            flow.start(77); flow.message(77,"Інший"); self.assertIn("Тест",flow.callback(77,"v2:register:class:mage").text)
            c=f.connect_read_only(); self.assertEqual(c.execute("SELECT COUNT(*) FROM accounts").fetchone()[0],1); self.assertEqual(c.execute("SELECT COUNT(*) FROM characters").fetchone()[0],1); c.close()
            flow.start(88); flow.message(88,"Тест2"); self.assertIn("Введіть",flow.callback(88,"v2:register:back").text); self.assertIn("скасовано",flow.callback(88,"v2:register:cancel").text)
if __name__=="__main__": unittest.main()
