from .slackbolt import SlackBoltBackend
from unittest.mock import MagicMock, call
import pytest
from errbot.backends.base import (
    RoomDoesNotExistError,
)
from .test_common import DummyChannel, SlackBoltBackendConfig

class Test_without_pagination:
    channel = DummyChannel(1, '#Test Channel 1', True)

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks()

    def test_find_channel(self, mocked_backend):
        channel_id = mocked_backend.channelname_to_channelid(self.channel.name)
        assert channel_id is self.channel.id
        assert len(mocked_backend.webclient.conversations_list.call_args_list) == 1
        assert mocked_backend.webclient.conversations_list.call_args_list[0] == call(limit=1, cursor=None, types='public_channel,private_channel')
    
    def test_get_all(self, mocked_backend):
        channels = mocked_backend.channels(mocked_backend)
        assert len(channels)

class Test_with_pagination:
    channel = DummyChannel(2, '#Test Channel 2', True)

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks()

    def test_find_channel(self, mocked_backend):
        channel_id = mocked_backend.channelname_to_channelid(self.channel.name)
        assert channel_id is self.channel.id
        assert len(mocked_backend.webclient.conversations_list.call_args_list) == 2
        assert mocked_backend.webclient.conversations_list.call_args_list[0] == call(limit=1, cursor=None, types='public_channel,private_channel')
        assert mocked_backend.webclient.conversations_list.call_args_list[1] == call(limit=1, cursor="1", types='public_channel,private_channel')

    def test_fail_find_channel(self, mocked_backend):
        enexistent_channel = DummyChannel(7001, '#Test Channel 7001', True)
        mocked_backend.webclient.users_list = MagicMock(return_value = {
            'members': [],
            'response_metadata': {
                'next_cursor': ''
            }
        })
        with pytest.raises(RoomDoesNotExistError):
            mocked_backend.channelname_to_channelid(enexistent_channel.name)

def inject_mocks():
    backend = SlackBoltBackend(SlackBoltBackendConfig())
    backend.CONVERSATIONS_PAGE_LIMIT = 1
    backend.webclient = create_web_client()
    return backend

def create_web_client():
    webclient = MagicMock()
    webclient.conversations_list = MagicMock(side_effect = conversations_list)
    return webclient

def prepare_response(data, next_cursor):
    result = dict()
    result['channels'] = data
    result['response_metadata'] = dict()
    result['response_metadata']['next_cursor'] = next_cursor
    return result

def conversations_list(**kwargs):
    if not kwargs['cursor']:
        return prepare_response([DummyChannel(1, f'Test Channel 1', True).__dict__], "1")
    else:
        return prepare_response([DummyChannel(2, f'Test Channel 2', True).__dict__], "")
