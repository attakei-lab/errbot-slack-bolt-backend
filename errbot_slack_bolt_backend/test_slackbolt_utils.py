from errbot_slack_bolt_backend.test_common import DummyUser
from .slackbolt import Utils
import pytest

class Test_get_item_by_key:
    users_list = [
        DummyUser(1, 'Test 1').__dict__,
        DummyUser(2, 'Test 2').__dict__,
        DummyUser(3, 'Test 3').__dict__
    ]

    @pytest.fixture
    def mocked_utils(self):
        return Utils()
    
    def test_returns_item_when_name_exists(self, mocked_utils):
        assert mocked_utils.get_item_by_key(self.users_list, 'name', 'Test 2') is not None
    
    def test_returns_none_when_id_does_not_exist(self, mocked_utils):
        assert mocked_utils.get_item_by_key(self.users_list, 'id', 99) is None