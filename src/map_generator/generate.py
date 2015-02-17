# C:\Python34\python.exe
# -*- coding: utf-8 -*-

import random
import itertools as it

from src.map_generator.structs import *
from src.map_generator.chunk import Chunk
from src.constants import *


class Generate(list):
    def __init__(self, headstart, flatness, deniv, size, structs=Structure.structures):
        super().__init__()
        width, height = size

        self.append(
            Chunk(headstart, flatness, deniv, size=(CHUNK_W, height))
        )

        for i in range(width-1):
            print('Generated', i+1, 'chunk.')
            headstart = len(list(it.dropwhile(lambda block: not block, self[-1].column(-1))))

            self.append(
                Chunk(headstart, flatness, deniv, size=(CHUNK_W, height))
            )

        for i, chunk in enumerate(self):
            for tile in chunk.tiles():
                tile.tx += i * CHUNK_W