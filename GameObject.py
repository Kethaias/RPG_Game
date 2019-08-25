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
        self.layer = layer or GameWindow.Window.LAYER_INVISIBLE
        self.solid = True
        self.static_position = False

        if name is None:
            name = Object.next_id
            Object.next_id += 1

        self.name = name

    def move(self, x, y, check_collision=None):
        if check_collision is None:
            check_collision = self.is_solid

        if check_collision and self.would_collide(x, y):
            return False

        self.x += x
        self.y += y

        return True

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window):
        if self.layer is None or self.layer < 0:
            return

        sprite = self.get_sprite()
        if sprite is None:
            return

        adjust_camera = not self.static_position
        window.blit(sprite, self.top_left(adjust_camera=adjust_camera))

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

            if not o.is_solid():
                continue

            if self.get_rect().colliderect(o.get_rect()):
                return True

        return False

    def is_solid(self):
        return self.solid

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
            self.next_frame = 0
            return

        self.next_frame = (self.next_frame + 1) % (self.animation_frames * len(self.sprite[self.direction]))

    def set_direction(self, direction):
        if self.direction == direction:
            return

        self.direction = direction
        self.next_frame = 0

    def is_moving(self):
        return True


class NPCharacter(AnimatedObject):
    def __init__(self, sprite, x, y, width=None, height=None, name=None, layer=None):
        super().__init__(sprite, x, y, width, height, name=name, layer=layer)
        self.target_x = None
        self.target_y = None
        self.currently_moving = False
        self.speed = 1.5
        self.approaching = None

    def update(self, window, input_handler):
        self.currently_moving = False

        if self.approaching is not None:
            self.target_x = self.approaching.x
            self.target_y = self.approaching.y

        move_x = 0
        direction = self.direction
        if self.target_x is not None:
            move_x = self.target_x - self.x
            if move_x != 0:
                self.currently_moving = True
                if abs(move_x) > self.speed:
                    move_x = self.speed if move_x > 0 else -self.speed

                if move_x > 0:
                    direction = 3

                else:
                    direction = 2

        move_y = 0
        if self.target_y is not None:
            move_y = self.target_y - self.y
            if move_y != 0:
                self.currently_moving = True
                if abs(move_y) > self.speed:
                    move_y = self.speed if move_y > 0 else -self.speed

                if move_y > 0:
                    direction = 0

                else:
                    direction = 1

        if self.approaching is not None and move_x == 0 and move_y == 0:
            self.approaching = None

        self.set_direction(direction)
        self.move(move_x, move_y)
        super().update(window, input_handler)

    def move_to(self, x, y):
        self.target_x = x
        self.target_y = y

    def teleport_to(self, x, y):
        super().move_to(x, y)

    def is_moving(self):
        return self.currently_moving

    def approach(self, obj):
        self.approaching = obj

    def at_destination(self):
        return self.approaching is None


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

        self.move(move_x, move_y)

    def is_moving(self):
        return self.currently_moving


class InvisibleObject(Object):
    def __init__(self, x, y, name=None, solid=False):
        super().__init__(None, x-1, y-1, width=2, height=2, name=name)
        self.solid = solid


class StaticObject(Object):
    def __init__(self, sprite, x, y, width=None, height=None, name=None):
        super().__init__(sprite, x, y, width=width, height=height, name=name, layer=GameWindow.Window.LAYER_STATIC)
        self.static_position = True


class Checkpoint(Object):
    next_id = 0
    checkpoints = list()

    def __init__(self, sprite, x, y):
        name = 'checkpoint_{id}'.format(id=Checkpoint.next_id)
        Checkpoint.next_id += 1
        Checkpoint.checkpoints.append(self)

        super().__init__(sprite, x, y, 10, 10, name=name, layer=GameWindow.Window.LAYER_FOREGROUND)

        self.solid = False

    def get_next_checkpoint(self):
        self_index = Checkpoint.checkpoints.index(self)
        next_index = self_index + 1

        if next_index >= len(Checkpoint.checkpoints):
            next_index = 0

        return Checkpoint.checkpoints[next_index]
