from Player import Player
import Constants as C
from Text import Text
from Button import Button
import pygame


class YahtzeeGame(object):

    def __init__(self):
        self.players = [Player("Jack")]
        self.current_player = 0
        self.game_started = False
        self.game_finished = False
        self.screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        self.game_name = Text("YAHTZEE", C.FONT_SIZE,  C.BLACK_COLOR, C.YAHTZEE_X, C.YAHTZEE_Y)
        self.player_name = Text(self.players[self.current_player].name, C.FONT_SIZE, C.BLACK_COLOR, C.PLAYER_X,
                                C.PLAYER_Y)
        pygame.display.set_caption(C.CAPTION)
        pygame.display.background = C.BACKGROUND_COLOR
        self.buttons = []

    def start_game(self):
        self.create_buttons()
        self.game_started = True
        self.screen.fill(C.BACKGROUND_COLOR)
        while self.game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_started = False
                for button in self.buttons:
                    if button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                        print("Button clicked")
            self.draw_game()
            pygame.display.flip()

    def draw_game(self):
        # Local variable to hold the current score_card to iterate through
        card = self.players[self.current_player].score_card
        # Draw the score_card
        pygame.draw.rect(self.screen, C.SCORE_CARD_COLOR, (C.SCORE_CARD_X, C.SCORE_CARD_Y, C.SCREEN_WIDTH//2,
                                                           C.SCREEN_HEIGHT - C.SC_BACKGROUND_OFFSET))

        # Draw the grid
        for row in range(card.length() + 3):
            grid_y = C.CELL_HEIGHT * row + (C.SCORE_CARD_OFFSET*2 - C.SC_X_OFFSET)
            pygame.draw.line(self.screen, C.BLACK_COLOR, (C.SCORE_CARD_X + C.SC_GRID_OFFSET, grid_y),
                         (C.SCREEN_WIDTH//2 + C.SCORE_CARD_Y-C.GRID_Y_OFFSET, grid_y))

        for col in range(card.width() + 1):
            # 1st column has a different offset because it needs more room for text
            if col == 0:
                grid_x = C.SCORE_CARD_X + C.SCORE_CARD_OFFSET - C.COL_ONE_OFFSET
            else:
                grid_x = C.SCORE_CARD_X + C.SCORE_CARD_OFFSET + col * (C.SCREEN_WIDTH//2 - 2 * C.SCORE_CARD_OFFSET) // card.width()
            # Adjust line length to fit the card
            pygame.draw.line(self.screen, C.BLACK_COLOR, (grid_x, C.SCORE_CARD_X+C.SC_BEGIN_LENGTH_OFFSET),
                             (grid_x, C.SCREEN_HEIGHT + C.SCORE_CARD_Y - C.SC_END_LENGTH_OFFSET))

        # Draw the score_card values
        for row in range(card.length()):
            for col in range(card.width()):
                # Convert the cell value to a text to be drawn
                cell_value = str(self.players[self.current_player].score_card.score[row][col])
                # Render the text
                cell_text = C.FONT.render(cell_value, True, C.BLACK_COLOR)
                # Draw each cell value on the screen and push text to make space for the 1st column
                if col == 0:
                    x = C.CELL_WIDTH * col + C.SCORE_CARD_OFFSET - C.COL_ONE_OFFSET
                elif row == 10:
                    continue
                else:
                    # Adjust the x position to fit the card
                    x = (C.SCORE_CARD_X + C.SCORE_CARD_OFFSET + col * (C.SCREEN_WIDTH//2 - 2 * C.SCORE_CARD_OFFSET)
                         // card.width())
                    x += C.COLS_OFFSET
                x += C.COLUMN_OFFSET
                y = C.CELL_HEIGHT * row + C.SCORE_CARD_OFFSET + C.VALUES_OFFSET
                self.screen.blit(cell_text, (x, y))

        # Draw the yahtzee name
        self.game_name.draw(self.screen)
        # Draw the player name
        self.player_name.draw(self.screen)
        # Draw the buttons on the screen
        for button in self.buttons:
            if button.is_hovered():
                button.color = C.HOVER_COLOR
            else:
                button.color = C.WHITE_COLOR
            button.draw(self.screen)

    def create_buttons(self):
        """Creates the buttons that the user can use to select the category for each round"""
        # Local variables to hold the x and y coordinates for the buttons
        x = C.SCORE_CARD_X + C.SCORE_CARD_OFFSET - C.BUTTON_X_OFFSET
        y = C.SCORE_CARD_Y + C.SCORE_CARD_OFFSET + C.BUTTON_Y_OFFSET
        # Creates 13 buttons for the 13 rounds/categories
        for n in range(13):
            b = Button(x, y, C.BUTTON_WIDTH, C.CELL_HEIGHT, "", C.FONT, C.WHITE_COLOR, C.WHITE_COLOR)
            # Moves the button down to the next section since the totals are not clicked
            if n == 5:
                y += C.SPLIT
            else:
                y += C.CELL_HEIGHT
            self.buttons.append(b)


if __name__ == "__main__":
    game = YahtzeeGame()
    game.start_game()
