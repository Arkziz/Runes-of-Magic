from __future__ import annotations
import sqlite3,tempfile,unittest
from pathlib import Path
from rom_v2.application.account_service import AccountService,RegisterAccountCommand
from rom_v2.application.character_service import CharacterService,CreateCharacterCommand
from rom_v2.application.profile_query_service import ProfileQueryService
from rom_v2.infrastructure.persistence import SQLiteAccountUnitOfWorkFactory,SQLiteCharacterUnitOfWorkFactory,V2ConnectionFactory,V2Migrator
from rom_v2.presentation.character_reset_flow import TelegramCharacterResetFlow
class ResetAcceptanceTest(unittest.TestCase):
 def runtime(self,root):
  db=root/"rom_v2.db";V2Migrator(db).recreate();factory=V2ConnectionFactory(db,runtime_root=root);af=SQLiteAccountUnitOfWorkFactory(factory);cf=SQLiteCharacterUnitOfWorkFactory(factory)
  accounts=AccountService(af);characters=CharacterService(cf);query=ProfileQueryService(af,cf)
  accounts.register(RegisterAccountCommand("a1",42,"2026-01-01T00:00:00Z",60));characters.create(CreateCharacterCommand("c1","a1","Arkziz","rogue","start_path",130,100))
  return db,query,characters
 def counts(self,db):
  connection=sqlite3.connect(db)
  try:return connection.execute("select count(*) from accounts").fetchone()[0],connection.execute("select count(*) from characters").fetchone()[0]
  finally:connection.close()
 def test_cancel_is_non_mutating_and_confirm_preserves_account(self):
  with tempfile.TemporaryDirectory() as d:
   db,query,characters=self.runtime(Path(d));flow=TelegramCharacterResetFlow(query,characters)
   flow.callback(42,flow.REQUEST);flow.callback(42,flow.CANCEL);self.assertEqual(self.counts(db),(1,1))
   flow.callback(42,flow.REQUEST);view=flow.callback(42,flow.CONFIRM);self.assertEqual(self.counts(db),(1,0));self.assertIn("Обліковий запис збережено",view.text);self.assertIsNone(query.by_telegram_user_id(42))
 def test_stale_confirmation_fails_closed(self):
  with tempfile.TemporaryDirectory() as d:
   db,query,characters=self.runtime(Path(d));flow=TelegramCharacterResetFlow(query,characters);view=flow.callback(42,flow.CONFIRM)
   self.assertIn("застаріло",view.text);self.assertEqual(self.counts(db),(1,1))
if __name__=="__main__":unittest.main()
