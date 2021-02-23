import pygame
import random
import json

import utilities
import constants
from wire import Wire
from button import Button
from signal import Signal
from chip import Chip
import itertools


class Board:
    def __init__(self, inputs, outputs):
        self.area = pygame.Rect(constants.MARGIN, constants.MARGIN*1.5, constants.WIDTH - constants.MARGIN * 2, constants.HEIGHT - constants.MARGIN * 2.5)
        self.ui_rect = pygame.Rect(0, constants.HEIGHT - constants.UI_HEIGHT, constants.WIDTH, constants.MARGIN)
        self.border_rect = self.area.copy().inflate(constants.BORDER_WIDTH, constants.BORDER_WIDTH)
        self.textbox_rect = pygame.Rect(self.border_rect.left, constants.MARGIN * 0.25, self.border_rect.width, self.border_rect.top - constants.MARGIN * 0.5)
        
        self.input_buttons = []
        self.output_buttons = []
        self.chip_buttons = []

        self.signal_inputs = []
        self.signal_outputs = []

        self.chips = []
        self.wires = []

        self.create_signals(inputs, outputs)
        self.create_buttons()

    # Removes everything from board
    def clear_board(self, inputs, outputs):
        self.signal_inputs.clear()
        self.signal_outputs.clear()
        self.create_signals(inputs, outputs)

        self.chips.clear()
        self.wires.clear()

        self.chip_buttons.clear()
        self.create_buttons()


    # Creates signals at the start at the edges of the board based on the number of inputs and outputs
    def create_signals(self, inputs, outputs):
        self.signal_inputs.clear()
        self.signal_outputs.clear()

        inputs_radius = constants.SIGNAL_RADIUS
        outputs_radius = constants.SIGNAL_RADIUS

        # Code that resizes radius when the signals are divisible by 8
        for i in range(1, inputs):
            if i % 8 == 0:
                inputs_radius /= 1.5

        for i in range(1, outputs):
            if i % 8 == 0:
                outputs_radius /= 1.5

        # This took way to long to perfect... 
        for i in range(self.area.height):  
            if i % (self.area.height // (inputs + 1)) == 0 and i != 0 and len(self.signal_inputs) < inputs:
                self.signal_inputs.append(Signal(constants.MARGIN, self.area.top + i, inputs_radius))
            if i % (self.area.height // (outputs + 1)) == 0 and i != 0 and len(self.signal_outputs) < outputs:
                self.signal_outputs.append(Signal(constants.WIDTH - constants.MARGIN, self.area.top + i, outputs_radius))

    # Creates buttons based on truth tables available
    def create_buttons(self):
        
        # SIGNAL BUTTONS
        self.input_buttons.append(Button('+', constants.BUTTON_SPACING, constants.MARGIN * 0.25, 20, self.border_rect.top - constants.MARGIN * 0.5))
        self.input_buttons.append(Button('-', constants.BUTTON_SPACING, self.input_buttons[-1].button_rect.bottom + constants.BUTTON_SPACING, 20, self.border_rect.top - constants.MARGIN * 0.5))

        self.output_buttons.append(Button('+', constants.WIDTH - constants.BUTTON_SPACING - constants.MARGIN * 0.25, constants.MARGIN * 0.25, 20, self.border_rect.top - constants.MARGIN * 0.5))
        self.output_buttons.append(Button('-', constants.WIDTH - constants.BUTTON_SPACING - constants.MARGIN * 0.25, self.output_buttons[-1].button_rect.bottom + constants.BUTTON_SPACING, 20, self.border_rect.top - constants.MARGIN * 0.5))


        # CHIP BUTTONS

        self.chip_buttons.append(Button('CREATE', constants.BUTTON_SPACING, self.ui_rect.center[1]))
        buttons_x = constants.BUTTON_SPACING + self.chip_buttons[0].width

        # Load list of all chips in json
        with open(constants.CHIPS_JSON, 'r') as file:
            truth_tables = json.load(file)

        for tt in truth_tables:
            buttons_x += constants.BUTTON_SPACING
            self.chip_buttons.append((Button(tt['name'], buttons_x, self.ui_rect.center[1])))
            buttons_x += self.chip_buttons[tt['index']].width

    def draw_board(self, screen):
        # Background color
        screen.fill(constants.OUTSIDE_COLOR)

        # Playable area
        pygame.draw.rect(screen, constants.BOARD_COLOR, self.area, border_radius=15)

        # Border
        pygame.draw.rect(screen, constants.BORDER_COLOR, self.border_rect, constants.BORDER_WIDTH, border_radius=15)

        # Button layout
        pygame.draw.rect(screen, constants.UI_COLOR, self.ui_rect)

        # Text box
        pygame.draw.rect(screen, constants.BOARD_COLOR, self.textbox_rect)

        # Buttons
        for button in self.chip_buttons:
            button.draw_chip_button(screen)

        for button in self.input_buttons:
            button.draw_signal_button(screen)
        
        for button in self.output_buttons:
            button.draw_signal_button(screen)

        # Draws inputs & outputs
        for signal in self.signal_inputs:
            signal.draw_signal(screen)
        for signal in self.signal_outputs:
            signal.draw_signal(screen)

        # Draws gates
        for chip in self.chips:
            chip.draw_chip(screen)

        # Draws Wires
        for wire in self.wires:
            wire.draw_wire(screen)

    # Connects wires between a selected signal and a signal the mouse is pointing at
    def connect_wires(self, selected_signal, mpos):
        for signal in self.signal_outputs:  # Connect to board outputs
            if signal.check_collision(mpos[0], mpos[1]) and selected_signal is not None and signal != selected_signal:
                for wire in self.wires:
                    if wire.end_signal == signal:
                        self.wires.remove(wire)
                self.wires.append(Wire(selected_signal, signal))
        for chip in self.chips:
            for signal in chip.inputs:  # Connect to gate inputs
                if signal.check_collision(mpos[0],
                                          mpos[1]) and selected_signal is not None and signal != selected_signal:
                    for wire in self.wires:
                        if wire.end_signal == signal:
                            self.wires.remove(wire)
                    self.wires.append(Wire(selected_signal, signal))
            for signal in chip.outputs:  # Connect to gate outputs
                if signal.check_collision(mpos[0],
                                          mpos[1]) and selected_signal is not None and signal != selected_signal:
                    for wire in self.wires:
                        if wire.end_signal == signal:
                            self.wires.remove(wire)
                    self.wires.append(Wire(selected_signal, signal))

    # Goes through all possible objects and deletes them if they're out of bounds
    def delete_outofbounds(self):
        for chip in self.chips:
            if not self.area.contains(chip.chip_rect):
                for signal in chip.inputs:
                    for wire in self.wires:
                        if wire.start_signal == signal:
                            self.wires.remove(wire)
                            wire.end_signal.value = False
                        if wire.end_signal == signal:
                            self.wires.remove(wire)
                            wire.end_signal.value = False
                for signal in chip.outputs:
                    for wire in self.wires:
                        if wire.start_signal == signal:
                            self.wires.remove(wire)
                            wire.end_signal.value = False
                        if wire.end_signal == signal:
                            self.wires.remove(wire)
                            wire.end_signal.value = False
                self.chips.remove(chip)

    # Updates signals of only signals that are not inputting
    def update_signals(self):
        for signal in self.signal_outputs:
            for wire in self.wires:
                if wire.end_signal == signal:
                    signal.value = wire.start_signal.value
        for chip in self.chips:
            for signal in chip.inputs:
                for wire in self.wires:
                    if wire.end_signal == signal:
                        signal.value = wire.start_signal.value
            for signal in chip.outputs:
                for wire in self.wires:
                    if wire.end_signal == signal:
                        signal.value = wire.start_signal.value

    # Enables logic of gates that have wires connected to them
    def activate_chips(self):
        for chip in self.chips:
            for wire in self.wires:
                if wire.end_signal in chip.inputs:
                    chip.logic()

    # Spawns chip in the middle of the board
    def spawn_chip(self, name):
#       Load list of all chips in json
        with open(constants.CHIPS_JSON, 'r') as file:
            truth_tables = json.load(file)

        for tt in truth_tables:
            if tt['name'] == name:
                inputs = len(utilities.string_to_bool(str(list(tt.keys())[-1]))) # Length of the list of the last key of the truth table (inputs)
                outputs = len(utilities.string_to_bool(str(list(tt.values())[-1]))) # Length of the list of the last value of the truth table (outputs)
                self.chips.append(Chip(name, random.randrange(constants.WIDTH*0.25, constants.WIDTH*0.75), random.randrange(constants.HEIGHT*0.25, constants.HEIGHT*0.75), inputs, outputs))
                return

    # Creates a chip and resets board
    def create_chip(self, name):
        values = [False, True]
        all_possible_inputs = list(itertools.product(values, repeat=len(self.signal_inputs)))

        # To get the board to its current state if creating chip failed
        current_inputs = [signal.value for signal in self.signal_inputs]

        truth_inputs = []
        truth_outputs = []

        # Puts in the truth_values 
        for value in all_possible_inputs:
            simulated_output = self.simulate_output(value)
            for output in simulated_output:
                if output:
                    truth_inputs.append(value)
                    truth_outputs.append(simulated_output)

        # If it has no truth inputs, then its an empty chip
        if len(truth_inputs) == 0:
            for i in range(len(self.signal_inputs)):
                self.signal_inputs[i].value = current_inputs[i]
            return


        chip = {
            'index': 0,
            'name': name,
            #'color': random.choice(constants.CHIP_COLORS), - for random using color pallete
            'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        }

        # Appends inputs as string and outputs
        for i in range(len(truth_inputs)):
            chip[str(truth_inputs[i])] = truth_outputs[i]

        # Load list of all chips in json
        with open(constants.CHIPS_JSON, 'r') as file:
            truth_tables = json.load(file)

        # Checks if a truth table with the same name already exists only if the list is not empty
        if truth_tables:
            for tt in truth_tables:
                if tt['name'] == name:
                    return
        
        # Adds index to the chip based on the amount of chips
        chip['index'] = len(truth_tables) + 1

        truth_tables.append(chip)

        # Appends to the json list the new truth table/chip
        with open(constants.CHIPS_JSON, 'w') as file:
            json.dump(truth_tables, file, indent=4)

        # Updates buttons
        self.clear_board(len(self.signal_inputs), len(self.signal_outputs))

    # Returns output of tuple of inputs
    def simulate_output(self, input_tuple):
        all_outputs = []

        # Updates all outputs with the new inputs and puts them in a tuple
        for output in self.signal_outputs:
            count = 0
            
            # Updates inputs based on input_tuple
            for signal in self.signal_inputs:
                signal.value = input_tuple[count]
                count += 1

            # To update the outputs: I literally have no clue why this works
            self.update_signals()

            for _ in self.chips:
                self.activate_chips()
                self.update_signals()
            
            all_outputs.append(output.value)
        
        return tuple(all_outputs)
