import Constants as C
from Text import Text
from Button import Button
import pygame
from TextBox import TextBox
from Player import Player
from YahtzeeGame import YahtzeeGame


class NameScreen(object):

    def __init__(self, screen, player_count=2):
        self.screen = screen
        self.title = Text("Enter Player 1's Name", C.NS_SIZE, C.WHITE_COLOR, C.SCREEN_WIDTH//2, C.NS_TITLE_Y,
                          centered=True)
        self.name_box = TextBox(C.NS_NAME_X, C.NS_NAME_Y, C.NS_NAME_WIDTH, C.NS_NAME_HEIGHT, C.LARGE_FONT)
        self.enter_button = Button(C.ENTER_X, C.ENTER_Y, C.ENTER_WIDTH, C.ENTER_HEIGHT, "Enter", C.FONT,
                                   C.GREY_COLOR,  C.WHITE_COLOR)
        self.player_count = player_count
        self.player_list = []

    def game_loop(self):
        """Runs the game loop for the player name screen"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.name_box.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN and self.enter_button.is_clicked() and self.name_box.text:
                    name = self.name_box.text.capitalize()
                    player = Player(name)
                    self.player_list.append(player)
                    if len(self.player_list) == self.player_count:
                        running = False
                        game = YahtzeeGame(self.screen, self.player_list)
                        game.start_game()
                    else:
                        self.update_message()
                    self.name_box.clear_text()  # Clears text box after clicking enter
            self.draw()

    def draw(self):
        """Draws the player name screen with the text box and enter button"""
        self.screen.fill(C.BACKGROUND_COLOR)
        self.title.draw(self.screen)
        self.name_box.draw(self.screen)
        self.enter_button.draw(self.screen)
        if self.enter_button.is_hovered():
            self.enter_button.color = C.LIGHT_GREY_COLOR
        else:
            self.enter_button.color = C.GREY_COLOR
        pygame.display.flip()

    def update_message(self):
        """Updates the message on the screen to indicate when to enter the next player's name"""
        self.title.update_message("Enter Player {}'s Name".format(len(self.player_list) + 1))


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
    pygame.display.set_caption("Yahtzee")
    NameScreen(screen).game_loop()
    pygame.quit()
