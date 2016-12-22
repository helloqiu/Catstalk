# -*- coding: utf-8 -*-

import os
import datetime
import sys
from catstalk.static import POST_TEMPLATE

if sys.version_info[0] < 3:
    from io import open


class Generator(object):
    def __init__(self, path=None, ):
        self.path = path

    def generate(self):
        content_path = os.path.join(self.path, "content")
        os.mkdir(self.path)
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
