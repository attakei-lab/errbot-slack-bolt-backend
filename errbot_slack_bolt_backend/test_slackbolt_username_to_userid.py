from .slackbolt import SlackBoltBackend
from unittest.mock import MagicMock, call
import pytest
from errbot.backends.base import (
    UserDoesNotExistError
)
from .test_common import DummyUser, SlackBoltBackendConfig
  
class Test_without_pagination:
    user = DummyUser(1, '@Test 1')

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks()

    def test_find_user(self, mocked_backend):
        user_id = mocked_backend.username_to_userid(self.user.name)
        assert user_id is self.user.id
        assert len(mocked_backend.webclient.users_list.call_args_list) == 1
        assert mocked_backend.webclient.users_list.call_args_list[0] == call(limit=1, cursor=None)

class Test_with_pagination:
    user = DummyUser(2, '@Test 2')

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks()

    def test_find_user(self, mocked_backend):
        user_id = mocked_backend.username_to_userid(self.user.name)
        assert user_id is self.user.id
        assert len(mocked_backend.webclient.users_list.call_args_list) == 2
        assert mocked_backend.webclient.users_list.call_args_list[0] == call(limit=1, cursor=None)
        assert mocked_backend.webclient.users_list.call_args_list[1] == call(limit=1, cursor="1")

    def test_fail_when_user_does_not_exist(self, mocked_backend):
        user = DummyUser(99, '@Test 99') # user not in the list
        mocked_backend.webclient.users_list = MagicMock(return_value = {
            'members': [],
            'response_metadata': {
                'next_cursor': ''
            }
        })
        with pytest.raises(UserDoesNotExistError):
            mocked_backend.username_to_userid(user.name)

def inject_mocks():
    backend = SlackBoltBackend(SlackBoltBackendConfig())
    backend.USERS_PAGE_LIMIT = 1
    backend.webclient = create_web_client()
    return backend

def create_web_client():
    webclient = MagicMock()
    webclient.users_list = MagicMock(side_effect = get_users_list)
    return webclient

def prepare_response(users, next_cursor):
    result = dict()
    result['members'] = users
    result['response_metadata'] = dict()
    result['response_metadata']['next_cursor'] = next_cursor
    return result

def get_users_list(**kwargs):
    if not kwargs['cursor']:
        return prepare_response([DummyUser(1, 'Test 1').__dict__], "1")
    else:
        return prepare_response([DummyUser(2, 'Test 2').__dict__], "")
