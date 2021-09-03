import os

class DummyUser:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class DummyChannel:
    def __init__(self, id, name, is_member):
        self.id = id
        self.name = name
        self.is_member = is_member

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
