"""Read-only profile identity query composed from canonical account/character ports."""
from __future__ import annotations
from dataclasses import dataclass
from rom_v2.application.account_ports import AccountUnitOfWorkFactoryPort
from rom_v2.application.character_ports import CharacterUnitOfWorkFactoryPort
@dataclass(frozen=True,slots=True)
class ProfileSummary:
 character_id:str;name:str;class_key:str;level:int;current_hp:int;current_mp:int|None
class ProfileQueryService:
 def __init__(self,accounts:AccountUnitOfWorkFactoryPort,characters:CharacterUnitOfWorkFactoryPort)->None:self._accounts=accounts;self._characters=characters
 def by_telegram_user_id(self,telegram_user_id:int)->ProfileSummary|None:
  if int(telegram_user_id)<=0:return None
  with self._accounts() as unit:
   account=unit.accounts.find_by_telegram_user_id(int(telegram_user_id))
  if account is None:return None
  with self._characters() as unit:
   character=unit.characters.find_by_account_id(account.account_id)
  if character is None:return None
  return ProfileSummary(character.character_id,character.name,character.class_key,character.level,character.current_hp,character.current_mp)
