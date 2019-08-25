import pygame
import random
import sys
import os

import GameWindow
import GameObject
import InputHandler
import ImageManager
import GameMap


def main(_):
    pygame.init()

    window = GameWindow.Window('RPG Game', 1366, 768, fullscreen=False)

    input_handler = InputHandler.Input()
    input_handler.set_exit_key(pygame.K_ESCAPE)

    image_manager = ImageManager.ImageManager()
    resources_location = 'res'

    character_layer = GameWindow.Window.LAYER_CHARACTER

    map = GameMap.Map(image_manager, os.path.join(resources_location, 'map.txt'))

    basic_sprite = image_manager.get_sprite(os.path.join(resources_location, 'basic.png'), 4, 4, 32, 32)
    checkpoint_sprite = image_manager.get_image(os.path.join(resources_location, 'checkpoint.png'))

    my_object = GameObject.PlayableCharacter(basic_sprite, 50, 50, 24, 24, layer=character_layer)
    other_object = GameObject.NPCharacter(basic_sprite, 400, 100, 24, 24, layer=character_layer)
    GameObject.InvisibleObject(400, 400, name='invis')

    map_width = map.get_map_tile_width()
    map_height = map.get_map_tile_height()

    checkpoints = list()
    for _ in range(5):
        x = random.randint(1, map_width)
        y = random.randint(1, map_height)

        checkpoints.append(GameObject.Checkpoint(checkpoint_sprite, *map.tile_to_pixel(x, y)))

    map.add_objects(my_object, other_object, *checkpoints)
    window.set_map(map)

    clock = pygame.time.Clock()
    frames = 0
    previous_destination = None
    while not input_handler.exiting:
        clock.tick(30)

        input_handler.update()
        for obj in window.get_objects():
            obj.update(window, input_handler)

        window.draw_frame()
        frames += 1

        if frames == 100:
            other_object.approach(checkpoints[0])
            previous_destination = checkpoints[0]

        elif frames > 100:
            if other_object.at_destination():
                next_destination = previous_destination.get_next_checkpoint()
                other_object.approach(next_destination)
                previous_destination = next_destination


if __name__ == '__main__':
    main(sys.argv[1:])
