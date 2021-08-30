from unittest.mock import MagicMock
import pytest
from errbot.backends.base import (
    UserDoesNotExistError,
    UserNotUniqueError,
)
from .test_utils import DummyUser, paginate, get_item_by_key_test

class TestFindUserByUsername:
    user = DummyUser(1, '@Test 1')

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks()

    def test_find_user(self, mocked_backend):
        user_id = mocked_backend.username_to_userid(mocked_backend, self.user.name)
        assert user_id is self.user.id

class TestFindUserByUsernameWPagination:
    user = DummyUser(1, '@Test 1')

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks(users_pag_limit = 100)

    def test_find_user(self, mocked_backend):
        user_id = mocked_backend.username_to_userid(mocked_backend, self.user.name)
        assert user_id is self.user.id

class TestFindUserByUsernameFail:
    user = DummyUser(1, '@Test 1')

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks(return_zero_users = True)

    def test_find_user(self, mocked_backend):
        try:
            mocked_backend.username_to_userid(mocked_backend, self.user.name)
            assert False
        except UserDoesNotExistError:
            assert True

def inject_mocks(users_pag_limit = 10000, return_zero_users = False):
    backend = MagicMock()
    backend.USERS_PAG_LIMIT = users_pag_limit
    backend.webclient = create_web_client(return_zero_users)
    backend.username_to_userid = username_to_userid
    return backend

def create_web_client(return_zero_users = False):
    webclient = MagicMock()
    if return_zero_users:
        webclient.users_list = MagicMock(return_value = prepare_response(list(), ""))
    else:
        webclient.users_list = get_users
    return webclient

def get_users(limit = 10000, cursor = None):
    cursor = int(cursor) if cursor and len(cursor) > 0 else 0
    users = get_mock_users()
    users, next_cursor = paginate(users, limit, cursor)
    result = prepare_response(users, next_cursor)
    return result

def prepare_response(users, next_cursor):
    result = dict()
    result['members'] = users
    result['response_metadata'] = dict()
    if len(next_cursor) and int(next_cursor) > 0:
        result['response_metadata']['next_cursor'] = next_cursor
    else:
        result['response_metadata']['next_cursor'] = ""
    return result

def username_to_userid(backend, name):
    name = name.lstrip("@")
    user = find_user_by_name(backend, name)
    if not user:
        raise UserDoesNotExistError(f"Cannot find user {name}.")
    if user and isinstance(user, list) and len(user) > 1:
        raise UserNotUniqueError(f"Failed to uniquely identify {name}.")
    return user["id"]

def find_user_by_name(backend, name):
    members, next_cursor = index_users(backend, limit = backend.USERS_PAG_LIMIT)
    user = get_item_by_key_test(members, 'name', name)
    while len(next_cursor) and user is None:
        members, next_cursor = index_users(backend, limit = backend.USERS_PAG_LIMIT, cursor = next_cursor)
        user = get_item_by_key_test(members, 'name', name)
    return user

def index_users(backend, **kwargs):
    response = backend.webclient.users_list(**kwargs)
    members = response['members']
    next_cursor = response['response_metadata']['next_cursor']
    return members, next_cursor

def get_mock_users():
    users = list()
    for index in range(1, 5000):
        users.append(DummyUser(index, f'Test {index}').__dict__)
    return users
