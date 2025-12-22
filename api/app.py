import os

if not os.environ.get("DEBUG") or os.environ.get("DEBUG").lower() != 'true':
    from gevent import monkey
    monkey.patch_all()
import json
import logging
import threading

import flask_login
from flask import Flask, Response, request, session
from flask_cors import CORS

from config import CloudEditionConfig, Config
from extensions import (ext_celery, ext_database, ext_login, ext_migrate,
                        ext_redis, ext_sentry, ext_session, ext_storage,
                        ext_vector_store)
from extensions.ext_database import db
from extensions.ext_login import login_manager
from models import account, dataset, model, provider, task, web


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
