# C:\Python34\python.exe
# -*- coding: utf-8 -*-

import random
import itertools as it

from src.map_generator.structs import *

BLOCK, VOID = True, False


class Generate(list):
    def __init__(self, length, flatness, height=range(1, 16), headstart=10, deniv=1, structs=Structure.structures):
        self.structs = structs

        #---------------- Binary terrain generation ----------------#
        array = [[VOID for iy in range(height.stop)] for ix in range(length)]
        mem = length * [0]
        mem[0] = headstart
        r = list(range(-deniv, deniv + 1))
        turns = 0
        for x in range(1, length):
            same = 0
            for col in mem[:x - 1:-1]:
                if col == mem[x]:
                    same += 1
                else:
                    break

            new = (not random.randint(0, flatness // same)) * random.choice(r)
            mem[x] = mem[x - 1] + new
            while mem[x] not in height:
                if mem[x] < height.start:
                    mem[x] += 1
                else:
                    mem[x] -= 1

            if new < 0:
                r = list(range(-deniv, 0)) + [0] * flatness
                turns = flatness
            elif new > 0:
                r = list(range(1, deniv + 1)) + [0] * flatness
                turns = flatness

            turns -= 1
            if turns == 0:
                r = list(range(-deniv, deniv + 1))

        for x, h in enumerate(mem):
            array[x] = [BLOCK] * h + [VOID] * (len(array[x]) - h)

        width = len(array)
        height = len(array[0])
        array = [[array[width - 1 - x][y] for x in range(width)][::-1] for y in range(height)][::-1]

        super().__init__(array)

        #---------------------- Block setting ----------------------#

        new_array = self[:]

        what_can_be_in = lambda depth: [(block if (random.randint(0, 100) in range(block.prob)) and (
            len(new_array) - depth in block.strat) else Block.by_name['stone']) for block in Mineral.blocks]

        def distance_from_surface(x, y):
            blocks_to_surface = 0
            for line in self[y::-1]:
                if not line[x]:
                    return blocks_to_surface
                else:
                    blocks_to_surface += 1
            return blocks_to_surface

        for y, line in enumerate(new_array):
            for x, block in enumerate(line):
                if block:
                    if distance_from_surface(x, y) > random.randint(3, 5):
                        new_block = Block.by_name['stone']
                    elif distance_from_surface(x, y) == 1:
                        new_block = Block.by_name['grass']
                    else:
                        new_block = Block.by_name['dirt']
                    new_array[y][x] = new_block
                else:
                    new_array[y][x] = Block.by_name['air']

        for y, line in enumerate(new_array):
            for x, block in enumerate(line):
                if block is Block.by_name['stone']:
                    new_array[y][x] = random.choice(what_can_be_in(y))

        super().__init__(new_array)

        #-------------------- Structure setting --------------------#

        new_array = self[:]

        for y, line in enumerate(self):
            for x, block in enumerate(line):
                for s in self.structs:
                    if s.cond(self, (x, y)):
                        self.add_structure(s, (x, y))

    def add_structure(self, struct, pos):
        for block_pos, block in struct.substitute(*pos):
            x, y = block_pos
            if x >= 0 and y >= 0:
                try:
                    self[x, y] = block
                except IndexError:
                    pass

    def __getitem__(self, item):
        if isinstance(item, (tuple, list)):
            x, y = item
            try:
                return self[y][x]
            except IndexError:
                pass
        else:
            return super().__getitem__(item)

    def __setitem__(self, item, value):
        if isinstance(item, (tuple, list)):
            x, y = item
            try:
                self[y][x] = value
            except IndexError:
                pass
        else:
            super().__setitem__(item, value)

    def __add__(self, other):
        new = self[:]
        for y, line in enumerate(other):
            new[y] += line
        return new