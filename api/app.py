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
from extensions import ext_session, ext_celery, ext_sentry, ext_redis, ext_login, ext_vector_store, ext_migrate, \
    ext_database, ext_storage
from extensions.ext_database import db
from extensions.ext_login import login_manager

from config import Config, CloudEditionConfig

from models import model, account, provider, task, web


class DifyApp(Flask):
    pass


config_type = os.getenv('EDITION', default='SELF_HOSTED')


def initialize_extensions(app):
    ext_database.init_app(app)
    ext_migrate.init(app, db)


def create_app(test_config=None) -> Flask:
    app = DifyApp(__name__)

    if test_config:
        app.config.from_object(test_config)
    else:
        if config_type == "CLOUD":
            app.config.from_object(CloudEditionConfig())
        else:
            app.config.from_object(Config())

    app.secret_key = app.config['SECRET_KEY']
    logging.basicConfig(level=app.config.get('LOG_LEVEL', 'INFO'))
    initialize_extensions(app)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
