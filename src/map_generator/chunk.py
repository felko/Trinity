#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from src.constants import *
from src.tile import Tile
from src.map_generator.blocks import Block, Mineral
from src.map_generator.structs import Structure

BLOCK, VOID = True, False


class Chunk(list):
    last_column_height = None
    cur_flatness_level = None

    def __init__(self, headstart, flatness, deniv, size=CHUNK_S):
        self.structs = Structure.structures

        width, height = size

        #---------------- Binary terrain generation ----------------#
        array = [[VOID for iy in range(height)] for ix in range(width)]
        mem = width * [0]
        mem[0] = headstart
        r = list(range(-deniv, deniv + 1))
        turns = 0
        for x in range(1, width):
            same = 0
            for col in mem[:x - 1:-1]:
                if col == mem[x]:
                    same += 1
                else:
                    break

            new = (not random.randint(0, flatness // same)) * random.choice(r)
            mem[x] = mem[x - 1] + new

            while mem[x] > height:
                if mem[x] < 1:
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

        #----------------------- Tile setting ----------------------#

        for y, line in enumerate(self):
            for x, block in enumerate(line):
                self[x, y] = block

    def add_structure(self, struct, pos):
        for block_pos, block in struct.substitute(*pos):
            x, y = block_pos
            if x >= 0 and y >= 0:
                try:
                    self[x, y] = block
                except IndexError:
                    pass

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            return super().__getitem__(item)

        elif isinstance(item, tuple):
            x, y = item
            if isinstance(x, int) and 0 <= x < CHUNK_W and isinstance(y, int) and 0 <= y < CHUNK_H:
                return self[y][x]
            else:
                return Tile(Block('void'), item)

        else:
            raise TypeError('item must be an integer, a slice or a tuple.')

    def __setitem__(self, item, value):
        if not isinstance(value, (Tile, Block)):
            raise TypeError('must be Tile or Block object (got {}).'.format(value.__class__.__name__))

        if isinstance(item, (int, slice)):
            super().__setitem__(item, value)

        elif isinstance(item, tuple):
            x, y = item
            if isinstance(value, Block):
                item = list(item)
                item[0] *= TILE_W
                item[1] *= TILE_H
                value = Tile(
                    block=value,
                    pos=item
                )
            if isinstance(x, int) and isinstance(y, int):
                self[y][x] = value
            else:
                raise TypeError('coordinates must be integers.')

        else:
            raise TypeError('item must be an integer, a slice or a tuple.')

    def column(self, i):
        for line in self:
            yield line[i]

    def tiles(self):
        for line in self:
            for tile in line:
                yield tile