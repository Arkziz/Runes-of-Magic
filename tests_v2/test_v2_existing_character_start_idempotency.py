from __future__ import annotations
import unittest
from types import SimpleNamespace
from unittest.mock import Mock
from rom_v2.app.development_bot import DevelopmentBotConfig,IndependentDevelopmentBot
from rom_v2.application.character_service import CharacterCommandResult,CharacterResultStatus
from rom_v2.presentation.registration_flow import TelegramRegistrationFlow
class ExistingStartAcceptanceTest(unittest.TestCase):
 def update(self):return {"message":{"from":{"id":42},"chat":{"id":42},"text":"/start"}}
 def bot(self,profile,registration):
  api=SimpleNamespace(send_message=Mock());return IndependentDevelopmentBot(DevelopmentBotConfig("token",frozenset()),api=api,registration_flow=registration,profile_flow=profile),api
 def test_existing_character_start_routes_to_menu_without_registration(self):
  profile=SimpleNamespace(has_profile=Mock(return_value=True));registration=SimpleNamespace(start=Mock())
  bot,api=self.bot(profile,registration);bot.handle_update(self.update())
  registration.start.assert_not_called();profile.has_profile.assert_called_once_with(42);self.assertEqual(api.send_message.call_count,2)
  markup=api.send_message.call_args_list[-1].kwargs["reply_markup"];callbacks=[b["callback_data"] for row in markup["inline_keyboard"] for b in row];self.assertNotIn("v2:profile:root",callbacks);self.assertIn("v2:shell:status",callbacks)
 def test_missing_character_start_opens_registration(self):
  profile=SimpleNamespace(has_profile=Mock(return_value=False));view=SimpleNamespace(text="register",reply_markup={});registration=SimpleNamespace(start=Mock(return_value=view))
  bot,api=self.bot(profile,registration);bot.handle_update(self.update());registration.start.assert_called_once_with(42);self.assertEqual(api.send_message.call_args.args[1],"register")
 def test_already_exists_never_claims_new_creation(self):
  accounts=SimpleNamespace(register=Mock());existing=SimpleNamespace(name="Arkziz",class_key="rogue")
  characters=SimpleNamespace(create=Mock(return_value=CharacterCommandResult(CharacterResultStatus.ALREADY_EXISTS,"account_character_exists",existing)))
  flow=TelegramRegistrationFlow(accounts,characters);flow.start(42);flow.message(42,"Other");view=flow.callback(42,"v2:register:class:rogue")
  self.assertIn("уже існує",view.text);self.assertNotIn("створено:",view.text.casefold());self.assertEqual(view.reply_markup["inline_keyboard"][0][0]["callback_data"],"v2:shell:start")
if __name__=="__main__":unittest.main()
