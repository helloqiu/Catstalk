# -*- coding: utf-8 -*-

import os
import shutil
from catstalk.generator import Generator


def test_geenrator():
    path = "blog"
    generator = Generator(path=path)
    assert generator.path == path
    generator.generate()
    assert os.path.exists(path)
    shutil.rmtree(path)
