"""Pure immutable presentation models for the ROM V2 profile section."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class ProfileSummaryView:
 name:str
 class_label:str
 level:int
 current_hp:int
 current_mp:int|None

def present_summary(model:ProfileSummaryView)->str:
 mp="—" if model.current_mp is None else str(model.current_mp)
 return "\n".join((f"Профіль: {model.name}",f"Клас: {model.class_label}",f"Рівень: {model.level}",f"HP: {model.current_hp}",f"MP: {mp}"))

@dataclass(frozen=True,slots=True)
class ProfileIdentityView:
 name:str
 class_label:str
 level:int

@dataclass(frozen=True,slots=True)
class ProfilePrimaryStatsView:
 strength:int
 dexterity:int
 intelligence:int
 wisdom:int
 stamina:int
 free_points:int=0

@dataclass(frozen=True,slots=True)
class ProfileDerivedStatsView:
 physical_attack:int
 magical_attack:int
 physical_defense:int
 magical_defense:int
 physical_crit:float
 magical_crit:float
 dodge:float

@dataclass(frozen=True,slots=True)
class ProfileResourcesView:
 current_hp:int
 max_hp:int
 current_mp:int|None
 max_mp:int|None

@dataclass(frozen=True,slots=True)
class ProfileViewModel:
 identity:ProfileIdentityView
 primary:ProfilePrimaryStatsView
 derived:ProfileDerivedStatsView
 resources:ProfileResourcesView
 equipment_lines:tuple[str,...]=()
 skill_lines:tuple[str,...]=()

def _resource(current:int|None,maximum:int|None)->str:
 return "—" if current is None or maximum is None else f"{current}/{maximum}"

def present_overview(model:ProfileViewModel)->str:
 i=model.identity;r=model.resources
 return "\n".join((f"Профіль: {i.name}",f"Клас: {i.class_label}",f"Рівень: {i.level}",f"HP: {_resource(r.current_hp,r.max_hp)}",f"MP: {_resource(r.current_mp,r.max_mp)}"))

def present_stats(model:ProfileViewModel)->str:
 p=model.primary;d=model.derived
 return "\n".join(("Параметри",f"Сила: {p.strength}",f"Спритність: {p.dexterity}",f"Інтелект: {p.intelligence}",f"Мудрість: {p.wisdom}",f"Витривалість: {p.stamina}",f"Вільні очки: {p.free_points}","",f"Фізична атака: {d.physical_attack}",f"Магічна атака: {d.magical_attack}",f"Фізичний захист: {d.physical_defense}",f"Магічний захист: {d.magical_defense}",f"Фіз. крит: {d.physical_crit:.2f}%",f"Маг. крит: {d.magical_crit:.2f}%",f"Ухилення: {d.dodge:.2f}%"))

def present_equipment(model:ProfileViewModel)->str:
 return "Екіпірування\n"+("\n".join(model.equipment_lines) if model.equipment_lines else "Немає екіпірованих предметів.")

def present_skills(model:ProfileViewModel)->str:
 return "Навички\n"+("\n".join(model.skill_lines) if model.skill_lines else "Немає доступних навичок.")
