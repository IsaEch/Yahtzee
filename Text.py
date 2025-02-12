from pygame import font as Font
class Text(object):

    def __init__(self, message: str, size: int, color: tuple, x: int, y: int):
        self.message = message
        self.font = Font.Font(None, size)
        self.color = color
        self.x = x
        self.y = y

    def draw(self, screen):
        """Draw the text onto the screen at the x and y coordinates from the constructor"""
        text_surface = self.font.render(self.message, True, self.color)
        screen.blit(text_surface, (self.x, self.y))

    def update_message(self, message):
        """Update the message to be displayed"""
        self.message = message
