# -*- coding: utf-8 -*-

from src.map_generator.conditions import *


class Structure:
    structures = []

    def __init__(self, pattern, base, cond=lambda: True):
        self.pattern = pattern
        self.base = base
        self.cond = cond

        Structure.structures.append(self)

    def substitute(self, x, y):
        base_x, base_y = self.base
        get_absolute = lambda rel_x, rel_y: (x+rel_x, y+rel_y)
        get_relative_from_base = lambda abs_x, abs_y: (abs_x-base_x, abs_y-base_y)

        block_dict = {}
        for iy, line in enumerate(self.pattern()):
            for ix, block in enumerate(line):
                if block is not None:
                    abs_pos = get_absolute(*get_relative_from_base(ix, iy))
                    block_dict[abs_pos] = block
        return block_dict.items()

n = None
a = Block.by_name['air']
l = Block.by_name['leaves']
s = Block.by_name['stem']
p = Block.by_name['planks']
w = Block.by_name['window']

TREE = Structure(
    lambda: [
        [n, n, n, l, l, l, l, n, n, n],
        [n, l, l, l, l, l, l, l, l, l],
        [l, l, l, l, l, l, l, l, l, l],
        [l, l, l, l, l, l, l, l, l, l],
        [l, l, l, l, l, l, l, l, l, l],
        [n, n, l, l, l, l, l, l, n, n],
        [n, n, n, n, s, s, s, n, n, n],
        [n, n, n, n, s, s, n, n, n, n],
        [n, n, n, n, s, s, n, n, n, n],
        [n, n, n, n, s, s, n, n, n, n],
        [n, n, n, n, s, s, n, n, n, n]
    ],
    base=(4, 10),
    cond=TREE
)

HOUSE = Structure(
    lambda: [
        [n, n, n, p, n, n, n],
        [n, n, p, p, p, n, n],
        [n, p, p, p, p, p, n],
        [p, p, p, p, p, p, p],
        [p, p, p, w, p, p, p],
        [p, w, p, w, p, w, p],
        [p, w, p, w, p, w, p],
        [p, p, p, p, p, p, p],
        [p, p, p, a, p, p, p],
        [p, w, a, a, a, w, p],
        [p, p, a, a, a, p, p]
    ],
    base=(3, 10),
    cond=HOUSE
)