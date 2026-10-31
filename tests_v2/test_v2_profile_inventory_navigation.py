from __future__ import annotations
import unittest
from unittest.mock import Mock
from rom_v2.app.development_bot import DevelopmentBotConfig,IndependentDevelopmentBot
class NavigationCorrectionTest(unittest.TestCase):
 def _message(self,text):return {"message":{"from":{"id":42},"chat":{"id":42},"text":text}}
 def test_profile_text_switches_keyboard_and_delegates_to_profile_owner(self):
  api=Mock();profile=Mock();profile.callback.return_value=Mock(text="Профіль",reply_markup={"inline_keyboard":[]})
  bot=IndependentDevelopmentBot(DevelopmentBotConfig("token",frozenset()),api=api,profile_flow=profile)
  bot.handle_update(self._message("👤 Профіль"));profile.callback.assert_called_once_with(42,"v2:profile:root")
  self.assertEqual(api.send_message.call_args_list[0].kwargs["reply_markup"]["keyboard"],[[{"text":"🎒 Інвентар"}],[{"text":"🔙 Назад"}]])
 def test_back_restores_persistent_profile_button(self):
  api=Mock();bot=IndependentDevelopmentBot(DevelopmentBotConfig("token",frozenset()),api=api)
  bot.handle_update(self._message("🔙 Назад"));self.assertEqual(api.send_message.call_args_list[0].kwargs["reply_markup"]["keyboard"],[[{"text":"👤 Профіль"}]])
 def test_inventory_uses_canonical_profile_query_api(self):
  from pathlib import Path
  import rom_v2.presentation.inventory_flow as module
  source=Path(module.__file__).read_text(encoding="utf-8")
  self.assertIn(".by_telegram_user_id(user_id)",source);self.assertNotIn(".get_by_telegram_user_id(user_id)",source)
if __name__=="__main__":unittest.main()
