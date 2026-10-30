"""Explicit confirmation flow for destructive V2 character reset."""
from __future__ import annotations
from rom_v2.application.character_service import CharacterResultStatus,CharacterService,ResetCharacterCommand
from rom_v2.application.profile_query_service import ProfileQueryService
from rom_v2.presentation.development_shell import ShellView
class TelegramCharacterResetFlow:
 REQUEST="v2:character:reset:request";CONFIRM="v2:character:reset:confirm";CANCEL="v2:character:reset:cancel"
 def __init__(self,query:ProfileQueryService,characters:CharacterService)->None:self._query=query;self._characters=characters;self._pending:set[int]=set()
 def callback(self,user_id:int,data:str)->ShellView|None:
  if data==self.REQUEST:
   record=self._query.by_telegram_user_id(user_id)
   if record is None:return ShellView("Персонажа для скидання не знайдено.",{"inline_keyboard":[[{"text":"Назад","callback_data":"v2:shell:start"}]]})
   self._pending.add(user_id)
   return ShellView(f"Скинути персонажа {record.name}? Цю дію не можна скасувати.",{"inline_keyboard":[[{"text":"Підтвердити","callback_data":self.CONFIRM}],[{"text":"Скасувати","callback_data":self.CANCEL}]]})
  if data==self.CANCEL:
   self._pending.discard(user_id)
   return ShellView("Скидання персонажа скасовано.",{"inline_keyboard":[[{"text":"До профілю","callback_data":"v2:profile:root"}]]})
  if data!=self.CONFIRM:return None
  if user_id not in self._pending:return ShellView("Підтвердження застаріло. Персонажа не змінено.",{"inline_keyboard":[[{"text":"Назад","callback_data":"v2:shell:start"}]]})
  self._pending.discard(user_id);record=self._query.by_telegram_user_id(user_id)
  if record is None:return ShellView("Персонажа вже немає. Обліковий запис збережено.",{"inline_keyboard":[[{"text":"Створити персонажа","callback_data":"v2:register:start"}]]})
  result=self._characters.reset(ResetCharacterCommand(record.character_id))
  if result.status is not CharacterResultStatus.RESET:return ShellView("Не вдалося скинути персонажа. Дані не змінено.",{"inline_keyboard":[[{"text":"Назад","callback_data":"v2:profile:root"}]]})
  return ShellView("Персонажа скинуто. Обліковий запис збережено. Тепер можна створити нового персонажа.",{"inline_keyboard":[[{"text":"Створити персонажа","callback_data":"v2:register:start"}]]})
