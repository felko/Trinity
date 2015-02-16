#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame as pg
from pygame.locals import *
from collections import OrderedDict

from src.tools import Locatable
from src.player_states import *
from src.inventory import Inventory


class Player(Locatable, MultiBehavioral):
	default_states = OrderedDict((
		(XMovementState, Idle),
		(YMovementState, OnGround)
	))

	def __init__(self, model, name, pos, hotbar):
		self.model = model
		self.name = name
		self.x, self.y = pos

		self.hotbar = hotbar
		self.inventory = Inventory()

		self.velocity_x = lambda dt: 0
		self.velocity_y = lambda dt: 0

		super().__init__()

		self.walking_time = 0

		self.fall_time = 1
		self.jump_time = 1
		self.jump_height = 100
		self.jump_gravity = 700
		self.jump_start = self.py

	def take_item(self, item):
		try:
			self.hotbar.add(item)
		except IndexError:
			self.inventory.add(item)