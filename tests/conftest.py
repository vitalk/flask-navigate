#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from flask import Flask
from flask_navigator import Navigator


@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route('/')
    def ping():
        return 'pong'

    return app
