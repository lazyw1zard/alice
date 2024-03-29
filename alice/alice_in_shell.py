import os
import re
import subprocess

from collections import OrderedDict
from math import ceil

from config import SHELL_PREFIX

class Alice_in_shell:
    def __init__(self, home):
        # shell & aliases file path
        self.home = home
        self.config_path = f'{self.home}/.{SHELL_PREFIX}_aliases'

    def get_aliases(self):
        aliases = OrderedDict()
        mode = "r" if os.path.exists(self.config_path) else "a+"
        try:
            with open(self.config_path, mode) as f:
                for line in f.readlines():
                    clean = line.replace('"', "")
                    result = re.split(r"=", clean)
                    name = result[0].replace("alias", "").lstrip()
                    cmd = result[1].rstrip()
                    aliases[name] = cmd
            return aliases
        except Exception as e:
            raise e

    def source_aliases(self):
        try:
            cmd = f'source {self.config_path}'
            subprocess.call([os.environ["SHELL"], "-ic", cmd])
        except Exception as e:
            raise e

    def edit_aleases(self, editor):
        mode = "a"
        try:
            with open(self.config_path, mode):
                subprocess.call([editor, self.config_path])
        except Exception as e:
            raise e

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
