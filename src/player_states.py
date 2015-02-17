#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

from src.state import *
from src.constants import *
from src.tools import load_tile_size_image, Locatable


class XMovementState:
    pass


class YMovementState:
    pass


@state()
class MovingLeft(XMovementState):
    walking = (
        load_tile_size_image('src/assets/entity/player_left_walking_0.png'),
        load_tile_size_image('src/assets/entity/player_left.png'),
        load_tile_size_image('src/assets/entity/player_left_walking_1.png'),
        load_tile_size_image('src/assets/entity/player_left.png')
    )

    @classmethod
    def on_enter(cls, player):
        player.walking_time = 0
        player.velocity_x = lambda dt: -dt // 6

    def update(self, dt):
        if not self.model[self.tpos]:
            if self.states[YMovementState] is Falling:
                Falling.update(self, dt)
                self.px += self.velocity_x(dt) // 4
            elif self.states[YMovementState] is Jumping:
                Jumping.update(self, dt)
                self.px += self.velocity_x(dt)
            else:
                self.walking_time += 1 / 6
                self.sprite = MovingLeft.walking[int(self.walking_time) % len(MovingLeft.walking)]
                self.px += self.velocity_x(dt)


@state()
class MovingRight(XMovementState):
    walking = (
        load_tile_size_image('src/assets/entity/player_right_walking_0.png'),
        load_tile_size_image('src/assets/entity/player_right.png'),
        load_tile_size_image('src/assets/entity/player_right_walking_1.png'),
        load_tile_size_image('src/assets/entity/player_right.png')
    )

    @classmethod
    def on_enter(cls, player):
        player.walking_time = 0
        player.velocity_x = lambda dt: dt // 6

    def update(self, dt):
        if not self.model.get_neighbors(*self.tpos)['right']:
            if self.states[YMovementState] is Falling:
                Falling.update(self, dt)
                self.px += self.velocity_x(dt) // 4
            elif self.states[YMovementState] is Jumping:
                Jumping.update(self, dt)
                self.px += self.velocity_x(dt)
            else:
                self.walking_time += 1 / 6
                self.sprite = MovingRight.walking[int(self.walking_time) % len(MovingRight.walking)]
                self.px += self.velocity_x(dt)


@state()
class RunningLeft(MovingLeft):
    @classmethod
    def on_enter(cls, player):
        player.velocity_x = lambda dt: -dt // 4


@state()
class RunningRight(MovingRight):
    @classmethod
    def on_enter(cls, player):
        player.velocity_x = lambda dt: dt // 4


@state()
class Idle(XMovementState):
    sprite = load_tile_size_image('src/assets/entity/player_front.png')

    @classmethod
    def on_enter(cls, player):
        player.sprite = Idle.sprite

    def update(self, dt):
        if self.states[YMovementState] is Falling:
            Falling.update(self, dt)
        elif self.states[YMovementState] is Jumping:
            Jumping.update(self, dt)


@state(True)
class Falling(YMovementState):
    @classmethod
    def on_enter(cls, player):
        player.fall_time = 1

    @classmethod
    def on_exit(cls, player):
        player.fall_time = 1

    def update(self, dt):
        self.velocity_y = lambda dt: -(math.log(self.fall_time) - 2) * self.fall_time * -3 / (self.gravity/10)
        self.fall_time += dt

        neighbors = self.model.get_neighbors(*self.tpos)
        if not neighbors['bottom'] and not self.model.get_neighbors(*neighbors['bottom'].tpos)['right']:
            if self.py + self.velocity_y(dt) < neighbors['bottom'].py:
                self.py += self.velocity_y(dt)
            else:
                self.py = neighbors['bottom'].py
        else:
            self.exit(Falling)


@state()
class OnGround(YMovementState):
    pass


@state()
class Jumping(YMovementState):
    @classmethod
    def on_enter(cls, player):
        player.velocity_y = lambda dt: -math.log(player.jump_time) * dt//2
        player.jump_start = player.py
        player.jump_time = 1

    @classmethod
    def on_exit(cls, player):
        player.jump_start = player.py
        player.jump_time = 1

    def update(self, dt):
        self.velocity_y = lambda dt: ((-self.jump_time * (self.jump_time - self.gravity)) / ((self.gravity / 2) ** 2)) * self.jump_height

        self.jump_time += dt
        new_y = self.jump_start - self.velocity_y(dt)
        neighbors = self.model.get_neighbors(*self.tpos)
        if new_y > self.py:
            if not neighbors['bottom'] and not self.model.get_neighbors(*neighbors['bottom'].tpos)['right']:
                if new_y < neighbors['bottom'].py:
                    self.py = new_y
                else:
                    self.py = neighbors['bottom'].py
            else:
                self.exit(Jumping)
        else:
            if not self.model[self.tpos] and not neighbors['right']:
                self.py = new_y
            else:
                self.enter(Falling)