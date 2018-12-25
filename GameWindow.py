import pygame
import collections

import GameObject


class Window:
    LAYER_BACKGROUND = 0
    LAYER_FOREGROUND = 1

    def __init__(self, name, width, height, background_color=(0, 0, 0)):
        self._window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        self.height = height
        self.width = width
        self.objects = collections.defaultdict(collections.OrderedDict)
        self.background_color = background_color

    def add_object(self, uid, obj: GameObject.Object, layer):
        for objects in self.objects.values():
            existing_object = objects.get(uid)
            if existing_object:
                if obj is existing_object:
                    return

                raise RuntimeError('Attempt to add duplicate object with uid \'{uid}\''.format(uid=uid))

        self.objects[layer][uid] = obj
        obj.added(self)

    def remove_object(self, uid, safe=False):
        for objects in self.objects.values():
            if uid not in objects:
                continue

            del objects[uid]
            return

        if not safe:
            raise RuntimeError('Attempt to remove object which did not exist \'{obj}\''.format(obj=uid))

    def get_object(self, uid):
        for objects in self.objects.values():
            ret = objects.get(uid)
            if ret is not None:
                return ret

    def get_objects(self, filter_type=None):
        ret = []
        for objects in self.objects.values():
            for obj in objects.values():
                if filter_type is None or isinstance(obj, filter_type):
                    ret.append(obj)

        return ret

    def draw_frame(self):
        self._window.fill(self.background_color)
        for layer in sorted(self.objects):
            for obj in self.objects[layer].values():
                obj.draw(self._window)

            pygame.display.update()
