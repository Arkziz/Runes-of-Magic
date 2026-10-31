"""Single Telegram presentation owner for inventory and equipment."""
from __future__ import annotations
from rom_v2.domain.equipment import EquipmentItemPolicy,SLOT_KEYS
from rom_v2.presentation.development_shell import ShellView
PAGE_SIZE=8
DEFAULT_SORT="inventory_id"
ALLOWED_SORT_KEYS=("inventory_id","item_id","quantity")
SLOT_LABELS={"main_hand":"Основна рука","off_hand":"Друга рука","helmet":"Шолом","shoulders":"Плечі","chest":"Нагрудник","gloves":"Рукавиці","legs":"Штани","boots":"Взуття","necklace":"Намисто","ring":"Перстень"}
class TelegramInventoryEquipmentFlow:
 def __init__(self,inventory_service,equipment_service,profile_query):self._inventory=inventory_service;self._equipment=equipment_service;self._profile=profile_query
 def _character(self,user_id):return self._profile.get_by_telegram_user_id(user_id)
 @staticmethod
 def _button(text,data):return {"text":text,"callback_data":data}
 def _list(self,user_id,page=0,sort_key=DEFAULT_SORT):
  if not self._character(user_id):return ShellView("Персонажа не знайдено.",{"inline_keyboard":[[self._button("Назад","v2:shell:start")]]})
  result=self._inventory.list_inventory(user_id);rows=list(result.instances)
  key=sort_key if sort_key in ALLOWED_SORT_KEYS else DEFAULT_SORT
  rows.sort(key=lambda x:(getattr(x,key),x.inventory_id))
  pages=max(1,(len(rows)+PAGE_SIZE-1)//PAGE_SIZE);page=max(0,min(int(page),pages-1));shown=rows[page*PAGE_SIZE:(page+1)*PAGE_SIZE]
  text=[f"Інвентар • сторінка {page+1}/{pages}"]+[f"ID {x.inventory_id} • предмет {x.item_id} • x{x.quantity}" for x in shown]
  keys=[[self._button(f"Предмет {x.item_id} ×{x.quantity}",f"v2:inventory:item:{x.inventory_id}")] for x in shown]
  nav=[]
  if page:nav.append(self._button("Назад",f"v2:inventory:page:{page-1}"))
  if page+1<pages:nav.append(self._button("Далі",f"v2:inventory:page:{page+1}"))
  if nav:keys.append(nav)
  keys.append([self._button("Екіпірування","v2:equipment:open"),self._button("За ID","v2:inventory:sort:inventory_id")])
  return ShellView("\n".join(text),{"inline_keyboard":keys})
 def _details(self,user_id,inventory_id):
  result=self._inventory.list_inventory(user_id);item=next((x for x in result.instances if x.inventory_id==inventory_id),None)
  if item is None:return ShellView("Предмет більше не доступний.",{"inline_keyboard":[[self._button("До інвентарю","v2:inventory:open")]]})
  meta=dict(item.metadata);slot=str(meta.get("slot_key","") or "")
  keys=[]
  if slot in SLOT_KEYS:keys.append([self._button("Вдягнути",f"v2:equipment:equip:{item.inventory_id}")])
  keys.append([self._button("До інвентарю","v2:inventory:open")])
  return ShellView(f"Предмет {item.item_id}\nInventory ID: {item.inventory_id}\nКількість: {item.quantity}",{"inline_keyboard":keys})
 def _equipment_view(self,user_id,notice=None):
  result=self._equipment.list_slots(user_id);by={x.slot_key:x.inventory_id for x in result.slots};lines=["Екіпірування"]
  keys=[]
  if notice:lines.append(notice)
  for slot in SLOT_KEYS:
   value=by.get(slot);lines.append(f"{SLOT_LABELS[slot]}: {value if value else 'порожньо'}")
   if value:keys.append([self._button(f"Зняти: {SLOT_LABELS[slot]}",f"v2:equipment:unequip:{slot}")])
  keys.append([self._button("Інвентар","v2:inventory:open")]);return ShellView("\n".join(lines),{"inline_keyboard":keys})
 def _equip(self,user_id,inventory_id):
  character=self._character(user_id);result=self._inventory.list_inventory(user_id);item=next((x for x in result.instances if x.inventory_id==inventory_id),None)
  if character is None or item is None:return self._equipment_view(user_id,"Дію відхилено: предмет недоступний.")
  m=dict(item.metadata);slot=str(m.get("slot_key","") or "")
  try:policy=EquipmentItemPolicy(item.inventory_id,user_id,slot,int(m.get("required_level",1)),tuple(m.get("allowed_classes",()) or ()),int(m.get("weapon_hands",1)),int(m.get("durability",100)))
  except (TypeError,ValueError):return self._equipment_view(user_id,"Дію відхилено: предмет не має коректної політики екіпірування.")
  outcome=self._equipment.equip(policy,character.level,character.class_key);return self._equipment_view(user_id,"Готово." if outcome.status=="ok" else f"Дію відхилено: {outcome.reason}.")
 def callback(self,user_id,data):
  value=str(data or '')
  if value=='v2:inventory:open':return self._list(user_id)
  if value.startswith('v2:inventory:page:'):
   try:return self._list(user_id,int(value.rsplit(':',1)[1]))
   except ValueError:return self._list(user_id)
  if value.startswith('v2:inventory:sort:'):return self._list(user_id,0,value.rsplit(':',1)[1])
  if value.startswith('v2:inventory:item:'):
   try:return self._details(user_id,int(value.rsplit(':',1)[1]))
   except ValueError:return self._list(user_id)
  if value=='v2:equipment:open':return self._equipment_view(user_id)
  if value.startswith('v2:equipment:equip:'):
   try:return self._equip(user_id,int(value.rsplit(':',1)[1]))
   except ValueError:return self._equipment_view(user_id,"Некоректна дія.")
  if value.startswith('v2:equipment:unequip:'):
   slot=value.rsplit(':',1)[1];outcome=self._equipment.unequip(user_id,slot);return self._equipment_view(user_id,"Готово." if outcome.status=="ok" else f"Дію відхилено: {outcome.reason}.")
  return None
