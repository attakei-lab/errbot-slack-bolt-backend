from .slackbolt import SlackBoltBackend
from unittest.mock import MagicMock, call
import pytest
from .test_common import SlackBoltBackendConfig

userid = '123'

class Test_find_user_profile:
    wrong_userid = 'xxx'

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks()

    def test_find_profile(self, mocked_backend):
        profile = mocked_backend.find_user_profile(userid)
        assert profile
        assert len(mocked_backend.webclient.users_profile_get.call_args_list) == 1
        assert mocked_backend.webclient.users_profile_get.call_args_list[0] == call(user=userid, include_labels=True)

    def test_not_find_profile(self, mocked_backend):
        profile = mocked_backend.find_user_profile(self.wrong_userid)
        assert profile is None
        assert len(mocked_backend.webclient.users_profile_get.call_args_list) == 1
        assert mocked_backend.webclient.users_profile_get.call_args_list[0] == call(user=self.wrong_userid, include_labels=True)

def inject_mocks():
    backend = SlackBoltBackend(SlackBoltBackendConfig())
    backend.CONVERSATIONS_PAGE_LIMIT = 1
    backend.webclient = create_web_client()
    return backend

def create_web_client():
    webclient = MagicMock()
    webclient.users_profile_get = MagicMock(side_effect = get_user_profile_response)
    return webclient

def get_user_profile_response(user, include_labels):
    response = dict()
    response['ok'] = True
    if user == userid:
        response['profile'] = MagicMock()
    else:
        response['profile'] = None
    return response
