# -*- coding: utf-8 -*-

import json
import tornado.web
from catstalk.models import Tag, Post


class AllTagHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        tags = Tag.select().order_by(Tag.name).get()
        return json.dumps(tags)


class TagDetailHandler(tornado.web.RequestHandler):
    def get(self, name=None, page=1):
        if not name:
            raise tornado.web.HTTPError(404)
        else:
            posts = Post.select().order_by(Post.date).where(Post.tag.name == name).get()
            try:
                page = int(page)
            except TypeError:
                raise tornado.web.HTTPError(404)
            result = dict()
            result["max_page"] = int(len(posts) / 10)
            if page >= result["max_page"]:
                posts = posts[result["max_page"] * 10:]
            else:
                posts = posts[page * 10: (page + 1) * 10]
            result["posts"] = posts
            return json.dumps(result)

# TODO: Add AllPostHandler and PostDetailHandler


def get_app():
    return tornado.web.Application([
        (r"/api/tags(/)?$", AllTagHandler),
        (r"/api/tags/([^/]+)/page/(\d+)", TagDetailHandler),
        (r"/api/tags/([^/]+)", TagDetailHandler)

    ])
