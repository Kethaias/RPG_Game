import pygame
import collections

import GameObject


class Window:
    def __init__(self, name, width, height, background_color=(0, 0, 0)):
        self._window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        self.height = height
        self.width = width
        self.objects = collections.OrderedDict()
        self.background_color = background_color

    def add_object(self, uid, obj: GameObject.Object):
        existing_object = self.objects.get(uid)
        if existing_object:
            if obj is existing_object:
                return

            raise RuntimeError('Attempt to add duplicate object with uid \'{uid}\''.format(uid=uid))

        self.objects[uid] = obj

    def remove_object(self, uid, safe=False):
        if safe and uid not in self.objects:
            return False

        del self.objects[uid]
        return True

    def get_object(self, uid):
        return self.objects.get(uid)

    def get_objects(self, filter_type=None):
        return [o for o in self.objects.values() if filter_type is None or isinstance(o, filter_type)]

    def draw_frame(self):
        self._window.fill(self.background_color)
        for obj in self.objects.values():
            obj.draw(self._window)

        pygame.display.update()
