#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame as pg
from pygame.locals import *

pg.mixer.init()

from src.tools import load_tile_size_image
from src.constants import *
from src.tile import Tile


class Game:
	screen = pg.display.set_mode(SCREEN_S)
	pg.display.set_caption('Trinity')
	pg.display.set_icon(load_tile_size_image('src/assets/gui/trinity.png'))

	def __init__(self, player, selector, model, view):
		self.player = player
		self.selector = selector
		self.model = model
		self.model.player = player
		self.selected_tile = None
		self.view = view
		self.clock = pg.time.Clock()

	def process(self, event):
		if event.type == KEYDOWN:
			if event.key == K_a:
				self.player.enter(MovingLeft)
			elif event.key == K_d:
				self.player.enter(MovingRight)
			elif event.key == K_SPACE:
				if self.player.states[YMovementState] not in (Falling, Jumping):
					self.player.enter(Jumping)
			elif event.key == K_LSHIFT and pg.key.get_pressed()[K_a]:
				if self.player.states[YMovementState] not in (Falling, Jumping):
					self.player.enter(RunningLeft)
			elif event.key == K_LSHIFT and pg.key.get_pressed()[K_d]:
				if self.player.states[YMovementState] not in (Falling, Jumping):
					self.player.enter(RunningRight)

		elif event.type == KEYUP:
			if event.key in (K_a, K_d):
				self.player.enter(Idle)
			elif event.key == K_LSHIFT:
				if pg.key.get_pressed()[K_a]:
					self.player.enter(MovingLeft)
				elif pg.key.get_pressed()[K_d]:
					self.player.enter(MovingRight)

		elif event.type == MOUSEMOTION:
			self.selector.update()

		elif event.type == MOUSEBUTTONDOWN:
			if event.button == 4:
				self.player.hotbar.selected -= 1
				self.player.hotbar.selected %= self.player.hotbar.length
			elif event.button == 5:
				self.player.hotbar.selected += 1
				self.player.hotbar.selected %= self.player.hotbar.length

		from src.map_generator.blocks import Block

		mousebutton = pg.mouse.get_pressed()
		if mousebutton[0] == 1:
			try:
				block = Block.by_name[list(self.player.hotbar.keys())[self.player.hotbar.selected].to_block]
			except IndexError:
				pass
			else:
				self.selector.place_block(block)
		elif mousebutton[2] == 1:
			old_tile = self.selector.destroy_block()
			for drop in old_tile.block.drops:
				self.player.take_item(drop)
			if old_tile.block is not Block.by_name['air']:
				old_tile.block.break_sound.play()

	def start(self):
		running = True
		while running:
			dt = self.clock.tick()
			for event in pg.event.get():
				if event.type == pg.QUIT:
					running = False
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						running = False
				self.process(event)
			self.model.update(dt)

			self.view.render()
			self.screen.blit(self.view, (0, 0))
			pg.display.flip()
			pg.time.wait(int((1/120)*1000))


from .player_states import *