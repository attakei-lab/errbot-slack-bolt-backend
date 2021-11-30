from .slackbolt import SlackBoltBackend, Utils
from unittest.mock import MagicMock, call, patch
import pytest
from errbot.backends.base import UserDoesNotExistError
from .test_common import DummyUser, SlackBoltBackendConfig, \
    get_rate_limited_slack_response_error
from memoization import cached
from functools import update_wrapper
  
class Test_without_pagination:
    user = DummyUser(1, '@Test 1')

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks()

    def test_find_user(self, mocked_backend):
        # Calling clear_users_cache to clear the backend cache for users fetch
        mocked_backend.clear_users_cache()
        user_id = mocked_backend.username_to_userid(self.user.name)
        assert user_id is self.user.id
        assert len(mocked_backend.webclient.users_list.call_args_list) == 2
        assert mocked_backend.webclient.users_list.call_args_list[0] == call(limit=1, cursor=None)

class Test_with_pagination:
    user = DummyUser(2, '@Test 2')

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks()
    
    def mock_cached(self, method):
        return cached(user_function=method, max_size=0)

    def test_find_user(self, mocked_backend):
        mocked_backend.clear_users_cache()
        user_id = mocked_backend.username_to_userid(self.user.name)
        assert user_id is self.user.id
        assert len(mocked_backend.webclient.users_list.call_args_list) == 2
        assert mocked_backend.webclient.users_list.call_args_list[0] == call(limit=1, cursor=None)
        assert mocked_backend.webclient.users_list.call_args_list[1] == call(limit=1, cursor="1")

    def test_fails_when_user_does_not_exist(self, mocked_backend):
        mocked_backend.clear_users_cache()
        user = DummyUser(99, '@Test 99') # user not in the list
        mocked_backend.webclient.users_list = MagicMock(return_value = prepare_response([], ""))
        with pytest.raises(UserDoesNotExistError):
            mocked_backend.username_to_userid(user.name)

    def test_fail_when_rate_limited_error_raises_with_retry_after(self, mocked_backend):
        mocked_backend.clear_users_cache()
        mocked_backend.webclient.users_list = MagicMock(side_effect = get_rate_limited_slack_response_error())
        with pytest.raises(Exception):
            mocked_backend.username_to_userid(self.user.name)
        assert mocked_backend.webclient.users_list.call_count == Utils.PAGINATION_RETRY_LIMIT + 1

    def test_success_when_rate_limited_error_raises_with_retry_after(self, mocked_backend):
        mocked_backend.clear_users_cache()
        with patch('time.sleep') as sleep_mock:
            mocked_backend.webclient.users_list = MagicMock(side_effect = [get_rate_limited_slack_response_error(), get_users_list(cursor='1')])
            mocked_backend.username_to_userid(self.user.name)
            assert mocked_backend.webclient.users_list.call_count == 2
            sleep_mock.assert_called_once_with(0)
    
    def test_success_when_users_cache_exists(self, mocked_backend):
        mocked_backend.clear_users_cache()
        mocked_backend.username_to_userid(self.user.name)
        assert len(mocked_backend.webclient.users_list.call_args_list) == 2
        mocked_backend.username_to_userid(self.user.name)
        # Asserting the cached content was used instead of calling users_list again
        assert len(mocked_backend.webclient.users_list.call_args_list) == 2
    
    def test_success_when_users_cache_was_cleaned(self, mocked_backend):
        mocked_backend.clear_users_cache()
        mocked_backend.username_to_userid(self.user.name)
        assert len(mocked_backend.webclient.users_list.call_args_list) == 2
        mocked_backend.clear_users_cache()
        mocked_backend.username_to_userid(self.user.name)
        assert len(mocked_backend.webclient.users_list.call_args_list) == 4

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
    return {
        'members': users,
        'response_metadata': {
            'next_cursor': next_cursor
        }
    }

def get_users_list(**kwargs):
    if not kwargs['cursor']:
        return prepare_response([DummyUser(1, 'Test 1').__dict__], "1")
    else:
        return prepare_response([DummyUser(2, 'Test 2').__dict__], "")
