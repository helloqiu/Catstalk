# -*- coding: utf-8 -*-

import argparse

DESCRIPTION = """The command line interface of Catstalk."""
USAGE = "catstalk <command> [options]"
COMMANDS = ["init"]

parser = argparse.ArgumentParser(description=DESCRIPTION, usage=USAGE)

command = parser.add_argument_group("Commands")
command.add_argument("init", help="generate a new project")

args = parser.parse_args()
