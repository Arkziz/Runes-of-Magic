from __future__ import annotations
import tempfile,unittest
from pathlib import Path
from rom_v2.application.account_service import AccountResultStatus,AccountService,RegisterAccountCommand
from rom_v2.application.character_service import CharacterResultStatus,CharacterService,CreateCharacterCommand
from rom_v2.infrastructure.persistence import SQLiteAccountUnitOfWorkFactory,SQLiteCharacterUnitOfWorkFactory,V2ConnectionFactory,V2Migrator

class AccountCharacterPersistenceIntegrationTest(unittest.TestCase):
 def _clean(self,d):
  runtime=Path(d)/"runtime";db=runtime/"rom_v2.db";V2Migrator(db).recreate();factory=V2ConnectionFactory(db,runtime_root=runtime);return db,factory
 def _services(self,factory):
  return AccountService(SQLiteAccountUnitOfWorkFactory(factory)),CharacterService(SQLiteCharacterUnitOfWorkFactory(factory))
 def _commands(self):
  return RegisterAccountCommand("account-1",7001,"2026-10-29T00:00:00Z",60),CreateCharacterCommand("character-1","account-1","Тест","warrior","start_path",130,100)
 def test_create_read_repeat_and_restart_are_persistent(self):
  with tempfile.TemporaryDirectory() as d:
   db,factory=self._clean(d);accounts,characters=self._services(factory);ac,cc=self._commands()
   self.assertEqual(accounts.register(ac).status,AccountResultStatus.CREATED)
   self.assertEqual(characters.create(cc).status,CharacterResultStatus.CREATED)
   self.assertTrue(db.is_file())
   # Simulate a fresh process composition over the same clean V2 database.
   restarted_factory=V2ConnectionFactory(db,runtime_root=db.parent)
   restarted_accounts,restarted_characters=self._services(restarted_factory)
   replay_account=restarted_accounts.register(ac);replay_character=restarted_characters.create(cc)
   self.assertEqual((replay_account.status,replay_account.account.account_id),(AccountResultStatus.ALREADY_EXISTS,"account-1"))
   self.assertEqual((replay_character.status,replay_character.character.character_id),(CharacterResultStatus.ALREADY_EXISTS,"character-1"))
   c=restarted_factory.connect_read_only()
   self.assertEqual(c.execute("SELECT COUNT(*) FROM accounts").fetchone()[0],1)
   self.assertEqual(c.execute("SELECT COUNT(*) FROM crystal_wallets").fetchone()[0],1)
   self.assertEqual(c.execute("SELECT COUNT(*) FROM characters").fetchone()[0],1)
   row=c.execute("SELECT account_id,name,class_key,location_key,current_hp,current_mp FROM characters WHERE character_id=?",("character-1",)).fetchone();c.close()
   self.assertEqual(tuple(row),("account-1","Тест","warrior","start_path",130,100))
 def test_account_wallet_creation_is_atomic_on_repository_failure(self):
  with tempfile.TemporaryDirectory() as d:
   _,factory=self._clean(d)
   with self.assertRaises(Exception):
    with SQLiteAccountUnitOfWorkFactory(factory)() as unit:
     from rom_v2.domain.account import Account
     unit.accounts.add(Account("atomic",8001,"2026-10-29T00:00:00Z",60))
     unit.accounts.create_crystal_wallet("missing-parent")
     unit.commit()
   c=factory.connect_read_only();self.assertEqual(c.execute("SELECT COUNT(*) FROM accounts WHERE account_id='atomic'").fetchone()[0],0);c.close()
 def test_character_creation_rolls_back_without_commit(self):
  with tempfile.TemporaryDirectory() as d:
   _,factory=self._clean(d);accounts,_=self._services(factory);ac,_=self._commands();accounts.register(ac)
   with SQLiteCharacterUnitOfWorkFactory(factory)() as unit:
    from rom_v2.domain.character import Character
    unit.characters.add(Character("rollback","account-1","Відкат","warrior",1,0,"start_path",130,100))
   c=factory.connect_read_only();self.assertEqual(c.execute("SELECT COUNT(*) FROM characters WHERE character_id='rollback'").fetchone()[0],0);c.close()
if __name__=="__main__":unittest.main()
