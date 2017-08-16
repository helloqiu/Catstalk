# -*- coding: utf-8 -*-

import os
import datetime
import sys
import shutil
import markdown2
import peewee
import json
import subprocess
from catstalk.static import POST_TEMPLATE, CONF_TEMPLATE
from catstalk.models import Tag, Post, Info, db
from catstalk.logger import logger

DEFAULT_THEME = "https://github.com/helloqiu/catstalk-theme-simple"

if sys.version_info[0] < 3:
    from io import open


class Cat(object):
    @staticmethod
    def generate(path):
        """
        Method to generate a new source folder.
        :param path: The path of the new folder.
        """
        logger.info("Creating new catstalk folder in \"{}\".".format(path))
        content_path = os.path.join(path, "content")
        os.mkdir(path)
        os.mkdir(content_path)
        os.mkdir(os.path.join(path, "uploads"))
        os.mkdir(os.path.join(path, "theme"))
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
        with open(
                os.path.join(path, "config.json"),
                mode="w",
                encoding="utf-8"
        ) as f:
            f.write(CONF_TEMPLATE)
        avatar_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "resource/avatar.png"
        )
        shutil.copy(avatar_path, os.path.join(path, "uploads/"))
        # Clone theme repo
        logger.info("Clone theme repo.")
        p = subprocess.Popen(["git", "clone", DEFAULT_THEME, os.path.join(path, "theme/simple")])
        p.wait()
        logger.info("Done.")

    @staticmethod
    def compile_post(content):
        """
        Compile a post into a model.
        :param content: The content of the post.
        """
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
            logger.error("Can not find content folder \"%s\"." % content_path)
            return
        try:
            db.create_tables([Tag, Post, Info])
        except peewee.OperationalError:
            pass
        for file in os.listdir(content_path):
            if file.endswith("md"):
                with open(os.path.join(content_path, file), mode="r", encoding="utf-8") as f:
                    Cat.compile_post(f.read())

    @staticmethod
    def compile_info(info):
        info = json.loads(info)
        Info.create(**info)
