import pygame


class ImageManager:
    def __init__(self):
        self.images = {}

    def get_image(self, path):
        image = self.images.get(path)
        if image is not None:
            return image

        image = pygame.image.load(path)
        self.images[path] = image
        return image

    def get_sprite(self, path, x, y, sprite_width, sprite_height):
        return ImageManager.split(self.get_image(path), x, y, sprite_width, sprite_height)

    @staticmethod
    def split(img, x, y, convert_sprite_width=None, convert_sprite_height=None):
        ret = []
        sprite_width = img.get_width() / x
        sprite_height = img.get_height() / y
        for x_pos in range(x):
            for y_pos in range(y):
                if x_pos == 0:
                    ret.append([])

                sprite_img = img.subsurface(x_pos * sprite_width, y_pos * sprite_height, sprite_width, sprite_height)

                if convert_sprite_width is not None and convert_sprite_height is not None:
                    sprite_img = pygame.transform.scale(sprite_img, (convert_sprite_width, convert_sprite_height))

                ret[y_pos].append(sprite_img)

        return ret
