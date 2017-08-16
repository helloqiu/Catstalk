# -*- coding: utf-8 -*-

import json
import os
from playhouse.shortcuts import model_to_dict
from flask import Flask, render_template
from catstalk.models import Tag, Post, Info

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    render_template('index.html')


def get_app(root_path):
    info = Info.select().get()
    app.template_folder = os.path.join(root_path, '{}/template/'.format(info.theme))
    return app
