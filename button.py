import pygame
from pygame.math import Vector2
import constants


class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.text_surface = constants.BUTTON_FONT.render(self.text, True, constants.FONT_COLOR)
        self.color = constants.BOARD_COLOR

        self.width = self.text_surface.get_width() + constants.BUTTON_SPACING*2
        self.height = constants.MARGIN - self.text_surface.get_height() + constants.BUTTON_SPACING*2

        self.pos = Vector2(x, y)

        self.button_rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    def draw_button(self, screen):
        self.button_rect.centery = constants.HEIGHT - constants.UI_HEIGHT/2
        pygame.draw.rect(screen, self.color, self.button_rect, border_radius=1)
        self.draw_text(screen, self.button_rect.centerx, self.button_rect.centery)

    def draw_text(self, screen, x, y):
        text_rect = self.text_surface.get_rect(center=(x, y))
        screen.blit(self.text_surface, text_rect)
