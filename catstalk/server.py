# -*- coding: utf-8 -*-

import json
import tornado.web
from catstalk.models import Tag, Post


class AllTagHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        tags = []
        for tag in Tag.select().order_by(Tag.name):
            tags.append({"name": tag.name})
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(tags))


class TagDetailHandler(tornado.web.RequestHandler):
    def get(self, name=None, page=1):
        if not name:
            raise tornado.web.HTTPError(404)
        else:
            try:
                page = int(page)
            except TypeError:
                raise tornado.web.HTTPError(404)
            posts = Post.select().join(Tag).order_by(Post.date).paginate(page, 10).where(Tag.name == name)
            if not posts.exists():
                raise tornado.web.HTTPError(404)
            num = Post.select().join(Tag).where(Tag.name == name).count()
            result = dict()
            result["max_page"] = int(num / 10) + 1
            result["posts"] = []
            for post in posts:
                result["posts"].append({
                    "tag": post.tag.name,
                    "date": post.date.strftime("%Y-%m-%d %H:%M:%S"),
                    "title": post.title,
                    "content": post.content
                })
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            self.write(json.dumps(result))


# TODO: Add AllPostHandler and PostDetailHandler


def get_app():
    return tornado.web.Application([
        (r"/api/tags(/)?$", AllTagHandler),
        (r"/api/tags/([^/]+)/page/(\d+)", TagDetailHandler),
        (r"/api/tags/([^/]+)", TagDetailHandler)

    ])
