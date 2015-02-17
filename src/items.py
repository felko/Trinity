#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

from src.tools import load_item_icon


class Item:
    by_name = {}

    def __init__(self, name, icon, lore=None, **kwds):
        self.name, self.lore = name, lore
        self.icon = load_item_icon('src/assets/texture/item/' + icon)
        self.__dict__.update(kwds)

    @classmethod
    def load_all(cls, path='src/assets/item'):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith('.item'):
                    path = dirpath + os.sep + filename
                    with open(path) as item_file:
                        json_content = item_file.read()
                        attributes = json.loads(json_content)
                        Item.by_name[filename.split('.')[0]] = Item(**attributes)