# -*- coding: utf-8 -*-

import os
import shutil
from catstalk.generator import Generator


def test_geenrator():
    path = "blog"
    try:
        generator = Generator(path=path)
        assert generator.path == path
        generator.generate()
        assert os.path.exists(path)
        assert os.path.exists(os.path.join(path, "content"))
        assert os.path.exists(os.path.join(os.path.join(path, "content"), "HelloWorld.md"))
    finally:
        shutil.rmtree(path)
