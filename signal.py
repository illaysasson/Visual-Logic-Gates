import math

from pygame.math import Vector2
from pygame import gfxdraw

import constants


class Signal:
    def __init__(self, x, y, radius):
        self.pos = Vector2(x, y)
        self.value = False
        self.radius = radius

    # Draws anti-aliased signals
    def draw_signal(self, screen):
        if not self.value:
            gfxdraw.aacircle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), constants.SIGNAL_OFF_COLOR)
            gfxdraw.filled_circle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), constants.SIGNAL_OFF_COLOR)
        else:
            gfxdraw.aacircle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), constants.SIGNAL_ON_COLOR)
            gfxdraw.filled_circle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), constants.SIGNAL_ON_COLOR)

    # Checks if object hits the circle using pythagoras
    def check_collision(self, x, y):
        sqx = (x - self.pos.x) ** 2
        sqy = (y - self.pos.y) ** 2

        if math.sqrt(sqx + sqy) < self.radius:
            return True
        return False
