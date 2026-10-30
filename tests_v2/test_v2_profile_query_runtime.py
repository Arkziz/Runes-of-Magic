from __future__ import annotations
import unittest
from types import SimpleNamespace
from unittest.mock import Mock
from rom_v2.application.profile_query_service import ProfileQueryService
from rom_v2.presentation.profile_flow import TelegramProfileFlow
class Uow:
 def __init__(self,repo,name):setattr(self,name,repo)
 def __enter__(self):return self
 def __exit__(self,*args):return False
class ProfileRuntimeTest(unittest.TestCase):
 def test_query_and_flow_use_persisted_identity(self):
  accounts=SimpleNamespace(find_by_telegram_user_id=Mock(return_value=SimpleNamespace(account_id="a1")))
  chars=SimpleNamespace(find_by_account_id=Mock(return_value=SimpleNamespace(character_id="c1",name="Олег",class_key="warrior",level=2,current_hp=90,current_mp=None)))
  query=ProfileQueryService(lambda:Uow(accounts,"accounts"),lambda:Uow(chars,"characters"));view=TelegramProfileFlow(query).open(42)
  self.assertIn("Олег",view.text);self.assertIn("HP: 90",view.text);accounts.find_by_telegram_user_id.assert_called_once_with(42)
 def test_missing_profile_fails_closed(self):
  accounts=SimpleNamespace(find_by_telegram_user_id=Mock(return_value=None));flow=TelegramProfileFlow(ProfileQueryService(lambda:Uow(accounts,"accounts"),lambda:None))
  self.assertIn("створіть персонажа",flow.open(42).text);self.assertIsNone(flow.callback(42,"unknown"))
if __name__=="__main__":unittest.main()
