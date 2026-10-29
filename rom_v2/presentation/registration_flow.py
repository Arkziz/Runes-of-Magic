"""Framework-neutral V2 Telegram character-registration wizard."""
from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum
from uuid import uuid5, NAMESPACE_URL
from rom_v2.application.account_service import AccountService, RegisterAccountCommand
from rom_v2.application.character_service import CharacterService, CreateCharacterCommand
from rom_v2.presentation.development_shell import ShellView

CLASS_LABELS = {"warrior":"Воїн","knight":"Лицар","scout":"Розвідник","rogue":"Розбійник","mage":"Маг","priest":"Жрець"}
class RegistrationStep(StrEnum): NAME="name"; CLASS="class"
@dataclass(slots=True)
class RegistrationSession:
    account_id: str
    name: str | None = None
    step: RegistrationStep = RegistrationStep.NAME

    def accept_name(self, value: str) -> None:
        self.name = value
        self.step = RegistrationStep.CLASS

    def reset_name(self) -> None:
        self.name = None
        self.step = RegistrationStep.NAME
class TelegramRegistrationFlow:
    def __init__(self, accounts: AccountService, characters: CharacterService) -> None:
        self._accounts=accounts; self._characters=characters; self._sessions:dict[int,RegistrationSession]={}
    def _account_id(self,user_id:int)->str: return str(uuid5(NAMESPACE_URL,f"rom-v2:telegram:{user_id}"))
    def _character_id(self,user_id:int)->str: return str(uuid5(NAMESPACE_URL,f"rom-v2:character:{user_id}"))
    def start(self,user_id:int)->ShellView:
        aid=self._account_id(user_id); self._accounts.register(RegisterAccountCommand(aid,user_id,"2026-01-01T00:00:00Z",60)); self._sessions[user_id]=RegistrationSession(aid)
        return ShellView("Створення персонажа ROM V2\n\nВведіть ім’я персонажа (2–24 символи).",{"inline_keyboard":[[{"text":"Скасувати","callback_data":"v2:register:cancel"}]]})
    def message(self,user_id:int,text:str)->ShellView|None:
        s=self._sessions.get(user_id)
        if s is None or s.step is not RegistrationStep.NAME: return None
        name = str(text or "").strip()
        if not name: return ShellView("Ім’я не може бути порожнім.",{"inline_keyboard":[]})
        s.accept_name(name)
        buttons=[[{"text":label,"callback_data":f"v2:register:class:{key}"}] for key,label in CLASS_LABELS.items()]
        buttons.append([{"text":"Назад","callback_data":"v2:register:back"},{"text":"Скасувати","callback_data":"v2:register:cancel"}])
        return ShellView("Оберіть клас персонажа.",{"inline_keyboard":buttons})
    def callback(self,user_id:int,data:str)->ShellView|None:
        s=self._sessions.get(user_id)
        if data=="v2:register:start": return self.start(user_id)
        if data=="v2:register:cancel": self._sessions.pop(user_id,None); return ShellView("Створення персонажа скасовано.",{"inline_keyboard":[]})
        if s is None: return None
        if data=="v2:register:back":
            s.reset_name()
            return ShellView("Введіть ім’я персонажа.",{"inline_keyboard":[]})
        prefix="v2:register:class:"
        if not data.startswith(prefix): return None
        key=data[len(prefix):]
        if key not in CLASS_LABELS: return ShellView("Невідомий клас. Оберіть клас зі списку.",{"inline_keyboard":[]})
        result=self._characters.create(CreateCharacterCommand(self._character_id(user_id),s.account_id,s.name or "",key,"start_path",130,100))
        if result.character is None:
            s.reset_name()
            return ShellView(f"Не вдалося створити персонажа ({result.reason}). Введіть ім’я ще раз.",{"inline_keyboard":[]})
        self._sessions.pop(user_id,None)
        return ShellView(f"Персонажа створено: {result.character.name}\nКлас: {CLASS_LABELS[result.character.class_key]}",{"inline_keyboard":[[{"text":"До меню","callback_data":"v2:shell:start"}]]})
