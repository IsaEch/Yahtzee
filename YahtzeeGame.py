from Player import Player
import Constants as C
from Text import Text
from Button import Button
from Dice import Dice
import pygame


class YahtzeeGame(object):

    def __init__(self):
        self.players = [Player("Jack")]
        self.current_player = 0  # Index of the current player
        self.game_started = False
        self.game_finished = False
        self.screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        self.game_name = Text("YAHTZEE", C.FONT_SIZE,  C.BLACK_COLOR, C.YAHTZEE_X, C.YAHTZEE_Y)
        self.player_name = Text(self.players[self.current_player].name, C.FONT_SIZE, C.BLACK_COLOR, C.PLAYER_X,
                                C.PLAYER_Y)
        pygame.display.set_caption(C.CAPTION)
        pygame.display.background = C.BACKGROUND_COLOR
        self.roll_button = Button(C.ROLL_BUTTON_X, C.ROLL_BUTTON_Y, C.ROLL_WIDTH, C.ROLL_HEIGHT, "Roll",
                               C.FONT, C.GREY_COLOR, C.WHITE_COLOR)
        self.hold_button = Button(C.HOLD_BUTTON_X, C.HOLD_BUTTON_Y, C.HOLD_WIDTH, C.HOLD_HEIGHT, "Hold", C.FONT,
                                  C.GREY_COLOR, C.WHITE_COLOR)
        self.buttons = [self.roll_button, self.hold_button]
        self.dice_sprites = pygame.sprite.Group()   # Create a sprite group for the dice
        self.dice = []
        # Craete the dice objects and add them to the sprite group
        for n in range(5):
            if n < 3:
                x = C.DICE_X + n * (C.DICE_OFFSET + C.DICE_WIDTH)
                y = C.DICE_Y
            else:
                x = C.DICE_X + n * C.DICE_OFFSET
                y = C.DICE_Y + 100
            di = Dice(x, y)
            self.dice.append(di)
            self.dice_sprites.add(di)

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
                        if button == self.roll_button:
                            for die in self.dice:
                                die.start_animation()
            self.dice_sprites.update()
            self.draw_game()
            pygame.display.flip()

    def draw_game(self):
        """Draws the game on the screen"""
        # Local variable to hold the current score_card to iterate through
        card = self.players[self.current_player].score_card
        # Draw the score_card
        pygame.draw.rect(self.screen, C.SCORE_CARD_COLOR, (C.SCORE_CARD_X, C.SCORE_CARD_Y, C.SCREEN_WIDTH//2,
                                                           C.SCREEN_HEIGHT - C.SC_BACKGROUND_OFFSET))
        # Draw the buttons on the screen
        for button in self.buttons:
            # Change the button color when hovered to yellow
            if button.is_hovered() and button != (self.roll_button or button != self.hold_button):
                button.color = C.HOVER_COLOR
                # Change the roll or hold button color to light grey when hovered
            elif button.is_hovered() and (button == self.roll_button or button == self.hold_button):
                button.color = C.LIGHT_GREY_COLOR
                # Change the scorecard button color back to white when not hovered
            elif button != self.roll_button and button != self.hold_button:  # Roll button is always grey
                button.color = C.WHITE_COLOR
                # Change the roll or hold button color back to a darker grey when not hovered
            else:
                button.color = C.GREY_COLOR  # Changes the scorecard buttons black to white
            button.draw(self.screen)

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

        # Draw the hold box
        pygame.draw.rect(self.screen, C.RED_COLOR, (C.HOLD_BOX_X,
                                                    C.HOLD_BOX_Y, C.HOLD_BOX_WIDTH,
                                                    C.HOLD_BOX_HEIGHT + 100))
        # Draw the yahtzee name
        self.game_name.draw(self.screen)
        # Draw the player name
        self.player_name.draw(self.screen)
        # Draw the dice
        self.dice_sprites.draw(self.screen)


    def create_buttons(self):
        """Creates the buttons that the user can use to select the category for each round"""
        # Local variables to hold the x and y coordinates for the buttons
        x = C.SCORE_CARD_X + C.SCORE_CARD_OFFSET - C.BUTTON_X_OFFSET
        y = C.SCORE_CARD_Y + C.SCORE_CARD_OFFSET + C.BUTTON_Y_OFFSET
        # Creates 13 buttons for the 13 rounds/categories
        for n in range(13):
            b = Button(x, y, C.BUTTON_WIDTH, C.CELL_HEIGHT, "", C.FONT, C.WHITE_COLOR, C.WHITE_COLOR,
                       transparent=True)
            # Moves the button down to the next section since the totals are not clicked
            if n == 5:
                y += C.SPLIT
            else:
                y += C.CELL_HEIGHT
            self.buttons.append(b)


if __name__ == "__main__":
    game = YahtzeeGame()
    game.start_game()
