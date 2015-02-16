#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src import *


def main():
	map_model = MapModel.generate(128, 64)
	hotbar = HotBar(9)
	player = Player(map_model, 'Patrick', map_model.get_random_spawn_point(), hotbar)
	selector = Selector(map_model)

	view = GameView(
		[
			(MapView(map_model),     (0, 0)),
			(SelectorView(selector), (0, 0)),
			(HotBarView(hotbar),     (SCREEN_W//2-(hotbar.length*TILE_W/1.3)//2, 2))
		]
	)

	game = Game(
		player=player,
		selector=selector,
		model=map_model,
		view=view
	)

	game.start()

if __name__ == '__main__':
	main()