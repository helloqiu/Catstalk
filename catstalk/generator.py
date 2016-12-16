# -*- coding: utf-8 -*-

import os


class Generator(object):
    def __init__(self, path=None, ):
        self.path = path

    def generate(self):
        os.mkdir(self.path)
