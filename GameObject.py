import pygame


class Object:
    def __init__(self, sprite, x, y, width=None, height=None):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.width = width or self.get_sprite().get_width()
        self.height = height or self.get_sprite().get_height()
        self.map = None

    def move(self, x, y):
        self.x += x
        self.y += y

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window):
        window.blit(self.get_sprite(), self.top_left(adjust_camera=True))

    def get_sprite(self):
        return self.sprite

    def _rect(self):
        return self.x, self.y, self.width, self.height

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


class AnimatedObject(Object):
    def __init__(self, sprite, x, y, width=None, height=None):
        self.next_frame = 0
        self.direction = 0
        self.animation_frames = 8
        self.speed = 5

        super().__init__(sprite, x, y, width, height)

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
    def __init__(self, sprite, x, y, width=None, height=None):
        super().__init__(sprite, x, y, width, height)
        self.currently_moving = False

    def update(self, window, input_manager):
        super().update(window, input_manager)
        if input_manager.is_key_pressed(pygame.K_LEFT):
            self.set_direction(2)
            self.move(-self.speed, 0)
            self.currently_moving = True

        elif input_manager.is_key_pressed(pygame.K_RIGHT):
            self.set_direction(3)
            self.move(self.speed, 0)
            self.currently_moving = True

        elif input_manager.is_key_pressed(pygame.K_UP):
            self.set_direction(1)
            self.move(0, -self.speed)
            self.currently_moving = True

        elif input_manager.is_key_pressed(pygame.K_DOWN):
            self.set_direction(0)
            self.move(0, self.speed)
            self.currently_moving = True

        else:
            self.currently_moving = False

    def is_moving(self):
        return self.currently_moving
