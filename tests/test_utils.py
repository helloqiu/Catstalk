# -*- coding: utf-8 -*-

import datetime
from catstalk.utils import serialize_post


class DottableDict(dict):
    def __init__(self, *args, **kwargs):
        super(DottableDict, self).__init__(*args, **kwargs)
        self.__dict__ = dict()


def test_serialize_post():
    # Without tag
    posts = []
    date = datetime.datetime.now()
    str_date = date.strftime("%Y-%m-%d %H:%M:%S")
    for i in range(0, 10):
        post = DottableDict()
        post.date = date
        post.title = "test_title"
        post.content = "test"
        posts.append(post)
    num = len(posts)
    result = serialize_post(posts, num)
    for post in result["posts"]:
        assert post["date"] == str_date
        assert post["title"] == "test_title"
        assert post["content"] == "test"
        assert post["tag"] is None
    assert result["max_page"] == 1
    # With tag
    posts = []
    for i in range(0, 10):
        post = DottableDict()
        post.date = date
        post.title = "test_title"
        post.content = "test"
        tag = DottableDict()
        tag.name = "tag"
        post.tag = tag
        posts.append(post)
    num = len(posts)
    result = serialize_post(posts, num)
    for post in result["posts"]:
        assert post["date"] == str_date
        assert post["title"] == "test_title"
        assert post["content"] == "test"
        assert post["tag"] == "tag"
    assert result["max_page"] == 1
