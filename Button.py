import pygame


class Button(object):

    def __init__(self, x: int, y: int, width: int, height: int, text: str, font: pygame.font, color: tuple,
                 text_color: tuple, disabled=False, transparent=False, hidden=False):
        """Initializes the Button object that will be used to create buttons on the screen to interact with the user
        :args:
            :param x: int: x-coordinate of the button
            :param y: int: y-coordinate of the button
            :param width: int: width of the button
            :param height: int: height of the button
            :param text: str: text to be displayed on the button
            :param font: pygame.font: font to be used for the text
            :param color: tuple: color of the button
            :param text_color: tuple: color of the text
            :param disabled: bool: True if the button is to be disabled, False otherwise
            :param transparent: bool: True if the button is to be transparent, False otherwise
            :param hidden: bool: True if the button is to be hidden, False otherwise
        """
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.button_name = " "
        self.text_color = text_color
        self.disabled = disabled
        self.transparent = transparent
        self.hidden = hidden

    def draw(self, screen: pygame.Surface):
        """Draws the buttons for each category and the roll button on the screen but the category buttons are
        transparent

        :param screen: pygame.Surface object to draw the buttons on

        """
        if not self.hidden:
            button = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            # Set the button color to be transparent
            if self.transparent:
                button.fill((*self.color, 128))
            else:
                button.fill(self.color)
            screen.blit(button, self.rect)

            # Render the text
            text_surface = self.font.render(self.text, True, self.text_color)

            # Center text inside the button
            text_rect = text_surface.get_rect(center=self.rect.center)

            # Draw the text
            screen.blit(text_surface, text_rect)

    def is_clicked(self):
        """
        This function checks the position of the cursor when the left mouse button is clicked

        :returns:
            bool: True if the button is clicked, False otherwise
        """
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]

    def is_hovered(self):
        """The function checks the position of the cursor when the mouse is moved

        :returns:
            bool: True if the cursor is on the button, False otherwise
        """
        return self.rect.collidepoint(pygame.mouse.get_pos())
