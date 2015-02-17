#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame as pg
from pygame.locals import *

pg.font.init()

from src.constants import *
from src.tools import load_tile_size_image


class GameView(pg.Surface):
    def __init__(self, views, size=(SCREEN_W, SCREEN_H)):
        super().__init__(size)
        self.views = views

    def render(self):
        for view, pos in self.views:
            view.render()
            self.blit(view, pos)


class MapView(pg.Surface):
    def __init__(self, map_model, size=(SCREEN_W, SCREEN_H)):
        super().__init__(size)
        self.model = map_model

    def render(self):
        self.fill(0x4088DD)
        chunks = slice(
            max(self.model.player.tx//CHUNK_W-CHUNK_IN_SCREEN//2, 0),
            min(self.model.player.tx//CHUNK_W+CHUNK_IN_SCREEN//2+1, len(self.model))
        )
        print(chunks)
        for chunk in self.model[chunks]:
            for tile in chunk.tiles():
                if tile.px in range(
                    self.model.xfov.start - TILE_W,
                    self.model.xfov.stop + TILE_W
                ) and tile.py in range(
                    self.model.yfov.start - TILE_H,
                    self.model.yfov.stop + TILE_H
                ):
                    self.blit(
                        tile.block.texture,
                        (
                            tile.px - self.model.xfov.start,
                            tile.py - self.model.yfov.start
                        )
                    )
        x = sorted((0, self.model.player.px - self.model.xfov.start, self.model.width * TILE_W))[1]
        y = sorted((0, self.model.player.py - self.model.yfov.start, self.model.height * TILE_H))[1]
        self.blit(self.model.player.sprite, (x, y))


class SelectorView(pg.Surface):
    def __init__(self, selector_model, size=(SCREEN_W, SCREEN_H)):
        super().__init__(size)
        self.model = selector_model
        self.set_colorkey(0x123456)

    def render(self):
        self.fill(0x123456)
        self.model.update()
        pg.draw.rect(
            self, 0xFFDDDD,
            (
                self.model.selected_tile.px - self.model.model.xfov.start,
                self.model.selected_tile.py - self.model.model.yfov.start
            ) + TILE_S, 1
        )


class HotBarView(pg.Surface):
    slot_texture = load_tile_size_image('src/assets/gui/hotbar_slot.png')
    selected_texture = load_tile_size_image('src/assets/gui/hotbar_slot_selected.png')
    count_font = pg.font.Font('src/assets/gui/DimitriBlack.ttf', 16)

    def __init__(self, hotbar_model, size=(TILE_W * 9, TILE_H)):
        super().__init__(size)
        self.model = hotbar_model
        self.set_colorkey(0x123456)

    def render(self):
        self.fill(0x123456)
        for i in range(0, self.model.length):
            if i == self.model.selected:
                self.blit(HotBarView.selected_texture, (i * TILE_W, 0))
            else:
                self.blit(HotBarView.slot_texture, (i * TILE_W, 0))
        for i, (item, count) in enumerate(self.model.items()):
            count_display = HotBarView.count_font.render(str(count), False, pg.Color(0, 0, 0, 255))
            self.blit(item.icon, (i * TILE_W + (TILE_W * 0.15), TILE_H * 0.15))
            self.blit(
                count_display,
                (
                    i * TILE_W + (TILE_W * 0.15),
                    TILE_H * 0.15 + TILE_H - HotBarView.count_font.get_linesize() - 8
                )
            )
