import pygame
import collections

import GameObject


class Window:
    LAYER_INVISIBLE = -1

    LAYER_BACKGROUND = 1
    LAYER_FOREGROUND = 2
    LAYER_CHARACTER = 3

    LAYER_STATIC = 10

    def __init__(self, name, width, height, background_color=(0, 0, 0), fullscreen=False):
        self._window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)

        display_type = pygame.DOUBLEBUF
        if fullscreen:
            display_type |= pygame.FULLSCREEN

        pygame.display.set_mode((0, 0), display_type)

        self.height = height
        self.width = width
        self.objects = collections.defaultdict(collections.OrderedDict)
        self.background_color = background_color
        self.current_map = None

    def add_object(self, obj: GameObject.Object):
        for objects in self.objects.values():
            existing_object = objects.get(obj.name)
            if existing_object:
                if obj is existing_object:
                    return

                raise RuntimeError('Attempt to add duplicate object with uid \'{uid}\''.format(uid=obj.name))

        self.objects[obj.layer][obj.name] = obj
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

            pygame.display.flip()

    def set_map(self, game_map):
        if self.current_map is not None:
            for o in self.current_map.get_objects():
                self.remove_object(o.name)

            self.remove_object(self.current_map.name)

        self.current_map = game_map
        for o in game_map.get_objects():
            self.add_object(o)

        self.add_object(game_map)
