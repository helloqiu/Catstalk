# -*- coding: utf-8 -*-

import os
import datetime
import sys
import logging
import markdown2
from catstalk.static import POST_TEMPLATE
from catstalk.models import Tag, Post

if sys.version_info[0] < 3:
    from io import open


class Cat(object):
    @staticmethod
    def generate(path):
        content_path = os.path.join(path, "content")
        os.mkdir(path)
        os.mkdir(content_path)
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(
                os.path.join(content_path, "HelloWorld.md"),
                mode="w",
                encoding="utf-8"
        ) as f:
            f.write(
                u"%s%s" % (
                    POST_TEMPLATE.replace("{{date}}", date).replace("{{title}}", "HelloWorld"), "Hello World!"
                )
            )

    @staticmethod
    def compile_post(content):
        post = markdown2.markdown(content, extras=["metadata"])
        # Get tag
        if u"tag" in post.metadata:
            if not Tag.select().where(Tag.name == post.metadata["tag"]).exists():
                Tag.create(name=post.metadata["tag"])
        else:
            post.metadata["tag"] = None
        Post.create(
            tag=Tag.select().where(Tag.name == post.metadata["tag"]).first(),
            title=post.metadata["title"],
            date=datetime.datetime.strptime(post.metadata["date"], "%Y-%m-%d %H:%M:%S"),
            content=post
        )

    @staticmethod
    def compile(content_path="content"):
        try:
            assert os.path.exists(content_path)
        except AssertionError:
            logging.error("Can not find content folder \"%s\"." % content_path)
            return
        for file in os.listdir(content_path):
            if file.endswith("md"):
                with open(os.path.join(content_path, file), mode="r", encoding="utf-8") as f:
                    Cat.compile_post(f.read())
