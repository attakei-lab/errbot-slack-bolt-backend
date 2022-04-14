from .slackbolt import SlackBoltBackend
from unittest.mock import MagicMock
import pytest
from .test_common import SlackBoltBackendConfig

bot_id = '123'

class Test_resolve_access_form_bot_id:
    @pytest.fixture
    def mocked_backend(self):
        return inject_mocks()

    def test_resolve_access_form_bot_id(self, mocked_backend):
        mocked_backend.username_to_bot_id = MagicMock(return_value=bot_id)
        mocked_backend.resolve_access_form_bot_id()
        assert mocked_backend.bot_config.ACCESS_FORM_BOT_INFO.get('bot_id') == bot_id 

def inject_mocks():
    backend = SlackBoltBackend(SlackBoltBackendConfig())
    return backend
