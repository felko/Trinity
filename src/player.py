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
        self.jump_start = self.py

        self.gravity = 1000

    def take_item(self, item):
        if not self.hotbar.is_full() or item in self.hotbar:
            self.hotbar.add(item)
        else:
            self.inventory.add(item)