import pygame
from utils import COLORS

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont('Arial', 20, bold=True)

    def draw(self, win):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            color = COLORS['BUTTON_HOVER']
        else:
            color = COLORS['BUTTON_COLOR']

        pygame.draw.rect(win, color, self.rect)
        pygame.draw.rect(win, COLORS['BLACK'], self.rect, 2)

        text_surf = self.font.render(self.text, True, COLORS['TEXT_COLOR'])
        text_rect = text_surf.get_rect(center=self.rect.center)
        win.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)