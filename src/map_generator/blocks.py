#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import pygame as pg
from pygame.locals import *


from src.tools import load_tile_size_image, normalize_path
from src.items import Item


class Block:
	blocks = []
	from_id = {}
	by_name = {}
	next_id = 0

	def __init__(self, name, texture='unknown.png',
				 opaque=True, solid=True, break_sound='stony.ogg',
				 drops=(), **kwds):
		self.name = name
		if isinstance(texture, str):
			self.texture = load_tile_size_image('src/assets/texture/tile/'+texture)
		elif isinstance(texture, pg.Surface):
			self.texture = texture
		else:
			raise TypeError("texture should be either a pygame.Surface or the path to the image file")
		if isinstance(break_sound, str):
			self.break_sound = self.break_sound = pg.mixer.Sound(normalize_path('src/assets/sound/'+break_sound))
		elif isinstance(break_sound, pg.mixer.Sound):
			self.break_sound = break_sound
		else:
			raise TypeError("break sound should be either a pygame.mixer.Sound or the path to the sound file")
		self.opaque = opaque
		self.solid = solid
		self.drops = []
		for item in drops:
			if isinstance(item, str):
				self.drops.append(Item.by_name[item])
			else:
				self.drops.append(item)

	def __bool__(self):
		return bool(self.solid)

	def __repr__(self):
		return "<Block {}{}{}>".format(
			'opaque' if self.opaque else '',
			' ' if self.solid and self.opaque else '',
			'solid' if self.solid else ''
		)

	@classmethod
	def load_all(cls, path='src/assets/block'):
		for dirpath, dirnames, filenames in os.walk(path):
			for filename in filenames:
				if filename.endswith('.block'):
					block_path = dirpath + os.sep + filename
					with open(block_path) as item_file:
						json_content = item_file.read()
						attributes = json.loads(json_content)
						block = cls(name=filename.split('.')[0], **attributes)
						cls.blocks.append(block)
						cls.by_name[block.name] = block
						cls.from_id[cls.next_id] = block
						cls.next_id += 1

Block.load_all()


class Mineral(Block):
	blocks = []
	probs = []

	def __init__(self, block, strat=range(0, 0), prob=1.0):
		super().__init__(**block.__dict__)
		self.strat = strat
		self.prob = prob

		Mineral.add_block(self)

	@classmethod
	def add_block(cls, block):
		cls.blocks.append(block)
		cls.probs = []
		for block in cls.blocks:
			cls.probs += [block] * block.prob
		while len(cls.probs) < 1000:
			cls.probs.append(Block.by_name['stone'])

# Minerals
SAPPHIRE = Mineral(Block.by_name['sapphire'], strat=range(0, 10), prob=3)
EMERALD = Mineral(Block.by_name['emerald'], strat=range(0, 10), prob=3)
RUBY = Mineral(Block.by_name['ruby'], strat=range(0, 10), prob=3)
DIAMOND = Mineral(Block.by_name['diamond'], strat=range(0, 3), prob=1)
GOLD = Mineral(Block.by_name['gold'], strat=range(0, 7), prob=2)