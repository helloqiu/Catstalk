# -*- coding: utf-8 -*-

import json
import tornado.web
from playhouse.shortcuts import model_to_dict
from catstalk.models import Tag, Post


class AllTagHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        tags = []
        for tag in Tag.select().order_by(Tag.name):
            tags.append(model_to_dict(tag))
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(tags))


class TagDetailHandler(tornado.web.RequestHandler):
    def get(self, name, page=1):
        try:
            page = int(page)
        except TypeError:
            page = 1
        posts = Post.select().join(Tag).order_by(Post.date).paginate(page, 10).where(Tag.name == name)
        if not posts.exists():
            raise tornado.web.HTTPError(404)
        num = Post.select().join(Tag).where(Tag.name == name).count()
        posts_result = []
        for post in posts:
            temp = model_to_dict(post)
            temp["date"] = temp["date"].strftime("%Y-%m-%d %H:%M:%S")
            posts_result.append(temp)
        result = dict(
            max_page=int((num - 1) / 10) + 1,
            posts=posts_result,
        )
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(result))


class PostHandler(tornado.web.RequestHandler):
    def get(self, page=1):
        try:
            page = int(page)
        except TypeError:
            page = 1
        posts = Post.select().order_by(Post.date).paginate(page, 10)
        num = Post.select().count()
        posts_result = []
        for post in posts:
            temp = model_to_dict(post)
            temp["date"] = temp["date"].strftime("%Y-%m-%d %H:%M:%S")
            posts_result.append(temp)
        result = dict(
            max_page=int((num - 1) / 10) + 1,
            posts=posts_result,
        )
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(result))


class PostDetailHandler(tornado.web.RequestHandler):
    def get(self, title):
        post = Post.select().where(Post.title == title)
        if not post.exists():
            raise tornado.web.HTTPError(404)
        post = post.get()
        post = model_to_dict(post)
        post["date"] = post["date"].strftime("%Y-%m-%d %H:%M:%S")
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(post))


def get_app():
    return tornado.web.Application([
        (r"/api/tags(/)?$", AllTagHandler),
        (r"/api/tags/([^/]+)", TagDetailHandler),
        (r"/api/tags/([^/]+)/page/(\d+)", TagDetailHandler),
        (r"/api/posts(/)?$", PostHandler),
        (r"/api/posts/page/(\d+)", PostHandler),
        (r"/api/posts/title/([^/]+)", PostDetailHandler),
    ])
