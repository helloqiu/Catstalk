# -*- coding: utf-8 -*-

import argparse

DESCRIPTION = """The command line interface of Catstalk."""
USAGE = "catstalk <command> [options]"
COMMANDS = {
    "init": "generate a new project",
}
COMMANDS_HELP = "\nCommands:\n"
for command in COMMANDS.keys():
    COMMANDS_HELP += "  %s    %s\n" % (command, COMMANDS[command])

parser = argparse.ArgumentParser(
    description=DESCRIPTION,
    usage=USAGE,
    epilog=COMMANDS_HELP,
    formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("command", help="the command that you want")


def parse():
    args = parser.parse_args()
