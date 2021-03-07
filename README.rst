=========================
errbot-slack-bolt-backend
=========================

.. note::
    
   This package is experimental.
   It is not guaranteed for running correctly and updating future.

Overview
========

This is ErrBot backend-plugin for Slack App (not legacy and classic bot) by Slack Bolt.

Pre-requirements
================

This need Slack application in App Directory.

Configure bot scopes
--------------------

* ``chat:write``
* ``im:history``
* ``users:read``
* ``channels:read``

Configure subscrived events
---------------------------

* ``message.im``
* ``message.channels``

Installation
============

As python packege
-----------------

#. Run ``pip install --extra-index-url https://pypi.attakei.net/simple/ errbot-slack-bolt-backend``
#. | Import function to get plugin directory from ``errbot_slack_bolt_backend``.
   | example: ``from errbot_slack_bolt_backend import get_plugin_dir``
#. | Set directory path to ``BOT_EXTRA_BACKEND_DIR`` of your ``config.py``.
   | example: ``BOT_EXTRA_BACKEND_DIR = str(get_plugin_dir())``

As plain source coude
---------------------

#. | Clone repository into your workspace from GitHub.
   | example: ``git clone https://github.com/attakei-lab/errbot-slack-bolt-backend.git``
#. | Set directory path to ``BOT_EXTRA_BACKEND_DIR`` of your ``config.py``.
   | example: ``BOT_EXTRA_BACKEND_DIR = 'errbot-slack-bolt-backend/errbot_slack_bolt_backend'``

Post install
------------

Set configuration to your ``config.py``.

.. code-block:: python

   BACKEND = "SlackBolt"
   BOT_IDENTITY = {
       # Required
       "app_token": "YOUR-APP-LEVEL-TOKEN",
       "bot_token": "YOUR-BOT-USER-TOKEN",
   }

Implementations
===============

This does not yet implement all features of built-in Slack/SlackRTM backend.

- Response of direct message
- Response of post in joined channels

License
=======

Apache 2.0
