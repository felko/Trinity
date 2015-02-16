#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.inventory import Inventory


class HotBar(Inventory):
	def __init__(self, length):
		super().__init__()
		self.length = length
		self.selected = 0

	def add(self, item):
		if not self.is_full() or item in self:
			self[item] += 1
		else:
			raise IndexError('the hotbar is full')

	def is_full(self):
		return len(self) == self.length