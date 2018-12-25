import pygame
import os

import GameObject


class Tile(GameObject.Object):
    def __init__(self, x, y, image):
        super().__init__(image, x, y)


class Map(GameObject.Object):
    def __init__(self, image_manager, path, tileset_width=8, sprite_size=32):
        self.map = []
        self.sprite = None
        self.sprite_size = sprite_size
        with open(path, 'r') as in_file:
            tileset_path = in_file.readline().strip()
            tileset_path = os.path.join(os.path.dirname(path), tileset_path)

            self.tileset = image_manager.get_sprite(tileset_path, tileset_width, sprite_width=sprite_size, sprite_height=sprite_size)

            for y, line in enumerate(in_file):
                line = line.strip()
                self.map.append([])

                for x, part in enumerate(line.split()):
                    int_part = int(part)
                    tileset_x = int_part % tileset_width
                    tileset_y = int_part // tileset_width

                    tile = Tile(x, y, self.tileset[tileset_y][tileset_x])

                    self.map[-1].append(tile)

        super().__init__(self.get_sprite(), 0, 0)

    def redraw(self):
        map_height = len(self.map) * self.sprite_size
        map_width = len(self.map[0]) * self.sprite_size

        self.sprite = pygame.Surface((map_width, map_height))

        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                self.sprite.blit(self.map[y][x].get_sprite(), self.tile_to_pixel(x, y))

    def tile_to_pixel(self, x, y):
        return x * self.sprite_size, y * self.sprite_size

    def pixel_to_tile(self, x, y):
        return x // self.sprite_size, y // self.sprite_size

    def get_sprite(self):
        if self.sprite is None:
            self.redraw()

        return self.sprite
