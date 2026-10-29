from __future__ import annotations
import unittest
from rom_v2.application.account_service import AccountCommandResult,AccountResultStatus
from rom_v2.application.character_service import CharacterCommandResult,CharacterResultStatus
from rom_v2.domain.account import Account
from rom_v2.domain.character import Character
from rom_v2.presentation.account_character_contract import AccountCharacterAction,present_account_result,present_character_result,present_restart

class AccountCharacterParityContractTest(unittest.TestCase):
 def setUp(self):
  self.account=Account("a",1,"2026-01-01T00:00:00Z",60)
  self.character=Character("c","a","Тест","warrior",1,0,"start_path",130,100)
 def test_happy_account_and_character_have_stable_localization_inputs(self):
  a=present_account_result(AccountCommandResult(AccountResultStatus.CREATED,"account_created",self.account))
  c=present_character_result(CharacterCommandResult(CharacterResultStatus.CREATED,"character_created",self.character))
  self.assertEqual((a.localization_key,a.state_key,a.account_id),("account.created","character_registration","a"))
  self.assertEqual((c.localization_key,c.state_key,c.character_id),("character.created","character_ready","c"))
 def test_rejection_is_typed_retryable_and_never_exposes_technical_object(self):
  view=present_character_result(CharacterCommandResult(CharacterResultStatus.REJECTED,"class_key_unknown",None))
  self.assertEqual((view.status,view.reason,view.localization_key),("rejected","class_key_unknown","character.class.unknown"))
  self.assertTrue(view.retryable);self.assertIsNone(view.character_id)
 def test_repeat_is_idempotent_ready_state(self):
  view=present_character_result(CharacterCommandResult(CharacterResultStatus.ALREADY_EXISTS,"account_character_exists",self.character))
  self.assertEqual((view.status,view.state_key,view.character_id),("already_exists","character_ready","c"));self.assertFalse(view.retryable)
 def test_stale_reset_target_is_explicit_not_found(self):
  view=present_character_result(CharacterCommandResult(CharacterResultStatus.NOT_FOUND,"character_not_found",None),action=AccountCharacterAction.RESET_CHARACTER)
  self.assertEqual((view.action,view.localization_key,view.state_key),(AccountCharacterAction.RESET_CHARACTER,"character.not_found","character_registration"));self.assertTrue(view.retryable)
 def test_restart_without_character_returns_registration_state(self):
  account=AccountCommandResult(AccountResultStatus.ALREADY_EXISTS,"telegram_identity_exists",self.account)
  view=present_restart(account,None)
  self.assertEqual((view.action,view.status,view.reason,view.localization_key,view.account_id,view.state_key),(AccountCharacterAction.RESUME_CHARACTER,"registration_required","character_not_registered","character.registration.required","a","character_registration"))
 def test_restart_with_character_returns_ready_state(self):
  account=AccountCommandResult(AccountResultStatus.ALREADY_EXISTS,"telegram_identity_exists",self.account)
  character=CharacterCommandResult(CharacterResultStatus.ALREADY_EXISTS,"account_character_exists",self.character)
  view=present_restart(account,character)
  self.assertEqual((view.action,view.character_id,view.state_key),(AccountCharacterAction.RESUME_CHARACTER,"c","character_ready"))
if __name__=="__main__":unittest.main()
