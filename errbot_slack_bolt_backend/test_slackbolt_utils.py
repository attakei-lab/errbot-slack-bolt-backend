from unittest.mock import MagicMock
from errbot_slack_bolt_backend.test_common import DummyUser, get_rate_limited_slack_response_error
from .slackbolt import Utils
import pytest
from slack_sdk.errors import SlackApiError

class Test_get_item_by_key:
    users_list = [
        DummyUser(1, 'Test 1').__dict__,
        DummyUser(2, 'Test 2').__dict__,
        DummyUser(3, 'Test 3').__dict__,
    ]

    @pytest.fixture
    def mocked_utils(self):
        return Utils()

    def test_returns_item_when_name_exists(self, mocked_utils):
        assert mocked_utils.get_item_by_key(self.users_list, 'name', 'Test 2') is not None

    def test_returns_none_when_id_does_not_exist(self, mocked_utils):
        assert mocked_utils.get_item_by_key(self.users_list, 'id', 99) is None

class Test_paginate_safely:
    @pytest.fixture
    def mocked_utils(self):
        return Utils()
    
    def test_success_when_return_all_data(self, mocked_utils):
        data = mocked_utils.paginate_safely(get_users_page)
        assert len(data)

    def test_success_with_rate_limited_error(self, mocked_utils):
        # mocked_utils.paginate_safely = 
        data = mocked_utils.paginate_safely(MagicMock(side_effect=[
            get_rate_limited_slack_response_error(),
            get_users_page(),
            get_users_page(cursor='1'),
            get_users_page(cursor='2'),
        ]))
        assert len(data)

    def test_fail_with_rate_limited_error(self, mocked_utils):
        with pytest.raises(Exception):
            mocked_utils.paginate_safely(MagicMock(side_effect=get_rate_limited_slack_response_error()))

def get_users_page(cursor=None, **kwargs):
    if cursor == None:
        return [DummyUser(1, 'Test 1').__dict__], '1'
    elif cursor == '1':
        return [DummyUser(2, 'Test 2').__dict__], '2'
    return [DummyUser(3, 'Test 3').__dict__], ''
    
