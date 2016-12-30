# -*- coding: utf-8 -*-

import os
import unittest
import datetime
import webtest
from tornado.wsgi import WSGIAdapter
from playhouse.sqlite_ext import SqliteExtDatabase
from playhouse.test_utils import test_database

from catstalk.cat import Cat
from catstalk.static import POST_TEMPLATE
from catstalk.server import get_app
from catstalk.models import Tag, Post

test_db = SqliteExtDatabase(":memory:")


class ServerTestCase(unittest.TestCase):
    def tearDown(self):
        try:
            os.remove("blog_data.sqlite3")
        except OSError:
            pass

    def add_posts(self):
        date = datetime.datetime.now()
        str_date = date.strftime("%Y-%m-%d %H:%M:%S")
        content = u"%s%s" % (
            POST_TEMPLATE.replace("{{date}}", str_date).replace("{{title}}", "Test"), "Hello World!"
        )
        temp = content.split("---")
        content = "---\n%s\ntag: test\n---%s" % (temp[1], temp[2])
        Cat.compile_post(content)
        return str_date

    def add_tags(self):
        for i in range(0, 10):
            Tag.create(name="tag%d" % i)

    def test_tag_detail(self):
        with test_database(test_db, (Tag, Post)):
            # Add some post
            str_date = self.add_posts()
            app = webtest.TestApp(WSGIAdapter(get_app()))
            # Tag Detail
            response = app.get("/api/tags/none", expect_errors=True)
            self.assertEqual(response.status_code, 404)
            response = app.get("/api/tags/test")
            self.assertEqual(response.status_code, 200)
            response = response.json_body
            self.assertEqual(response["max_page"], 1)
            self.assertEqual(response["posts"][0]["tag"], "test")
            self.assertEqual(response["posts"][0]["date"], str_date)
            self.assertEqual(response["posts"][0]["title"], "Test")
            self.assertEqual(response["posts"][0]["content"], "<p>Hello World!</p>\n")

    def test_all_tag(self):
        with test_database(test_db, (Tag, Post)):
            # Add some tags
            self.add_tags()
            app = webtest.TestApp(WSGIAdapter(get_app()))
            # All Tag
            response = app.get("/api/tags")
            self.assertEqual(response.status_code, 200)
            response = response.json_body
            for i in range(0, len(response)):
                self.assertEqual(response[i]["name"], "tag%d" % i)
