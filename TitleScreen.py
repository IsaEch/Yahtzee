import Constants as C
from Text import Text
from Button import Button
from NameScreen import NameScreen
import pygame


class Title(object):

    def __init__(self):
        """Initializes the Title object with the screen and buttons. The first screen the user sees when running
        the program from main.py"""

        self.screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        pygame.display.set_caption("Yahtzee")
        self.title = Text("Yahtzee", C.TITLE_SIZE, C.WHITE_COLOR, C.SCREEN_WIDTH//2, C.TITLE_Y, centered=True)
        self.subtitle = Text("Use the arrow keys to adjust the total number of players", C.SUBTITLE_SIZE,
                             C.WHITE_COLOR, C.SCREEN_WIDTH//2, C.SUBTITLE_Y, centered=True)
        self.play_button = Button(C.PLAY_X, C.PLAY_Y, C.PLAY_WIDTH, C.PLAY_HEIGHT, "Play", C.FONT, C.GREY_COLOR,
                                  C.WHITE_COLOR)
        self.player_count = 3
        self.decrease_button = Button(C.DECREASE_X, C.DECREASE_Y, C.DECREASE_WIDTH, C.DECREASE_HEIGHT, "<",
                                      C.LARGE_FONT, C.GREY_COLOR, C.WHITE_COLOR)
        self.increase_button = Button(C.INCREASE_X, C.INCREASE_Y, C.INCREASE_WIDTH, C.INCREASE_HEIGHT, ">",
                                      C.LARGE_FONT, C.GREY_COLOR, C.WHITE_COLOR)
        self.num_box = pygame.Rect(C.DECREASE_X + C.DECREASE_WIDTH, C.DECREASE_Y, C.INCREASE_X - C.DECREASE_X
                                   - C.DECREASE_WIDTH, C.INCREASE_HEIGHT)
        self.buttons = [self.play_button, self.decrease_button, self.increase_button]

    def game_loop(self):
        """Runs the game loop for the title screen"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for button in self.buttons:
                    # Change the color of the button if it is hovered over
                    if button.is_hovered() and not button.disabled:
                        button.color = C.LIGHT_GREY_COLOR
                    else:
                        button.color = C.GREY_COLOR
                    if button.disabled:
                        button.color = C.EXTRA_LIGHT_GREY_COLOR
                    # Handle interactions with the screen buttons
                    if button.is_clicked() and not button.disabled and event.type == pygame.MOUSEBUTTONDOWN:
                        # Switch to the player name screen
                        if button == self.play_button:
                            running = False
                            name_screen = NameScreen(self.screen, self.player_count)
                            name_screen.game_loop()
                        # Decrease the player count
                        elif button == self.decrease_button:
                            if self.player_count > 2:
                                self.player_count -= 1
                        # Increase the player count
                        elif button == self.increase_button:
                            if self.player_count < 5:
                                self.player_count += 1
                    if self.player_count == 2:
                        self.decrease_button.disabled = True
                    else:
                        self.decrease_button.disabled = False
                    if self.player_count == 5:
                        self.increase_button.disabled = True
                    else:
                        self.increase_button.disabled = False
            self.draw()

    def draw(self):
        """Draws the title screen with the title and subtitle"""
        # Draw the text
        self.screen.fill(C.BACKGROUND_COLOR)
        self.title.draw(self.screen)
        self.subtitle.draw(self.screen)

        # Draw the buttons
        self.play_button.draw(self.screen)
        self.decrease_button.draw(self.screen)
        self.increase_button.draw(self.screen)

        # Draw the player count and box
        pygame.draw.rect(self.screen, C.GREY_COLOR, self.num_box)
        player_count_text = C.LARGE_FONT.render(str(self.player_count), True, C.WHITE_COLOR)
        player_count_rect = player_count_text.get_rect(center=self.num_box.center)
        self.screen.blit(player_count_text, player_count_rect)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    title = Title()
    title.game_loop()
