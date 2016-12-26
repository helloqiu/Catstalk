# -*- coding: utf-8 -*-

import argparse
from catstalk.cat import Cat

DESCRIPTION = """The command line interface of Catstalk."""
USAGE = "catstalk <command> [options]"
COMMANDS = {
    "init <path default=\"blog\">": "generate a new project",
    "build <path default=\"content\"": "build content into a sqlite database"
}
COMMANDS_HELP = "\nCommands:\n"
for command in COMMANDS.keys():
    COMMANDS_HELP += "  %s    %s\n" % (command, COMMANDS[command])

parser = argparse.ArgumentParser(
    description=DESCRIPTION,
    usage=USAGE,
    epilog=COMMANDS_HELP,
    formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("command", help="the command that you want", nargs="+")


def parse():
    args = parser.parse_args()
    if args.command[0] == "init":
        if len(args.command) > 1:
            path = args.command[1]
        else:
            path = "blog"
        Cat.generate(path)
    elif args.command[0] == "build":
        if len(args.command) > 1:
            path = args.command[1]
        else:
            path = "content"
        Cat.compile(path)
