import pygame

import GameWindow


class Object:
    next_id = 0

    def __init__(self, sprite, x, y, width=None, height=None, name=None, layer=None):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.width = width or self.get_sprite().get_width()
        self.height = height or self.get_sprite().get_height()
        self.map = None
        self.layer = layer

        if name is None:
            name = Object.next_id
            Object.next_id += 1

        self.name = name

    def move(self, x, y, check_collision=False):
        if check_collision and self.would_collide(x, y):
            return

        self.x += x
        self.y += y

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window):
        window.blit(self.get_sprite(), self.top_left(adjust_camera=True))

    def get_sprite(self):
        return self.sprite

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def _size(self):
        return self.width, self.height

    def top_left(self, adjust_camera=False):
        if adjust_camera and self.map and self.map.camera:
            return self.x - self.map.camera.x, self.y - self.map.camera.y

        return self.x, self.y

    def top_right(self):
        return self.x + self.width, self.y

    def bottom_left(self):
        return self.x, self.y + self.height

    def bottom_right(self):
        return self.x + self.width, self.y + self.height

    def center(self):
        return (self.x + self.width) // 2, (self.y + self.height) // 2

    def update(self, window, input_handler):
        pass

    def added(self, window):
        pass

    def removed(self, window):
        pass

    def would_collide(self, add_x, add_y):
        old_x = self.x
        old_y = self.y

        self.x += add_x
        self.y += add_y

        ret = self.is_colliding()

        self.x = old_x
        self.y = old_y

        return ret

    def is_colliding(self):
        for corner in {self.top_left(), self.top_right(), self.bottom_left(), self.bottom_right()}:
            if self.map.is_pixel_solid(*corner):
                return True

        for o in self.map.get_objects():
            if o is self:
                continue

            if not o.is_solid:
                continue

            if self.get_rect().colliderect(o.get_rect()):
                return True

        return False

    def is_solid(self):
        return True

    def set_map(self, game_map):
        self.map = game_map


class AnimatedObject(Object):
    def __init__(self, sprite, x, y, width=None, height=None, name=None, layer=None):
        self.next_frame = 0
        self.direction = 0
        self.animation_frames = 8
        self.speed = 5

        super().__init__(sprite, x, y, width, height, name=name, layer=layer)

    def get_sprite(self):
        return self.sprite[self.direction][self.next_frame // self.animation_frames]

    def update(self, window, input_handler):
        if not self.is_moving():
            return

        self.next_frame = (self.next_frame + 1) % (self.animation_frames * len(self.sprite[self.direction]))

    def set_direction(self, direction):
        if self.direction == direction:
            return

        self.direction = direction
        self.next_frame = 0

    def is_moving(self):
        return True


class PlayableCharacter(AnimatedObject):
    def __init__(self, sprite, x, y, width=None, height=None, name=None, layer=None):
        super().__init__(sprite, x, y, width, height, name=name, layer=layer)
        self.currently_moving = False

    def update(self, window, input_manager):
        super().update(window, input_manager)

        move_x = 0
        move_y = 0
        if input_manager.is_key_pressed(pygame.K_LEFT):
            self.set_direction(2)
            self.currently_moving = True
            move_x = -self.speed

        elif input_manager.is_key_pressed(pygame.K_RIGHT):
            self.set_direction(3)
            self.currently_moving = True
            move_x = self.speed

        elif input_manager.is_key_pressed(pygame.K_UP):
            self.set_direction(1)
            self.currently_moving = True
            move_y = -self.speed

        elif input_manager.is_key_pressed(pygame.K_DOWN):
            self.set_direction(0)
            self.currently_moving = True
            move_y = self.speed

        else:
            self.currently_moving = False

        self.move(move_x, move_y, check_collision=True)

    def is_moving(self):
        return self.currently_moving
