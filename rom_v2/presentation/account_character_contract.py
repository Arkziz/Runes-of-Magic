"""Pure account/character presentation contract for ROM V2.

The module maps typed application results to stable localization inputs. It has
no Telegram, persistence, SQL, V1 or runtime-registration dependency.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum
from rom_v2.application.account_service import AccountCommandResult,AccountResultStatus
from rom_v2.application.character_service import CharacterCommandResult,CharacterResultStatus

class AccountCharacterAction(StrEnum):
 REGISTER_ACCOUNT="register_account"
 CREATE_CHARACTER="create_character"
 RESET_CHARACTER="reset_character"
 RESUME_CHARACTER="resume_character"

@dataclass(frozen=True,slots=True)
class AccountCharacterView:
 action:AccountCharacterAction
 status:str
 reason:str
 localization_key:str
 account_id:str|None=None
 character_id:str|None=None
 state_key:str="registration"
 retryable:bool=False

_ACCOUNT_LOCALIZATION={
 (AccountResultStatus.CREATED,"account_created"):"account.created",
 (AccountResultStatus.ALREADY_EXISTS,"telegram_identity_exists"):"account.already_exists",
 (AccountResultStatus.REJECTED,"account_id_exists"):"account.id_exists",
}
_CHARACTER_LOCALIZATION={
 (CharacterResultStatus.CREATED,"character_created"):"character.created",
 (CharacterResultStatus.ALREADY_EXISTS,"account_character_exists"):"character.already_exists",
 (CharacterResultStatus.REJECTED,"character_id_exists"):"character.id_exists",
 (CharacterResultStatus.REJECTED,"character_name_exists"):"character.name.exists",
 (CharacterResultStatus.REJECTED,"class_key_unknown"):"character.class.unknown",
 (CharacterResultStatus.NOT_FOUND,"character_not_found"):"character.not_found",
 (CharacterResultStatus.RESET,"character_reset_requires_registration"):"character.reset.registration_required",
}

def _fallback(prefix:str,reason:str)->str:
 safe="".join(ch if ch.isalnum() or ch=="_" else "_" for ch in reason.strip().lower())
 return f"{prefix}.{safe or 'rejected'}"

def present_account_result(result:AccountCommandResult)->AccountCharacterView:
 key=_ACCOUNT_LOCALIZATION.get((result.status,result.reason),_fallback("account",result.reason))
 account_id=result.account.account_id if result.account is not None else None
 state="character_registration" if result.status in {AccountResultStatus.CREATED,AccountResultStatus.ALREADY_EXISTS} else "account_registration"
 return AccountCharacterView(AccountCharacterAction.REGISTER_ACCOUNT,result.status.value,result.reason,key,account_id=account_id,state_key=state,retryable=result.status is AccountResultStatus.REJECTED)

def present_character_result(result:CharacterCommandResult,*,action:AccountCharacterAction=AccountCharacterAction.CREATE_CHARACTER)->AccountCharacterView:
 key=_CHARACTER_LOCALIZATION.get((result.status,result.reason),_fallback("character",result.reason))
 character_id=result.character.character_id if result.character is not None else None
 if result.status in {CharacterResultStatus.CREATED,CharacterResultStatus.ALREADY_EXISTS}:state="character_ready"
 elif result.status is CharacterResultStatus.RESET:state="character_registration"
 else:state="character_registration"
 return AccountCharacterView(action,result.status.value,result.reason,key,character_id=character_id,state_key=state,retryable=result.status in {CharacterResultStatus.REJECTED,CharacterResultStatus.NOT_FOUND})

def present_restart(account_result:AccountCommandResult,character_result:CharacterCommandResult|None)->AccountCharacterView:
 if account_result.status is AccountResultStatus.REJECTED:return present_account_result(account_result)
 if character_result is None:
  return AccountCharacterView(AccountCharacterAction.RESUME_CHARACTER,"registration_required","character_not_registered","character.registration.required",account_id=account_result.account.account_id if account_result.account else None,state_key="character_registration",retryable=True)
 view=present_character_result(character_result,action=AccountCharacterAction.RESUME_CHARACTER)
 return AccountCharacterView(view.action,view.status,view.reason,view.localization_key,account_id=account_result.account.account_id if account_result.account else None,character_id=view.character_id,state_key=view.state_key,retryable=view.retryable)
