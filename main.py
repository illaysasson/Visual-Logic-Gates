import sys
import pygame

from board import Board
import constants
import pygame_textinput

sys.path.append('signal')

FPS = 60

pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption('Visual Logic Gates')


def main():
    # Runs & Sets clock
    pygame.init()
    run = True
    clock = pygame.time.Clock()
    board = Board(2, 1)

    # Variables to check actions
    selected_chip = None
    selected_signal = None
    left_clicking = False
    right_clicking = False

    # Text input
    textinput = pygame_textinput.TextInput(font_family='sprites/Manrope-Medium.otf', font_size=constants.TEXTBOX_FONT_SIZE, text_color=constants.FONT_COLOR, antialias=True, max_string_length=40)
    new_chip_name = ''

    while run:
        clock.tick(FPS)
        mpos = pygame.mouse.get_pos()

        # Moves gate center to mouse when dragging
        if left_clicking and selected_chip is not None:
            selected_chip.move(mpos[0] - selected_chip.width / 2, mpos[1] - selected_chip.height / 2)

        # Deletes out of bounds objects
        board.delete_outofbounds()

        events = pygame.event.get()

        for event in events:
            # Quitting the game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            # Pressing mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Left click
                if event.button == 1:
                    # Selects gate that collides with mouse
                    for chip in board.chips:
                        if chip.chip_rect.collidepoint(mpos):
                            selected_chip = chip
                            left_clicking = True
                    # Turns on/off signal if mouse collides with input
                    for signal in board.signal_inputs:
                        if signal.check_collision(mpos[0], mpos[1]):
                            signal.value = not signal.value 
                    # Click a button to spawn a new gate
                    left_clicking = True
                    for button in board.buttons:
                        if button.button_rect.collidepoint(mpos) and left_clicking:
                            if button.text == 'CREATE':
                                if new_chip_name != '':
                                    board.create_chip(new_chip_name.upper())
                                left_clicking = False
                                textinput.clear_text()
                            else:
                                left_clicking = False
                                board.spawn_chip(button.text)

                        
                # Middle click
                if event.button == 2:
                    # Removes wires that start with the signal you're middle clicking on
                    for signal in board.signal_inputs:
                        if signal.check_collision(mpos[0], mpos[1]):
                            for wire in board.wires:
                                if wire.start_signal == signal:
                                    board.wires.remove(wire)
                                    wire.end_signal.value = False
                    for chip in board.chips:
                        for signal in chip.outputs:
                            if signal.check_collision(mpos[0], mpos[1]):
                                for wire in board.wires:
                                    if wire.start_signal == signal:
                                        board.wires.remove(wire)
                                        wire.end_signal.value = False
                # Right click
                if event.button == 3:
                    # Selects signal in board inputs for drawing a line
                    for signal in board.signal_inputs:
                        if signal.check_collision(mpos[0], mpos[1]):
                            right_clicking = True
                            selected_signal = signal
                    # Selects signal in gate outputs for drawing a line
                    for chip in board.chips:
                        for signal in chip.outputs:
                            if signal.check_collision(mpos[0], mpos[1]):
                                right_clicking = True
                                selected_signal = signal

            # Releasing left mouse to drop object
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    left_clicking = False
                    selected_chip = None
                if event.button == 3:
                    right_clicking = False
                    board.connect_wires(selected_signal, mpos)
                    selected_signal = None

        board.update_signals()
        board.activate_chips()
        board.draw_board(screen)

        # Inputting text
        if textinput.update(events):
            print(len(textinput.get_text()))
        new_chip_name = textinput.get_text()

        screen.blit(textinput.get_surface(), (board.textbox_rect.left + constants.BUTTON_SPACING, board.textbox_rect.top))

        # Draws a temp wire between the signal and the mouse
        if right_clicking and selected_signal is not None:
            pygame.draw.line(screen, constants.SIGNAL_OFF_COLOR, selected_signal.pos, mpos, constants.WIRE_WIDTH)
            pygame.draw.circle(screen, constants.SIGNAL_OFF_COLOR, mpos, constants.WIRE_WIDTH)

        pygame.display.update()


main()
