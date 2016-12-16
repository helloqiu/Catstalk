# -*- coding: utf-8 -*-

from catstalk.cli import parser


def test_init():
    args = parser.parse_args("init".split())
    assert args.command == "init"
