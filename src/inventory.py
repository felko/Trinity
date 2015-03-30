#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict

from src.items import Item


class Inventory(OrderedDict):
    def __init__(self, items=OrderedDict()):
        if all(isinstance(item, Item) for item in items):
            super().__init__(items)
        else:
            raise TypeError("Excpected a list of items.")

    def __getitem__(self, item):
        if isinstance(item, str):
            return self[Item.by_name[item]]
        elif isinstance(item, Item):
            try:
                return super().__getitem__(item)
            except KeyError:
                return 0

    def add(self, item):
        self[item] += 1