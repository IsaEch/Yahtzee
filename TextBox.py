import pygame
import Constants as C


class TextBox(object):

    def __init__(self, x, y, width, height, font):
        """Initializes the TextBox object that will be used to create a text box on the screen for user input
        :args:
            :param x: int: x-coordinate of the text box
            :param y: int: y-coordinate of the text box
            :param width: int: width of the text box
            :param height: int: height of the text box
            :param font: pygame.font: font to be used for the text
        """
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = ''
        self.txt_surface = self.font.render(self.text, True, C.WHITE_COLOR)
        self.active = False
        self.color = C.GREY_COLOR  # Default outline color

    def handle_event(self, event):
        """Capture the user's input and updates the text surface"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicks on the text box, it becomes active and changes color
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            # Change color depending on active status
            if self.active:
                self.color = C.WHITE_COLOR
            else:
                self.color = C.GREY_COLOR
        if event.type == pygame.KEYDOWN:
            if self.active:
                # Capture the user's input and update the text surface
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # Remove the last character when backspace is pressed
                else:
                    self.text += event.unicode  # Add the character to the text when any other key is pressed
                # Update the text surface with the new text so that it doesn't appear blank
                self.txt_surface = self.font.render(self.text, True, C.WHITE_COLOR)

    def clear_text(self):
        """Clear the text in the text box"""
        self.text = ''
        self.txt_surface = self.font.render(self.text, True, C.WHITE_COLOR)

    def draw(self, screen):
        """Draw the text box on the screen

        :param screen: pygame.Surface object to draw the text box on"""
        screen.blit(self.txt_surface, (self.rect.x + C.TEXTBOX_X_OFFSET, self.rect.y + C.TEXTBOX_Y_OFFSET))
        pygame.draw.rect(screen, self.color, self.rect, C.TEXT_BOX_WIDTH)
