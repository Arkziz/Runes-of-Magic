"""Profile section routes and menus, independent of Telegram transport."""
from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum
from rom_v2.presentation.development_shell import ShellView
from rom_v2.presentation.profile_presenter import ProfileViewModel,present_equipment,present_overview,present_skills,present_stats
class ProfileRoute(StrEnum):ROOT="v2:profile:root";STATS="v2:profile:stats";EQUIPMENT="v2:profile:equipment";SKILLS="v2:profile:skills";BACK="v2:shell:start"
@dataclass(frozen=True,slots=True)
class ProfileMenu:
 def root(self,model:ProfileViewModel)->ShellView:return ShellView(present_overview(model),{"inline_keyboard":[[{"text":"Параметри","callback_data":ProfileRoute.STATS},{"text":"Екіпірування","callback_data":ProfileRoute.EQUIPMENT}],[{"text":"Навички","callback_data":ProfileRoute.SKILLS}],[{"text":"Назад","callback_data":ProfileRoute.BACK}]]})
 def route(self,route:str,model:ProfileViewModel)->ShellView|None:
  if route==ProfileRoute.ROOT:return self.root(model)
  text={ProfileRoute.STATS:present_stats,ProfileRoute.EQUIPMENT:present_equipment,ProfileRoute.SKILLS:present_skills}.get(route)
  return None if text is None else ShellView(text(model),{"inline_keyboard":[[{"text":"До профілю","callback_data":ProfileRoute.ROOT},{"text":"Назад","callback_data":ProfileRoute.BACK}]]})
