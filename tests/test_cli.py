# -*- coding: utf-8 -*-

from catstalk.cli import parser


def test_init():
    # With default path
    args = parser.parse_args("init".split())
    assert args.command[0] == "init"
    # With specific path
    args = parser.parse_args("init test".split())
    assert args.command[0] == "init"
    assert args.command[1] == "test"


def test_build():
    # With default path
    args = parser.parse_args("build".split())
    assert args.command[0] == "build"
    # With specific path
    args = parser.parse_args("build test".split())
    assert args.command[0] == "build"
    assert args.command[1] == "test"
