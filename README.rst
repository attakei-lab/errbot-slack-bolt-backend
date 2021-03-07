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

Configure subscrived events
---------------------------

* ``message.im``

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

#. Copy ``errbot_slack_bolt_backend/slackbolt.py`` and ``errbot_slack_bolt_backend/slackbolt.plug`` from GitHub to some directory. 
#. Set directory path to ``BOT_EXTRA_BACKEND_DIR`` of your ``config.py``.

Post install
------------

(TBD)

Implementations
===============

This does not yet implement all features of built-in Slack/SlackRTM backend.

License
=======

Apache 2.0
