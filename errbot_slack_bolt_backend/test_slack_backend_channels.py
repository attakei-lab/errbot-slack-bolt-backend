from .slackbolt import SlackBoltBackend
from unittest.mock import MagicMock
import pytest
from errbot.backends.base import (
    RoomDoesNotExistError,
)
from .test_utils import DummyChannel, paginate, get_item_by_key_test, \
    get_webclient_mock_config

class TestFindChannelByName:
    channel = DummyChannel(1, '#Test Channel 1')

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks()

    def test_find_channel(self, mocked_backend):
        channel_id = mocked_backend.channelname_to_channelid(mocked_backend, self.channel.name)
        assert channel_id is self.channel.id

class TestFindChannelByNameWPagination:
    channel = DummyChannel(101, '#Test Channel 101')

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks(conversations_pag_limit = 10)

    def test_find_channel(self, mocked_backend):
        channel_id = mocked_backend.channelname_to_channelid(mocked_backend, self.channel.name)
        assert channel_id is self.channel.id

class TestNotFindChannelByName:
    channel = DummyChannel(1, '#Test Channel 1')

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks(return_zero_channels = True)

    def test_not_find_channel(self, mocked_backend):
        try:
            mocked_backend.channelname_to_channelid(mocked_backend, self.channel.name)
            assert False
        except:
            assert True

class TestFetchChannels:
    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks()

    def test_not_find_channel(self, mocked_backend):
        channels = mocked_backend.channels(mocked_backend)
        assert len(channels) > 0

def inject_mocks(conversations_pag_limit = 10000, return_zero_channels = False):
    backend = SlackBoltBackend(get_webclient_mock_config())
    backend.CONVERSATIONS_PAG_LIMIT = conversations_pag_limit
    backend.webclient = create_web_client(return_zero_channels)
    backend.channelname_to_channelid = channelname_to_channelid
    backend.channels = channels
    return backend

def create_web_client(return_zero_channels = False):
    webclient = MagicMock()
    if return_zero_channels:
        webclient.conversations_list = MagicMock(return_value = prepare_response(list(), ""))
    else:
        webclient.conversations_list = get_conversations
    return webclient

def prepare_response(data, next_cursor):
    result = dict()
    result['channels'] = data
    result['response_metadata'] = dict()
    if len(next_cursor) and int(next_cursor) > 0:
        result['response_metadata']['next_cursor'] = next_cursor
    else:
        result['response_metadata']['next_cursor'] = ""
    return result

def get_conversations(limit = 1000, cursor = None, **kwargs):
    cursor = int(cursor) if cursor and len(cursor) > 0 else 0
    channels = get_mock_channels()
    channels, next_cursor = paginate(channels, limit, cursor)
    result = prepare_response(channels, next_cursor)
    return result

def channelname_to_channelid(backend, name):
    name = name.lstrip("#")
    channel = find_conversation_by_name(backend, name, types = "public_channel,private_channel", limit = backend.CONVERSATIONS_PAGE_LIMIT)
    if not channel:
        raise RoomDoesNotExistError(f"No channel named {name} exists")
    return channel["id"]

def find_conversation_by_name(backend, name, **kwargs):
    channels, next_cursor = index_conversations(backend, **kwargs)
    channel = get_item_by_key_test(channels, 'name', name)
    while len(next_cursor) and channel is None:
        channels, next_cursor = index_conversations(backend, cursor = next_cursor, **kwargs)
        channel = get_item_by_key_test(channels, 'name', name)
    return channel

def index_conversations(backend, **kwargs):
    response = backend.webclient.conversations_list(**kwargs)
    channels = response['channels']
    next_cursor = response['response_metadata']['next_cursor']
    return channels, next_cursor

def get_mock_channels():
    channels = list()
    for index in range(5000):
        channels.append(DummyChannel(index + 1, f'Test Channel {index + 1}').__dict__)
    return channels

def channels(backend):
    channels = fetch_conversations(backend, limit = backend.CONVERSATIONS_PAGE_LIMIT)

    return channels

def fetch_conversations(backend, **kwargs):
    channels, next_cursor = index_conversations(backend, **kwargs)
    while len(next_cursor):
        next_channels, next_cursor = index_conversations(backend, cursor = next_cursor, **kwargs)
        channels.extend(next_channels)
    return channels

