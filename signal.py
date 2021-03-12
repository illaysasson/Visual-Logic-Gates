import math
import pygame
from pygame.math import Vector2
from pygame import gfxdraw

import constants


class Signal:
    def __init__(self, x, y, radius):
        self.pos = Vector2(x, y)
        self.value = False
        self.radius = radius
        self.highlighted = False

    # Draws anti-aliased signals
    def draw_signal(self, screen):
        if not self.value:
            gfxdraw.aacircle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), constants.SIGNAL_OFF_COLOR)
            gfxdraw.filled_circle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), constants.SIGNAL_OFF_COLOR)
        else:
            gfxdraw.aacircle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), constants.SIGNAL_ON_COLOR)
            gfxdraw.filled_circle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), constants.SIGNAL_ON_COLOR)

        if self.highlighted:
            pygame.draw.circle(screen, pygame.Color('White'), self.pos, self.radius + 1, width=3)

    # Checks if object hits the circle using pythagoras
    def check_collision(self, x, y):
        sqx = (x - self.pos.x) ** 2
        sqy = (y - self.pos.y) ** 2

        if math.sqrt(sqx + sqy) < self.radius:
            return True
        return False
