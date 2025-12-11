import os
if not os.environ.get("DEBUG") or os.environ.get("DEBUG").lower() != 'true':
    from gevent import monkey
    monkey.patch_all()
import logging
import json
import threading

from flask import Flask, request, Response, session
import flask_login
from flask_cors import CORS


class DifyApp(Flask):
    pass


config_type = os.getenv('EDITION', default='SELF_HOSTED')


