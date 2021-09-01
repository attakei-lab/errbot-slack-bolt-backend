from .slackbolt import SlackBoltBackend
from unittest.mock import MagicMock
import pytest
from errbot.backends.base import (
    UserDoesNotExistError
)
from .test_common import DummyUser, paginate, SlackBoltBackendConfig
  
class Test_without_pagination:
    user = DummyUser(1, '@Test 1')

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks()

    def test_find_user(self, mocked_backend):
        user_id = mocked_backend.username_to_userid(self.user.name)
        assert user_id is self.user.id

class Test_with_pagination:
    user = DummyUser(101, '@Test 101')

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks(users_page_limit = 100)

    def test_find_user(self, mocked_backend):
        user_id = mocked_backend.username_to_userid(self.user.name)
        assert user_id is self.user.id

    def test_fail_when_user_does_not_exist(self, mocked_backend):
        user = DummyUser(7000, '@Test 7000')
        with pytest.raises(UserDoesNotExistError):
            mocked_backend.username_to_userid(user.name)

def get_5k_users():
    return [DummyUser(index, f'Test {index}').__dict__ for index in range(5000)]

def inject_mocks(users_page_limit = 10000, users = get_5k_users()):
    backend = SlackBoltBackend(SlackBoltBackendConfig())
    backend.USERS_PAGE_LIMIT = users_page_limit
    backend.webclient = create_web_client(users)
    return backend

def create_web_client(users):
    webclient = MagicMock()
    webclient.users_list = get_users_list_fn(users)
    return webclient

def prepare_response(users, next_cursor):
    result = dict()
    result['members'] = users
    result['response_metadata'] = dict()
    result['response_metadata']['next_cursor'] = next_cursor
    return result

def get_users_list_fn(_users):
    def get_users_list(limit = 10000, cursor = None):
        cursor = int(cursor) if cursor and len(cursor) > 0 else 0
        page_users, next_cursor = paginate(_users, limit, cursor)
        return prepare_response(page_users, next_cursor)
    return get_users_list
