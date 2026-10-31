"""Canonical pure V2 Telegram navigation labels and markup builders."""
from __future__ import annotations
from collections.abc import Iterable
PROFILE_TEXT="👤 Профіль"
INVENTORY_TEXT="🎒 Інвентар"
BACK_TEXT="🔙 Назад"
SHELL_START="v2:shell:start"
SHELL_STATUS="v2:shell:status"
PROFILE_ROOT="v2:profile:root"
INVENTORY_OPEN="v2:inventory:open"
EQUIPMENT_OPEN="v2:equipment:open"
def button(text:str,callback_data:str)->dict[str,str]:return {"text":text,"callback_data":callback_data}
def reply_keyboard(rows:Iterable[Iterable[str]])->dict:
 return {"keyboard":[[{"text":text} for text in row] for row in rows],"resize_keyboard":True,"is_persistent":True}
def main_reply_keyboard()->dict:return reply_keyboard(((PROFILE_TEXT,),))
def profile_reply_keyboard()->dict:return reply_keyboard(((INVENTORY_TEXT,),(BACK_TEXT,)))
def shell_inline_keyboard()->dict:return {"inline_keyboard":[[button("Стан V2",SHELL_STATUS)]]}
def empty_inline_keyboard()->dict:return {"inline_keyboard":[]}
def back_to_main_inline_keyboard()->dict:return {"inline_keyboard":[[button("Назад",SHELL_START)]]}
def inventory_inline_rows(item_rows:list[list[dict]],pagination:list[dict]|None=None)->dict:
 rows=list(item_rows)
 if pagination:rows.append(pagination)
 rows.append([button("Екіпірування",EQUIPMENT_OPEN)])
 return {"inline_keyboard":rows}
def equipment_back_row()->list[dict]:return [button("До інвентарю",INVENTORY_OPEN)]
