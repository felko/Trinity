#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from src.map_generator.generate import Generate
from src.map_generator.blocks import Block
from src.map_generator.chunk import Chunk
from src.tile import Tile
from src.constants import *
from src.player_states import *


class MapModel(list):
    def __init__(self, *chunks,  player=None):
        super().__init__(chunks)
        self.player = player
        self.width, self.height = len(chunks) * CHUNK_W, CHUNK_H
        self.xfov = slice(0, 1)
        self.yfov = slice(0, 1)

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            return super().__getitem__(item)

        elif isinstance(item, tuple):
            x, y = item
            if isinstance(x, int) and x >= 0 and isinstance(y, int) and y >= 0:
                return self[x // CHUNK_W][x % CHUNK_W, y]
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
                self[x // CHUNK_W][x % CHUNK_W, y] = value
            else:
                raise TypeError('coordinates must be integers.')

        else:
            raise TypeError('item must be an integer, a slice or a tuple.')

    def __add__(self, other):
        new = self[:]
        for y, line in enumerate(other):
            new[y] += line
        return new

    @classmethod
    def generate(cls, w, h=CHUNK_H):
        generated = Generate(headstart=h//2, flatness=4, deniv=1, size=(w, h))
        return MapModel(*generated)

    def update(self, dt):
        neighbors = self.get_neighbors(*self.player.tpos)
        if not neighbors['bottom'] and not self.get_neighbors(*neighbors['bottom'].tpos)['right'] and \
                        self.player.states[YMovementState] is not Jumping:
            self.player.enter(Falling)
        self.xfov = slice(self.player.px - SCREEN_W // 2, self.player.px + SCREEN_W // 2)
        self.yfov = slice(self.player.py - SCREEN_H // 2, self.player.py + SCREEN_H // 2)
        self.player.update(dt)

    def tiles(self):
        for chunk in self:
            for tile in chunk.tiles():
                yield tile

    def get_neighbors(self, tx, ty):
        neighbors = {}
        direction_map = {
            'top': (+0, -1),
            'bottom': (+0, +1),
            'left': (-1, +0),
            'right': (+1, +0),
        }

        for direction_name, offsets in direction_map.items():
            dtx, dty = offsets
            try:
                neighbors[direction_name] = self[tx + dtx, ty + dty]
            except IndexError:
                neighbors[direction_name] = Tile(Block('void'), (tx + dtx, ty + dty))
            except TypeError:
                neighbors[direction_name] = Tile(Block('void'), (tx + dtx, ty + dty))
        return neighbors

    def get_random_spawn_point(self):
        potential_spawn_points = []
        for tile in self.tiles():
            if self.get_neighbors(*tile.tpos)['bottom'] and not (tile.block.opaque or tile.block.solid):
                potential_spawn_points.append(tile.ppos)

        try:
            return random.choice(potential_spawn_points)
        except IndexError:
            return 0, 0