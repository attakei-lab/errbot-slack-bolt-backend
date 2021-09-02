from .slackbolt import SlackBoltBackend
from unittest.mock import MagicMock
import pytest
from errbot.backends.base import (
    RoomDoesNotExistError,
)
from .test_common import DummyChannel, paginate, SlackBoltBackendConfig

class Test_without_pagination:
    channel = DummyChannel(1, '#Test Channel 1', True)

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks()

    def test_find_channel(self, mocked_backend):
        channel_id = mocked_backend.channelname_to_channelid(self.channel.name)
        assert channel_id is self.channel.id
    
    def test_get_all(self, mocked_backend):
        channels = mocked_backend.channels(mocked_backend)
        assert len(channels)

class Test_with_pagination:
    channel = DummyChannel(101, '#Test Channel 101', True)

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks(conversations_pag_limit = 10)

    def test_find_channel(self, mocked_backend):
        channel_id = mocked_backend.channelname_to_channelid(self.channel.name)
        assert channel_id is self.channel.id
    
    def test_fail_find_channel(self, mocked_backend):
        enexistent_channel = DummyChannel(7001, '#Test Channel 7001', True)
        with pytest.raises(RoomDoesNotExistError):
            mocked_backend.channelname_to_channelid(enexistent_channel.name)

def get_5k_channels():
    return [
        DummyChannel(index + 1, f'Test Channel {index + 1}', True if index % 2 == 0 else False).__dict__
        for index in range(5000)
    ]

def inject_mocks(conversations_pag_limit = 10000, channels = get_5k_channels()):
    backend = SlackBoltBackend(SlackBoltBackendConfig())
    backend.CONVERSATIONS_PAGE_LIMIT = conversations_pag_limit
    backend.webclient = create_web_client(channels)
    return backend

def create_web_client(channels):
    webclient = MagicMock()
    webclient.conversations_list = conversations_list_fn(channels)
    return webclient

def prepare_response(data, next_cursor):
    result = dict()
    result['channels'] = data
    result['response_metadata'] = dict()
    result['response_metadata']['next_cursor'] = next_cursor
    return result

def conversations_list_fn(_channels):
    def conversations_list(limit = 1000, cursor = None, **kwargs):
        cursor = int(cursor) if cursor and len(cursor) > 0 else 0
        channels = _channels
        channels, next_cursor = paginate(channels, limit, cursor)
        result = prepare_response(channels, next_cursor)
        return result
    return conversations_list
