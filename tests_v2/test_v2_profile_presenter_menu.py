from __future__ import annotations
import unittest
from unittest.mock import Mock
from rom_v2.infrastructure.telegram.bot_api import TelegramApiResponse,TelegramBotApi
from rom_v2.presentation.profile_menu import ProfileMenu,ProfileRoute
from rom_v2.presentation.profile_presenter import *
class ProfilePresentationTest(unittest.TestCase):
 def model(self):return ProfileViewModel(ProfileIdentityView("Олег","Воїн",7),ProfilePrimaryStatsView(10,11,12,13,14,3),ProfileDerivedStatsView(20,21,22,23,4.5,5.5,6.5),ProfileResourcesView(80,100,None,None),("Меч",),("Удар",))
 def test_pure_presenter_and_menu(self):
  menu=ProfileMenu();root=menu.root(self.model());self.assertIn("Профіль: Олег",root.text);self.assertIn("MP: —",root.text)
  self.assertIn("Фізична атака: 20",menu.route(ProfileRoute.STATS,self.model()).text)
  self.assertIn("Меч",menu.route(ProfileRoute.EQUIPMENT,self.model()).text);self.assertIsNone(menu.route("unknown",self.model()))
 def test_callback_ack_transport_contract(self):
  api=object.__new__(TelegramBotApi);api.call=Mock(return_value=TelegramApiResponse(True,True,None))
  result=api.answer_callback_query("abc");api.call.assert_called_once_with("answerCallbackQuery",{"callback_query_id":"abc"});self.assertTrue(result.ok)
 def test_models_are_immutable(self):
  with self.assertRaises(Exception):self.model().identity.level=8
if __name__=="__main__":unittest.main()
