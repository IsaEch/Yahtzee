import pygame


class Button(object):

    def __init__(self, x: int, y: int, width: int, height: int, text: str, font: pygame.font, color: tuple,
                 text_color: tuple, disabled=False):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
        self.disabled = disabled

    def draw(self, screen: pygame.Surface):
        """Draws the buttons for each category on the screen but transparently"""

        button = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        # Set the button color to be transparent
        button.fill((*self.color, 128))
        screen.blit(button, self.rect)

        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)

        # Center text inside the button
        text_rect = text_surface.get_rect(center=self.rect.center)

        # Draw the text
        screen.blit(text_surface, text_rect)

    def is_clicked(self):
        # Check if the button is pressed, true if it is, false if it isn't
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

