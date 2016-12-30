# -*- coding: utf-8 -*-


def serialize_post(posts, num):
    result = dict()
    result["max_page"] = int((num - 1) / 10) + 1
    result["posts"] = []

    for post in posts:
        try:
            tag = post.tag.name
        except:
            tag = None
        result["posts"].append({
            "tag": tag,
            "date": post.date.strftime("%Y-%m-%d %H:%M:%S"),
            "title": post.title,
            "content": post.content
        })

    return result
