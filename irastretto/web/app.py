# -*- coding: utf-8 -*-
""":mod:'irastretto.web.app'
--- Quart application

Todo:
    * Download Queue (Modular Structure).
    * Download images from Twitter (Queue Module).
    * Caching duplicated reference.
    * Extract Zelda.
    * User login.
    * Accounts Management.
    * Download images from Pixiv (Queue Module).
    * Library interface.
    * Audio/Video Play.
    * Share Timeline.
    * Finder Extension (Another Project).
"""

from quart_openapi import Pint
from quart_cors import cors

from . import blueprints
from .. import config

app = Pint(__name__, title='Irastretto',
           template_folder='templates')
app = cors(app)
# app.config.from_object()

app.register_blueprint(blueprints.root.blueprint)
app.register_blueprint(blueprints.tasks.blueprint)
app.register_blueprint(blueprints.users.blueprint)
