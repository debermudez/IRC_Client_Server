#!usr/bin/env python3

import argparse
import sys

"""
Initial (very early) proof of concept for command parser. Not sure if this is the best route.
argparse is really useful but has a few issues for our use case, the worst of which is how it handles parsing failures.
As far as I can tell all it does it print the error the stderr and exit. We can wrap it in a try/except to prevent
the process from exiting but i'm not sure if it's possible to capture the error type/message. 
I'll have to look into that further...

Good news is argparse can be fed a list in place of sys.argv, so we could use it to parse commands inside a running
client or server process.
"""

# Functions to set up parsers for specific IRC commands
def parseJoin(joinParser):
    addRequiredArg(joinParser, "rooms")
    addOptionalArg(joinParser, "keys")


def parseList(listParser):
    addOptionalArg(listParser, "rooms")
    addOptionalArg(listParser, "server")


def parsePart(partParser):
    addRequiredArg(partParser, "rooms")
    addOptionalArg(partParser, "message")


def parseQuit(quitParser):
    addOptionalArg(quitParser, "message")


def parseNames(namesParser):
    addOptionalArg(namesParser, "rooms")


# General functions to add arguments to a parser
def addRequiredArg(commandParser, arg):
    commandParser.add_argument(arg)


def addOptionalArg(commandParser, arg):
    commandParser.add_argument("--" + arg)


ircCommands = {
    "join": parseJoin,
    "list": parseList,
    "part": parsePart,
    "quit": parseQuit,
    "names": parseNames,
}


def parseCommand(argv):
    if len(argv) > 1:
        commandArg = argv[1]
    else:
        print("no arguments received")
        return None

    command = ircCommands.get(commandArg)
    if command:
        parser = argparse.ArgumentParser(description="parse IRC command")
        parser.add_argument("command", help="a supported IRC command")
        command(parser)
        args = parser.parse_args()
        print("you parsed {}! here are its args: {}".format(commandArg, args))
    else:
        print("command not supported: {}".format(commandArg))
        return None
    return args


if __name__ == "__main__":
    parseCommand(sys.argv)