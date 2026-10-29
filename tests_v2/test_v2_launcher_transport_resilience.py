from __future__ import annotations
import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from rom_v2.app.development_bot import DevelopmentBotConfig,IndependentDevelopmentBot
from rom_v2.infrastructure.telegram.bot_api import TelegramApiResponse,TelegramTransportError
from rom_v2.main import _allowed_ids,build_runtime
class RetryApi:
 def __init__(self):self.calls=0;self.bot=None
 def get_updates(self,*,offset=None,timeout=20):
  self.calls+=1
  if self.calls==1:raise TelegramTransportError("network timeout")
  self.bot.stop();return TelegramApiResponse(ok=True,result=[])
class LauncherTransportTest(unittest.TestCase):
 def test_empty_allowlist_is_supported_and_numeric_values_parse(self):
  self.assertEqual(_allowed_ids(""),frozenset());self.assertEqual(_allowed_ids("1, 2"),frozenset({1,2}))
  with self.assertRaises(ValueError):_allowed_ids("name")
 def test_transport_error_retries_instead_of_terminating(self):
  api=RetryApi();bot=IndependentDevelopmentBot(DevelopmentBotConfig("token",frozenset(),poll_timeout_seconds=0,transport_retry_seconds=0),api=api);api.bot=bot
  with patch("rom_v2.app.development_bot.sleep",lambda _:None):bot.run()
  self.assertEqual(api.calls,2)
 def test_launcher_uses_persistent_isolated_db_and_no_required_allowlist(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/"rom_v2").mkdir();(root/"rom_v2"/".env").write_text("ROM_V2_BOT_TOKEN=123:test-token\n",encoding="utf-8")
   bot=build_runtime(root);db=root/".runtime"/"rom_v2"/"rom_v2.db";self.assertTrue(db.is_file());self.assertEqual(bot._config.allowed_user_ids,frozenset())
if __name__=="__main__":unittest.main()
