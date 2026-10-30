"""Telegram-independent profile flow over the canonical read-only query."""
from __future__ import annotations
from rom_v2.application.profile_query_service import ProfileQueryService
from rom_v2.domain.class_catalog import DEFAULT_CLASS_CATALOG
from rom_v2.presentation.development_shell import ShellView
from rom_v2.presentation.profile_presenter import ProfileSummaryView,present_summary
class TelegramProfileFlow:
 def __init__(self,query:ProfileQueryService)->None:self._query=query
 def open(self,user_id:int)->ShellView:
  record=self._query.by_telegram_user_id(user_id)
  if record is None:return ShellView("Профіль ще недоступний. Спочатку створіть персонажа через /start.",{"inline_keyboard":[[{"text":"Назад","callback_data":"v2:shell:start"}]]})
  definition=DEFAULT_CLASS_CATALOG.find(record.class_key);label=definition.display_name if definition else record.class_key
  view=ProfileSummaryView(record.name,label,record.level,record.current_hp,record.current_mp)
  return ShellView(present_summary(view),{"inline_keyboard":[[{"text":"Назад","callback_data":"v2:shell:start"}]]})
 def callback(self,user_id:int,data:str)->ShellView|None:return self.open(user_id) if data=="v2:profile:root" else None
