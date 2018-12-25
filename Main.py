import pygame
import sys
import os

import GameWindow
import GameObject
import InputHandler
import ImageManager


def main(_):
    pygame.init()

    window = GameWindow.Window('RPG Game', 400, 300)
    input_handler = InputHandler.Input()
    clock = pygame.time.Clock()
    image_manager = ImageManager.ImageManager()
    resources_location = 'res'

    basic_sprite = image_manager.get_sprite(os.path.join(resources_location, 'basic.png'), 4, 4, 32, 32)
    my_object = GameObject.PlayableCharacter(basic_sprite, 10, 10, 32, 32)
    window.add_object('basic_object', my_object)

    while not input_handler.exiting:
        clock.tick(30)

        input_handler.update()
        for obj in window.get_objects():
            obj.update(window, input_handler)

        window.draw_frame()


if __name__ == '__main__':
    main(sys.argv[1:])