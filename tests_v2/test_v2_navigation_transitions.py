from __future__ import annotations
import unittest
from unittest.mock import Mock
from rom_v2.app.development_bot import DevelopmentBotConfig,IndependentDevelopmentBot
from rom_v2.presentation.navigation import *
class NavigationTransitionsTest(unittest.TestCase):
 def msg(self,text):return {"message":{"from":{"id":42},"chat":{"id":42},"text":text}}
 def test_profile_inventory_back_transitions(self):
  api=Mock();profile=Mock();profile.callback.return_value=Mock(text="Профіль",reply_markup={"inline_keyboard":[]});inventory=Mock();inventory.callback.return_value=Mock(text="Інвентар",reply_markup={"inline_keyboard":[]})
  bot=IndependentDevelopmentBot(DevelopmentBotConfig("token",frozenset()),api=api,profile_flow=profile,inventory_flow=inventory)
  bot.handle_update(self.msg(PROFILE_TEXT));self.assertEqual(api.send_message.call_args_list[0].kwargs["reply_markup"],profile_reply_keyboard());profile.callback.assert_called_once_with(42,PROFILE_ROOT)
  bot.handle_update(self.msg(INVENTORY_TEXT));inventory.callback.assert_called_once_with(42,INVENTORY_OPEN)
  bot.handle_update(self.msg(BACK_TEXT));self.assertEqual(api.send_message.call_args_list[-2].kwargs["reply_markup"],main_reply_keyboard())
if __name__=="__main__":unittest.main()
