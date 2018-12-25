import pygame

import GameObject

class Camera:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def center(self, obj, window):
        self.x = obj.x + (obj.width - window.get_width()) // 2
        self.y = obj.y + (obj.height - window.get_height()) // 2
