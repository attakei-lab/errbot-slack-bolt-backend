import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from errbot_slack_bolt_backend import get_plugin_dir


ROOT = Path(__file__).parent

load_dotenv(ROOT / '.env', override=True)

BACKEND = 'SlackBolt'
BOT_EXTRA_BACKEND_DIR = str(get_plugin_dir())

BOT_DATA_DIR = str(ROOT / 'data')

BOT_EXTRA_PLUGIN_DIR = str(ROOT / 'plugins')

BOT_LOG_FILE = str(ROOT / 'errbot.log')
BOT_LOG_LEVEL = logging.DEBUG

BOT_ADMINS = ('@CHANGE_ME', )

BOT_IDENTITY = {
    "app_token": os.environ["SLACK_APP_TOKEN"],
    "bot_token": os.environ["SLACK_BOT_TOKEN"],
    "bot_userid": os.environ["SLACK_BOT_USERID"],
}
