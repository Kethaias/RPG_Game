import pygame


class Input:
    def __init__(self):
        self.keys = set()
        self.exiting = False
        self.exit_key = None

    def set_exit_key(self, exit_key):
        self.exit_key = exit_key

    def is_key_pressed(self, key_code):
        return key_code in self.keys

    def update(self):
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                self.keys.add(event.key)

            elif event.type == pygame.KEYUP:
                self.keys.remove(event.key)

            elif event.type == pygame.QUIT:
                self.exiting = True

        if self.exit_key is not None and self.is_key_pressed(self.exit_key):
            self.set_exiting()

    def set_exiting(self):
        self.exiting = True
