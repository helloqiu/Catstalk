# -*- coding: utf-8 -*-

import json
import tornado.web
from catstalk.models import Tag, Post
from catstalk.utils import serialize_post


class AllTagHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        tags = []
        for tag in Tag.select().order_by(Tag.name):
            tags.append({"name": tag.name})
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(tags))


class TagDetailHandler(tornado.web.RequestHandler):
    def get(self, name=None, page=1):
        posts = Post.select().join(Tag).order_by(Post.date).paginate(page, 10).where(Tag.name == name)
        if not posts.exists():
            raise tornado.web.HTTPError(404)
        num = Post.select().join(Tag).where(Tag.name == name).count()
        result = serialize_post(posts, num)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(result))


# TODO: Add AllPostHandler and PostDetailHandler

class PostHandler(tornado.web.RequestHandler):
    def get(self, page=1):
        posts = Post.select().order_by(Post.date).paginate(page, 10)
        num = Post.select().count()
        result = serialize_post(posts, num)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(result))


def get_app():
    return tornado.web.Application([
        (r"/api/tags(/)?$", AllTagHandler),
        (r"/api/tags/([^/]+)/page/(\d+)", TagDetailHandler),
        (r"/api/tags/([^/]+)", TagDetailHandler)

    ])
