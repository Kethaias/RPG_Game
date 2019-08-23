import pygame
import sys
import os

import GameWindow
import GameObject
import InputHandler
import ImageManager
import GameMap


def main(_):
    pygame.init()

    window = GameWindow.Window('RPG Game', 1920, 1080)

    input_handler = InputHandler.Input()
    input_handler.set_exit_key(pygame.K_ESCAPE)
    clock = pygame.time.Clock()

    image_manager = ImageManager.ImageManager()
    resources_location = 'res'

    background_layer = GameWindow.Window.LAYER_BACKGROUND
    foreground_layer = GameWindow.Window.LAYER_FOREGROUND

    map = GameMap.Map(image_manager, os.path.join(resources_location, 'map.txt'), layer=background_layer)

    basic_sprite = image_manager.get_sprite(os.path.join(resources_location, 'basic.png'), 4, 4, 32, 32)

    my_object = GameObject.PlayableCharacter(basic_sprite, 50, 50, 24, 24, layer=foreground_layer)
    other_object = GameObject.AnimatedObject(basic_sprite, 50, 100, 24, 24, layer=foreground_layer)

    map.add_objects(my_object, other_object)
    map.track(my_object)
    window.set_map(map)

    while not input_handler.exiting:
        clock.tick(30)

        input_handler.update()
        for obj in window.get_objects():
            obj.update(window, input_handler)

        window.draw_frame()


if __name__ == '__main__':
    main(sys.argv[1:])
