import os

import ImageManager


class Tileset:
    def __init__(self, image_manager: ImageManager.ImageManager, file_path, tile_size):
        self.tiles = []

        with open(file_path, 'r') as in_file:
            image_path = in_file.readline().strip()
            image_path = os.path.join(os.path.dirname(file_path), image_path)

            image = None
            y = -1
            for line in in_file:
                x = 0
                y += 1
                line = line.strip()
                self.tiles.append([])

                if image is None:
                    self.width = len(line.split())
                    image = image_manager.get_sprite(image_path, self.width, sprite_width=tile_size, sprite_height=tile_size)

                for part in line.split():
                    solid = None
                    if part == '0':
                        solid = False

                    elif part == '1':
                        solid = True

                    self.tiles[-1].append(Tile(image[y][x], solid))
                    x += 1

    def get_tile(self, x, y):
        return self.tiles[y][x]

    def get_width(self):
        return self.width


class Tile:
    def __init__(self, image, solid):
        self.image = image
        self.solid = solid

    def get_image(self):
        return self.image

    def is_solid(self):
        return self.solid
