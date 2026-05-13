#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Execute main menu"""

__version__ = "0.1.4"

import argparse
import curses
import sys
from collections import OrderedDict

from .alice_in_shell import Alice_in_shell
from .config import EDITOR, HOME, MENU_LANG


def main(stdscr):
    from .menu import Menu

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)

    # Getting initial terminal window size
    height, width = stdscr.getmaxyx()

    Menu.display_rows(stdscr, MENU_LANG, 0, 1, "main", height, width)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="alice",
        description="Browse, search, edit, and run shell aliases.",
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("tui", help="open the interactive curses menu")

    list_parser = subparsers.add_parser("list", help="list parsed aliases")
    list_parser.add_argument("--names", action="store_true", help="print names only")

    search_parser = subparsers.add_parser("search", help="search aliases by name or command")
    search_parser.add_argument("query")

    show_parser = subparsers.add_parser("show", help="show one alias command")
    show_parser.add_argument("name")

    run_parser = subparsers.add_parser("run", help="run one alias command in the current shell")
    run_parser.add_argument("name")

    subparsers.add_parser("edit", help="open the aliases file in $EDITOR")
    subparsers.add_parser("path", help="print the aliases file path")

    return parser


def print_aliases(aliases, names_only=False):
    for name, command in aliases.items():
        if names_only:
            print(name)
        else:
            print(f"{name}\t{command}")


def find_alias(aliases, name):
    try:
        return aliases[name]
    except KeyError:
        print(f"alias not found: {name}", file=sys.stderr)
        return None


def main_entry(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    alice = Alice_in_shell(HOME)

    if args.command in (None, "tui"):
        curses.wrapper(main)
        return 0

    if args.command == "path":
        print(alice.config_path)
        return 0

    if args.command == "edit":
        alice.edit_aliases(EDITOR)
        return 0

    aliases = alice.get_aliases()

    if args.command == "list":
        print_aliases(aliases, args.names)
        return 0

    if args.command == "search":
        query = args.query.lower()
        matches = OrderedDict(
            (name, command)
            for name, command in aliases.items()
            if query in name.lower() or query in command.lower()
        )
        print_aliases(matches)
        return 0 if matches else 1

    if args.command == "show":
        command = find_alias(aliases, args.name)
        if command is None:
            return 1
        print(command)
        return 0

    if args.command == "run":
        command = find_alias(aliases, args.name)
        if command is None:
            return 1
        return alice.run_alias(command)

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main_entry())
