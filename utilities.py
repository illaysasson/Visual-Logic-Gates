import constants
import re


def draw_text(screen, text, x, y):
    text_surface = constants.BUTTON_FONT.render(text, True, constants.FONT_COLOR)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


# Turns a string of a boolean tuple into the boolean tuple
def string_to_bool(string):
    string = re.sub(r'[()]', '', string) # Removes ()
    string = re.sub(r',', '', string) # Removes ,
    string = string.split(" ") # Splits the strings into the different boolean expressions
    result = tuple([value == 'True' for value in string]) # Turns into a tuple

    return result

# Turns a boolean tuple into a string
def bool_to_string(boolean):
    result = str(boolean)

    # Assigns a , at the end only if the tuple is not a single boolean
    if len(boolean) > 1:
        result = result[:-1] + ',)'
    return result