import os

from slack_sdk.errors import SlackApiError
from slack_sdk.web.slack_response import SlackResponse

class DummyUser:
    def __init__(self, id, name, profile={}, deleted=False):
        self.id = id
        self.name = name
        self.profile = profile
        self.deleted = deleted

class DummyChannel:
    def __init__(self, id, name, is_member, is_archived=False, is_private=False):
        self.id = id
        self.name = name
        self.is_member = is_member
        self.is_archived = is_archived
        self.is_private = is_private

class SlackBoltBackendConfig:
    def __init__(self):
        self.BOT_PREFIX = 'SLACK_BOLT_BACKEND_TEST'
        self.BOT_ASYNC = True
        # self.BOT_ASYNC_POOLSIZE = 1024
        self.BOT_ASYNC_POOLSIZE = 64
        self.BOT_ALT_PREFIX_CASEINSENSITIVE = True
        self.BOT_ALT_PREFIXES = ['slack_bolt']
        self.MESSAGE_SIZE_LIMIT = 1024
        self.BOT_IDENTITY = {
            'bot_token': os.environ.get('SLACK_BOT_TOKEN'),
            'app_token': os.environ.get('SLACK_APP_TOKEN')
        }
        self.ACCESS_FORM_BOT_INFO = {
            "bot_id": None,
            "nickname": os.environ.get("SDM_ACCESS_FORM_BOT_NICKNAME")
        }

def get_rate_limited_slack_response_error():
    return SlackApiError('ratelimited', SlackResponse(
        data={'ok': False,'error': 'ratelimited'},
        client=None,
        headers={'retry-after': '0'},
        req_args=None,
        api_url="",
        http_verb="",
        status_code=400
    ))
