# -*- coding: utf-8 -*-

import os
import shutil
import datetime
from catstalk.cat import Cat
from catstalk.static import POST_TEMPLATE
from catstalk.models import *


def test_generate():
    path = "blog"
    try:
        Cat.generate(path)
        assert os.path.exists(path)
        assert os.path.exists(os.path.join(path, "content"))
        assert os.path.exists(os.path.join(os.path.join(path, "content"), "HelloWorld.md"))
    finally:
        shutil.rmtree(path)


def test_compile_post():
    # Without tag
    try:
        date = datetime.datetime.now()
        str_date = date.strftime("%Y-%m-%d %H:%M:%S")
        content = u"%s%s" % (
            POST_TEMPLATE.replace("{{date}}", str_date).replace("{{title}}", "HelloWorld"), "Hello World!"
        )
        Cat.compile_post(content)
        post = Post.select().where(Post.title == "HelloWorld").first()
        assert post.date.strftime("%Y-%m-%d %H:%M:%S") == date.strftime("%Y-%m-%d %H:%M:%S")
        # TODO: Add more tests
    finally:
        os.remove("blog_data.sqlite3")
