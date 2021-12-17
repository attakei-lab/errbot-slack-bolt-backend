from .slackbolt import SlackBoltBackend, SlackRoomOccupant, SlackPerson, SlackRoom
from unittest.mock import MagicMock
import pytest
from .test_common import DummyChannel, SlackBoltBackendConfig, DummyUser

name = 'My Name'
email = 'user@email.com'
username = 'myusername'
userid = 'Uxxx'
channelname = 'My Channel'
channelid = 'Cccc'

class Test_build_identifier:
    
    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks()
    
    @pytest.fixture
    def mocked_backend_with_user(self):
        backend = inject_mocks()
        backend.extract_identifiers_from_string = MagicMock(return_value=(name, None, None, None))
        backend.get_im_channel = MagicMock(return_value = channelid)
        return backend
    
    @pytest.fixture
    def mocked_backend_with_room(self):
        backend = inject_mocks()
        backend.extract_identifiers_from_string = MagicMock(return_value=(None, None, channelname, None))
        return backend
    
    def test_slack_room_occupant(self, mocked_backend):
        slack_room_occupant = mocked_backend.build_identifier('')
        assert isinstance(slack_room_occupant, SlackRoomOccupant)
        assert userid == slack_room_occupant.userid
        assert channelid == slack_room_occupant.channelid
    
    def test_slack_person(self, mocked_backend_with_user):
        slack_person = mocked_backend_with_user.build_identifier('')
        assert isinstance(slack_person, SlackPerson)
        assert userid == slack_person.userid
        assert name == slack_person.username
        assert channelid == slack_person.channelid
        assert email == slack_person.email
    
    def test_slack_room(self, mocked_backend_with_room):
        slack_room = mocked_backend_with_room.build_identifier('')
        assert isinstance(slack_room, SlackRoom)
        assert channelid == slack_room.id

def inject_mocks():
    backend = SlackBoltBackend(SlackBoltBackendConfig())
    backend.CONVERSATIONS_PAGE_LIMIT = 1
    backend.webclient = create_web_client()
    backend.extract_identifiers_from_string = MagicMock(return_value=(name, userid, channelname, channelid))
    return backend

def create_web_client():
    webclient = MagicMock()
    webclient.conversations_list = MagicMock(side_effect = get_conversations_list)
    webclient.users_list = MagicMock(side_effect = get_users_list)
    return webclient

def prepare_channels_response(data, next_cursor):
    return {
        'channels': data,
        'response_metadata': {
            'next_cursor': next_cursor
        }
    }
def prepare_members_response(data, next_cursor):
    return {
        'members': data,
        'response_metadata': {
            'next_cursor': next_cursor
        }
    }

def get_conversations_list(**kwargs):
    if not kwargs['cursor']:
        return prepare_channels_response([DummyChannel(channelid, channelname, True).__dict__], "1")
    else:
        return prepare_channels_response([DummyChannel('Cddd', 'My Channel 2', True).__dict__], "")

def get_users_list(**kwargs):
    if not kwargs['cursor']:
        return prepare_members_response([DummyUser(userid, name, {'email': email}).__dict__], "1")
    else:
        return prepare_members_response([DummyUser('Uyyy', 'My Name 2').__dict__], "")

