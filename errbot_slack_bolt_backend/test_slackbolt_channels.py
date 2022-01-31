from .slackbolt import SlackBoltBackend, Utils
from unittest.mock import MagicMock, call, patch
import pytest
from errbot.backends.base import RoomDoesNotExistError
from .test_common import DummyChannel, SlackBoltBackendConfig, \
    get_rate_limited_slack_response_error

class Test_channels:
    channel = DummyChannel(1, '#Test Channel 1', True)

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks()
    
    def test_returns_all_channels(self, mocked_backend):
        mocked_backend.clear_conversations_cache()
        channels = mocked_backend.channels()
        assert len(channels) == 2
        assert len(mocked_backend.webclient.conversations_list.call_args_list) == 2
        assert mocked_backend.webclient.conversations_list.call_args_list[0] == call(limit=1, types="public_channel,private_channel", cursor=None, exclude_archived=True)
        assert mocked_backend.webclient.conversations_list.call_args_list[1] == call(limit=1, types="public_channel,private_channel", cursor="1", exclude_archived=True)
        assert channels[0] == DummyChannel(1, 'Test Channel 1', True).__dict__
        assert channels[1] == DummyChannel(2, 'Test PV Channel 1', True, is_private=True).__dict__
    
    def test_returns_only_public_channels(self, mocked_backend):
        mocked_backend.clear_conversations_cache()
        channels = mocked_backend.channels(types='public_channel')
        assert len(channels) == 1
        assert len(mocked_backend.webclient.conversations_list.call_args_list) == 1
        assert mocked_backend.webclient.conversations_list.call_args_list[0] == call(limit=1, types="public_channel", cursor=None, exclude_archived=True)
        assert channels[0] == DummyChannel(1, 'Test Channel 1', True).__dict__

class Test_channelname_to_channelid:
    channel = DummyChannel(2, '#Test PV Channel 1', True, is_private=True)

    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks()

    def test_returns_channelid_when_channelname_exists(self, mocked_backend):
        mocked_backend.clear_conversations_cache()
        channel_id = mocked_backend.channelname_to_channelid(self.channel.name)
        assert channel_id is self.channel.id
        assert len(mocked_backend.webclient.conversations_list.call_args_list) == 2
        assert mocked_backend.webclient.conversations_list.call_args_list[0] == call(limit=1, cursor=None, types='public_channel,private_channel')
        assert mocked_backend.webclient.conversations_list.call_args_list[1] == call(limit=1, cursor="1", types='public_channel,private_channel')

    def test_fail_when_channel_does_not_exist(self, mocked_backend):
        mocked_backend.clear_conversations_cache()
        nonexistent_channel = DummyChannel(7001, '#Test Channel 7001', True)
        mocked_backend.webclient.users_list = MagicMock(return_value = prepare_response([], ""))
        with pytest.raises(RoomDoesNotExistError):
            mocked_backend.channelname_to_channelid(nonexistent_channel.name)

    def test_fail_when_rate_limited_error_raises_with_retry_after(self, mocked_backend):
        mocked_backend.clear_conversations_cache()
        mocked_backend.webclient.conversations_list = MagicMock(side_effect = get_rate_limited_slack_response_error())
        with pytest.raises(Exception):
            mocked_backend.channelname_to_channelid(self.channel.name)        
        assert mocked_backend.webclient.conversations_list.call_count == Utils.PAGINATION_RETRY_LIMIT + 1
    
    def test_success_when_rate_limited_error_raises_with_retry_after(self, mocked_backend):
        mocked_backend.clear_conversations_cache()
        with patch('time.sleep') as sleep_mock:
            mocked_backend.webclient.conversations_list = MagicMock(side_effect = [get_rate_limited_slack_response_error(), conversations_list(cursor='1', types='public_channel,private_channel')])
            mocked_backend.channelname_to_channelid(self.channel.name)
            assert mocked_backend.webclient.conversations_list.call_count == 2
            sleep_mock.assert_called_once_with(0)

    def test_success_when_conversations_cache_exists(self, mocked_backend):
        mocked_backend.clear_conversations_cache()
        mocked_backend.channelname_to_channelid(self.channel.name)
        assert len(mocked_backend.webclient.conversations_list.call_args_list) == 2
        mocked_backend.channelname_to_channelid(self.channel.name)
        # Asserting the cached content was used instead of calling conversations_list again
        assert len(mocked_backend.webclient.conversations_list.call_args_list) == 2

    def test_success_when_conversations_cache_was_cleaned(self, mocked_backend):
        mocked_backend.clear_conversations_cache()
        mocked_backend.channelname_to_channelid(self.channel.name)
        assert len(mocked_backend.webclient.conversations_list.call_args_list) == 2
        mocked_backend.clear_conversations_cache()
        mocked_backend.channelname_to_channelid(self.channel.name)
        assert len(mocked_backend.webclient.conversations_list.call_args_list) == 4
        
    def test_private_channel_not_present_when_fetching_only_public(self, mocked_backend):
        mocked_backend.clear_conversations_cache()
        with pytest.raises(RoomDoesNotExistError):
            mocked_backend.channelname_to_channelid(self.channel.name, types='public_channel')

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
    return {
        'channels': data,
        'response_metadata': {
            'next_cursor': next_cursor
        }
    }

def conversations_list(**kwargs):
    consider_private_channels = kwargs.get('types') and 'private_channel' in kwargs.get('types')
    if not kwargs['cursor']:
        return prepare_response([DummyChannel(1, 'Test Channel 1', True).__dict__], "1" if consider_private_channels else "")
    else:
        return prepare_response([DummyChannel(2, 'Test PV Channel 1', True, is_private=True).__dict__], "")

