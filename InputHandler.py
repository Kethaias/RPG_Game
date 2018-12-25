import pygame


class Input:
    def __init__(self):
        self.keys = set()
        self.exiting = False

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
