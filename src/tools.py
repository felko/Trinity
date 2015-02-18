#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from src.constants import *


class Locatable:
    @property
    def tpos(self):
        return self.x // TILE_W, self.y // TILE_H

    @tpos.setter
    def tpos(self, value):
        self.tx, self.ty = map(int, value)

    @property
    def tx(self):
        return self.x // TILE_W

    @tx.setter
    def tx(self, value):
        self.x = int(value * TILE_W)

    @property
    def ty(self):
        return self.y // TILE_H

    @ty.setter
    def ty(self, value):
        self.y = int(value * TILE_H)

    @property
    def ppos(self):
        return self.x, self.y

    @ppos.setter
    def ppos(self, value):
        self.x, self.y = map(int, value)

    @property
    def px(self):
        return self.x

    @px.setter
    def px(self, value):
        self.x = int(value)

    @property
    def py(self):
        return self.y

    @py.setter
    def py(self, value):
        self.y = int(value)


def load_tile_size_image(path):
    path = normalize_path(path)
    try:
        img = pg.transform.scale(pg.image.load(path).convert_alpha(), TILE_S)
    except pg.error:
        img = pg.transform.scale(pg.image.load(normalize_path('src/assets/texture/tile/unknown.png')).convert_alpha(), TILE_S)
    return img


def load_item_icon(path):
    path = normalize_path(path)
    try:
        img = pg.transform.scale(pg.image.load(path).convert_alpha(), tuple(map(int, (TILE_W / 1.3, TILE_H / 1.3))))
    except pg.error:
        img = pg.transform.scale(pg.image.load(normalize_path('src/assets/texture/tile/unknown.png')).convert_alpha(),
                                 tuple(map(int, (TILE_W / 1.3, TILE_H / 1.3))))
    return img


def load_sound(path):
    sound = pg.mixer.Sound(normalize_path(path))
    sound.set_volume(SOUND_VOLUME)
    return sound


def normalize_path(path):
    return os.path.join(*path.split('/'))