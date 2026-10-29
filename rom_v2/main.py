"""Executable launcher for the isolated ROM V2 development bot."""
from __future__ import annotations
import os
from pathlib import Path
from rom_v2.app.development_bot import DevelopmentBotConfig,IndependentDevelopmentBot
from rom_v2.application.account_service import AccountService
from rom_v2.application.character_service import CharacterService
from rom_v2.infrastructure.persistence import SQLiteAccountUnitOfWorkFactory,SQLiteCharacterUnitOfWorkFactory,V2ConnectionFactory,V2Migrator
from rom_v2.infrastructure.telegram.bot_api import TelegramBotApi
from rom_v2.presentation.registration_flow import TelegramRegistrationFlow

def _dotenv(path:Path)->dict[str,str]:
 values={}
 if not path.is_file():return values
 for raw in path.read_text(encoding="utf-8-sig").splitlines():
  line=raw.strip()
  if not line or line.startswith("#") or "=" not in line:continue
  key,value=line.split("=",1);values.setdefault(key.strip(),value.strip().strip('"').strip("'"))
 return values

def _allowed_ids(value:str)->frozenset[int]:
 raw=[item.strip() for item in str(value or "").split(",") if item.strip()]
 if any(not item.isdigit() for item in raw):raise ValueError("ROM_V2_ALLOWED_USER_IDS must contain comma-separated numeric IDs")
 return frozenset(int(item) for item in raw)

def build_runtime(root:Path|None=None)->IndependentDevelopmentBot:
 project=(root or Path.cwd()).resolve(); values=_dotenv(project/"rom_v2"/".env")
 token=os.environ.get("ROM_V2_BOT_TOKEN",values.get("ROM_V2_BOT_TOKEN","")).strip()
 if not token:raise RuntimeError("ROM_V2_BOT_TOKEN is missing in rom_v2/.env")
 allowed=_allowed_ids(os.environ.get("ROM_V2_ALLOWED_USER_IDS",values.get("ROM_V2_ALLOWED_USER_IDS","")))
 runtime=project/".runtime"/"rom_v2";database=runtime/"rom_v2.db"
 if not database.exists():V2Migrator(database).recreate()
 factory=V2ConnectionFactory(database,runtime_root=runtime)
 flow=TelegramRegistrationFlow(AccountService(SQLiteAccountUnitOfWorkFactory(factory)),CharacterService(SQLiteCharacterUnitOfWorkFactory(factory)))
 config=DevelopmentBotConfig(token=token,allowed_user_ids=allowed,poll_timeout_seconds=20,transport_retry_seconds=2.0)
 return IndependentDevelopmentBot(config,api=TelegramBotApi(token,timeout_seconds=35.0),registration_flow=flow)

def main()->int:
 bot=build_runtime();print("ROM V2 bot started. Press Ctrl+C to stop.")
 try:bot.run()
 except KeyboardInterrupt:bot.stop();print("ROM V2 bot stopped.")
 return 0
if __name__=="__main__":raise SystemExit(main())
