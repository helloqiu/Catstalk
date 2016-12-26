# -*- coding: utf-8 -*-

import os
import shutil
import unittest
import datetime
from peewee import IntegrityError
from catstalk.cat import Cat
from catstalk.static import POST_TEMPLATE
from catstalk.models import *


class CatTestCase(unittest.TestCase):
    def test_generate(self):
        path = "blog"
        try:
            Cat.generate(path)
            self.assertTrue(os.path.exists(path))
            self.assertTrue(os.path.exists(os.path.join(path, "content")))
            self.assertTrue(os.path.exists(os.path.join(os.path.join(path, "content"), "HelloWorld.md")))
        finally:
            shutil.rmtree(path)

    def test_compile_post(self):
        try:
            # Without tag
            date = datetime.datetime.now()
            str_date = date.strftime("%Y-%m-%d %H:%M:%S")
            content = u"%s%s" % (
                POST_TEMPLATE.replace("{{date}}", str_date).replace("{{title}}", "HelloWorld"), "Hello World!"
            )
            Cat.compile_post(content)
            post = Post.select().where(Post.title == "HelloWorld").first()
            self.assertEqual(post.date.strftime("%Y-%m-%d %H:%M:%S"), date.strftime("%Y-%m-%d %H:%M:%S"))
            self.assertEqual(post.content, "<p>Hello World!</p>\n")
            # With tag
            content = u"%s%s" % (
                POST_TEMPLATE.replace("{{date}}", str_date).replace("{{title}}", "WithTag"), "Hello World!"
            )
            temp = content.split("---")
            content = "---\n%s\ntag: test\n---%s" % (temp[1], temp[2])
            Cat.compile_post(content)
            tag = Tag.select().where(Tag.name == "test").first()
            self.assertTrue(tag)
            post = Post.select().where(Post.title == "WithTag").first()
            self.assertEqual(post.date.strftime("%Y-%m-%d %H:%M:%S"), date.strftime("%Y-%m-%d %H:%M:%S"))
            self.assertEqual(post.tag, tag)
            self.assertEqual(post.content, "<p>Hello World!</p>\n")
            # Unique
            self.assertRaises(IntegrityError, Cat.compile_post, content)
        finally:
            os.remove("blog_data.sqlite3")
