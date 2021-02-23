import pygame
import json
from pygame.math import Vector2

import constants
from signal import Signal


class Chip:
    def __init__(self, name, x, y, inputs, outputs):
        self.name = name

        self.pos = Vector2(x, y)
        self.chip_rect = pygame.Rect(self.pos.x, self.pos.y, constants.CHIP_WIDTH, constants.CHIP_HEIGHT)
        self.text_surface = constants.CHIP_FONT.render(self.name, True, constants.FONT_COLOR)

        self.truth_table = self.find_truth_table()
        self.width = self.text_surface.get_width() + constants.CHIP_WIDTH # Width based on text
        self.height = constants.CHIP_HEIGHT * max(inputs, outputs)  # Height based on the largest number of inputs or outputs

        self.inputs = []
        self.outputs = []
        self.create_signals(inputs, outputs)

    def draw_chip(self, screen):
        self.chip_rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        pygame.draw.rect(screen, self.truth_table['color'], self.chip_rect, border_radius=8)
        self.draw_text(screen, self.chip_rect.centerx, self.chip_rect.centery)

        for signal in self.inputs:
            signal.draw_signal(screen)
        for signal in self.outputs:
            signal.draw_signal(screen)

    def draw_text(self, screen, x, y):
        text_rect = self.text_surface.get_rect(center=(x, y))
        screen.blit(self.text_surface, text_rect)

    # Changes gate position and rectangle position based on new coordinates
    def move(self, x, y):
        self.pos = Vector2(x, y)
        self.chip_rect.move(self.pos)

        inputs_count = 0
        outputs_count = 0

        # Changes signal positions
        for i in range(self.height):
            if i % (self.height // (len(self.inputs) + 1)) == 0 and i != 0 and abs(self.height - i) > constants.CHIP_SIGNAL_RADIUS:
                self.inputs[inputs_count].pos = Vector2(x, y + i)
                inputs_count += 1
            if i % (self.height // (len(self.outputs) + 1)) == 0 and i != 0 and abs(self.height - i) > constants.CHIP_SIGNAL_RADIUS:
                self.outputs[outputs_count].pos = Vector2(x + self.width, y + i)
                outputs_count += 1

    # Creates signals on the gate
    def create_signals(self, inputs, outputs):
        # This took way to long to perfect... 
        for i in range(self.height):
            if i % (self.height // (inputs + 1)) == 0 and i != 0 and len(self.inputs) < inputs:
                self.inputs.append(Signal(self.pos.x, self.pos.y + i, constants.CHIP_SIGNAL_RADIUS))
            if i % (self.height // (outputs + 1)) == 0 and i != 0 and len(self.outputs) < outputs:
                self.outputs.append(Signal(self.pos.x + self.width, self.pos.y + i, constants.CHIP_SIGNAL_RADIUS))

    # Changes outputs based on the inputs and a logic table with the same name
    def logic(self):
        tt = self.find_truth_table()
        logic = tuple(input.value for input in self.inputs)

        # Checks if the values are in the truth table
        for i in range(len(self.outputs)):
            if str(logic) in tt:
                self.outputs[i].value = tt[str(logic)][i]
            # If not, assigns everything to false
            else:
                self.outputs[i].value = False

    # Finds a truth table with the same name as the chip
    def find_truth_table(self):
        # Load list of all chips in json
        with open(constants.CHIPS_JSON, 'r') as file:
            truth_tables = json.load(file)

        for tt in truth_tables:
            if tt['name'] == self.name:
                return tt
        return None

    
