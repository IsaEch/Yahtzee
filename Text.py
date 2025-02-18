from pygame import font as Font
class Text(object):

    def __init__(self, message: str, size: int, color: tuple, x: int, y: int, centered=False):
        self.message = message
        self.font = Font.Font(None, size)
        self.color = color
        self.x = x
        self.y = y
        self.centered = centered

    def draw(self, screen):
        """Draw the text onto the screen at the x and y coordinates from the constructor"""
        text_surface = self.font.render(self.message, True, self.color)
        if self.centered:
            text_width = text_surface.get_width()
            screen.blit(text_surface, (self.x - text_width // 2, self.y))
            # screen.blit(text_surface, (self.x - len(self.message), self.y))
        else:
            screen.blit(text_surface, (self.x, self.y))

    def update_message(self, message):
        """Update the message to be displayed"""
        self.message = message
