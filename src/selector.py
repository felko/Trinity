#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame as pg
from pygame.locals import *

from src.constants import *
from src.tile import Tile
from src.map_generator.blocks import *


class Selector:
	def __init__(self, model):
		self.model = model
		self.selected_tile = None

	def update(self):
		x, y = pg.mouse.get_pos()
		x += self.model.xfov.start
		y += self.model.yfov.start
		x //= TILE_W
		y //= TILE_H
		try:
			self.selected_tile = self.model[x, y]
		except IndexError:
			pass

	def place_block(self, block):
		self.model[self.selected_tile.tpos] = block

	def destroy_block(self):
		tile = self.model[self.selected_tile.tpos]
		self.model[self.selected_tile.tpos] = Block.by_name['air']
		return tile