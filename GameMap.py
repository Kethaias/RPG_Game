import pygame
import os

import GameObject
import Camera
import Tileset


class MapTile(GameObject.Object):
    def __init__(self, x, y, tile):
        self.tile = tile
        super().__init__(tile.get_image(), x, y)

    def is_solid(self):
        return self.tile.is_solid()


class Map(GameObject.Object):
    def __init__(self, image_manager, path, sprite_size=32, layer=None):
        self.map_tiles = []
        self.sprite = None
        self.sprite_size = sprite_size
        self.camera = Camera.Camera()
        self.tracking = None
        self.objects = dict()

        with open(path, 'r') as in_file:
            tileset_path = in_file.readline().strip()
            tileset_path = os.path.join(os.path.dirname(path), tileset_path)
            self.tileset = Tileset.Tileset(image_manager, tileset_path, sprite_size)
            tileset_width = self.tileset.get_width()

            for y, line in enumerate(in_file):
                line = line.strip()
                self.map_tiles.append([])

                for x, part in enumerate(line.split()):
                    int_part = int(part)
                    tileset_x = int_part % tileset_width
                    tileset_y = int_part // tileset_width

                    tile = MapTile(x, y, self.tileset.get_tile(tileset_x, tileset_y))

                    self.map_tiles[-1].append(tile)

        super().__init__(self.get_sprite(), 0, 0, name=os.path.basename(path), layer=layer)

    def redraw(self):
        map_height = len(self.map_tiles) * self.sprite_size
        map_width = len(self.map_tiles[0]) * self.sprite_size

        self.sprite = pygame.Surface((map_width, map_height))

        for y in range(len(self.map_tiles)):
            for x in range(len(self.map_tiles[y])):
                self.sprite.blit(self.map_tiles[y][x].get_sprite(), self.tile_to_pixel(x, y))

    def tile_to_pixel(self, x, y):
        return x * self.sprite_size, y * self.sprite_size

    def pixel_to_tile(self, x, y):
        return x // self.sprite_size, y // self.sprite_size

    def is_pixel_solid(self, x, y):
        return self.is_tile_solid(*self.pixel_to_tile(x, y))

    def is_tile_solid(self, x, y):
        if y >= len(self.map_tiles) or x >= len(self.map_tiles[y]):
            return True

        return self.map_tiles[y][x].is_solid()

    def get_sprite(self):
        if self.sprite is None:
            self.redraw()

        return self.sprite

    def draw(self, window):
        if self.tracking:
            self.camera.center(self.tracking, window)

        self.x = -self.camera.x
        self.y = -self.camera.y

        super().draw(window)

    def track(self, obj):
        self.tracking = obj

    def add_objects(self, *objects):
        for o in objects:
            self.objects[o.name] = o
            o.set_map(self)

    def remove_objects(self, *objects):
        for o in objects:
            del(self.objects[o.name])
            o.set_map(None)

    def get_objects(self):
        return self.objects.values()

    def is_solid(self):
        return False
