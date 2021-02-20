import pygame

import constants


class Wire:
    def __init__(self, start_signal, end_signal):
        self.start_signal = start_signal
        self.end_signal = end_signal

    # Draws wire according to start signal value
    def draw_wire(self, screen):
        if not self.start_signal.value:
            pygame.draw.line(screen, constants.SIGNAL_OFF_COLOR, self.start_signal.pos, self.end_signal.pos, constants.WIRE_WIDTH)
        else:
            pygame.draw.line(screen, constants.SIGNAL_ON_COLOR, self.start_signal.pos, self.end_signal.pos, constants.WIRE_WIDTH)