#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame as pg
from pygame.locals import *

from src.tools import Locatable, load_tile_size_image, normalize_path
from src.items import Item


class Tile(Locatable):
    def __init__(self, block, pos):
        self.block = block
        self.x, self.y = pos

    def __repr__(self):
        return "<{} ({}, {})>".format(
            self.block.name,
            self.tx, self.ty
        )

    def __bool__(self):
        return self.block.solid