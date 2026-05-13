import os
import shlex
import subprocess

from collections import OrderedDict
from math import ceil

from .config import SHELL_PREFIX

class Alice_in_shell:
    def __init__(self, home):
        # shell & aliases file path
        self.home = home
        self.config_path = f'{self.home}/.{SHELL_PREFIX}_aliases'

    @staticmethod
    def parse_alias_line(line):
        stripped = line.strip()
        if not stripped.startswith("alias "):
            return None

        body = stripped[len("alias "):]
        try:
            parts = shlex.split(body)
        except ValueError:
            return None

        if not parts or "=" not in parts[0]:
            return None

        name, cmd = parts[0].split("=", 1)
        if not name or not cmd:
            return None

        return name, cmd

    def get_aliases(self):
        aliases = OrderedDict()
        mode = "r" if os.path.exists(self.config_path) else "a+"
        try:
            with open(self.config_path, mode, encoding="utf-8") as f:
                for line in f.readlines():
                    parsed = self.parse_alias_line(line)
                    if parsed:
                        name, cmd = parsed
                        aliases[name] = cmd
            return aliases
        except Exception as e:
            raise e

    def source_aliases(self):
        try:
            cmd = f'source {self.config_path}'
            subprocess.call([os.environ["SHELL"], "-ic", cmd], env=self.shell_env())
        except Exception as e:
            raise e

    def edit_aleases(self, editor):
        return self.edit_aliases(editor)

    def edit_aliases(self, editor):
        mode = "a"
        try:
            with open(self.config_path, mode):
                subprocess.call([editor, self.config_path])
        except Exception as e:
            raise e

    @staticmethod
    def run_alias(command):
        return subprocess.call(
            [os.environ["SHELL"], "-ic", command],
            env=Alice_in_shell.shell_env(),
        )

    @staticmethod
    def shell_env():
        env = os.environ.copy()
        if env.get("TERM") in (None, "", "dumb"):
            env["TERM"] = "xterm-256color"
        return env

    @staticmethod
    def alias_paginate(ordered, page_counter: int):
        alias_menu_page_counter = page_counter
        pages = int(ceil(len(ordered) / 10))
        if alias_menu_page_counter <= pages:
            count = 0
            chunk = {}
            for key in ordered:
                if count != 0:
                    if (
                        ((alias_menu_page_counter - 1) * 10)
                        < count
                        <= (alias_menu_page_counter * 10)
                    ):
                        chunk[f"{count}. {key}"] = ordered[key]
                elif count == 0 and alias_menu_page_counter == 1:
                    chunk[f"{count}. {key}"] = ordered[key]
                count += 1
            return chunk
        else:
            return 0
