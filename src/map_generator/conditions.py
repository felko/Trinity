# -*- coding: utf-8 -*-

import random

from src.map_generator.properties import *
from src.map_generator.blocks import *


def TREE(map_, pos):
    x, y = pos
    if map_[x, y+1] in (Block.by_name['dirt'], Block.by_name['grass'])\
            and map_[x+1, y+1] in (Block.by_name['dirt'], Block.by_name['grass'])\
            and not map_[x, y]\
            and not map_[x+1, y]:
        tree = random.randint(0, 1000) in range(tree_rate)
        return tree

def HOUSE(map_, pos):
    x, y = pos
    if map_[x-3, y+1] \
            and map_[x-2, y+1]\
            and map_[x-1, y+1]\
            and map_[x, y+1]\
            and map_[x+1, y+1]\
            and map_[x+2, y+1]\
            and map_[x+3, y+1]\
            and map_[x-3, y] \
            and not map_[x-2, y]\
            and not map_[x-1, y]\
            and not map_[x, y]\
            and not map_[x+1, y]\
            and not map_[x+2, y]\
            and not map_[x+3, y]:
        return random.randint(0, 1000) in range(house_rate)