import random
from Player import Player
import Constants as C
from Text import Text
from Button import Button
from Dice import Dice
import pygame


class YahtzeeGame(object):

    button_names = ["Aces", "Twos", "Threes", "Fours", "Fives", "Sixes", "3 of a Kind", "4 of a Kind", "Full House",
                    "Small Straight", "Large Straight",
                    "Yahtzee", "Chance"]

    def __init__(self):
        self.players = [Player("Jack")]
        self.current_player = 0  # Index of the current player
        self.current_roll = 0   # Number of rolls for the current player; Max of 3 rolls per turn
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
        self.buttons = [self.roll_button]
        self.dice_sprites = pygame.sprite.Group()   # Create a sprite group for the dice
        self.dice = []  # List to hold the dice objects that can be rolled
        self.main_coordinates = [(945, 150), (1055, 150), (1165, 150), (995, 250), (1105, 250)]
        self.hold_coordinates = [(850, 675), (960, 675), (1070, 675), (1180, 675), (1290, 675)]
        self.hold_box = []    # List to hold the hold boxes for the dice
        # The text object that displays the message onto the screen
        self.game_text = Text("This is filler game text", C.MESSAGE_SIZE, C.WHITE_COLOR, C.MESSAGE_X,
                              C.MESSAGE_Y)
        self.roll_counter_text = Text("Roll 1", C.MESSAGE_SIZE, C.BLACK_COLOR, C.ROLL_COUNTER_X,
                                      C.ROLL_COUNTER_Y)
        self.has_rolled = False
        # Create the dice objects and add them to the sprite group
        for n in range(5):
            x, y = self.main_coordinates[n]
            di = Dice(x, y)   # Create the dice object
            self.dice.append(di)    # Add the dice object to the list; use to access dice methods
            self.dice_sprites.add(di)   # Add the dice object to the sprite group; used for animation
            self.rolling_dice = False
            self.game_clock = pygame.time.Clock()
            self.start_time = 0     # Placeholder for the start time of the dice roll animation
            self.wait_time = 0      # Placeholder for the amount of time to wait for the dice roll animation

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
                        print("Button clicked")     # Placeholder for now; Used for testing
                        print(self.get_roll_value())    # Placeholder for now; Used for testing
                        if button == self.roll_button and not button.disabled:
                            button.disabled = True
                            self.game_text.update_message("Rolling the dice.")
                            self.roll_counter_text.update_message("Roll " + str(self.current_roll + 1))
                            self.add_roll_count()
                            # Random amount of time to roll the dice
                            self.wait_time = random.randint(1000, 3000)
                            # Get the current ticks to start the timer
                            self.start_time = pygame.time.get_ticks()
                            self.rolling_dice = True
                            for die in self.dice:   # Start the animation for each di
                                die.start_animation()
                        elif not button.disabled:
                            self.score_category(button)
                            print("This is a category button")    # Placeholder for now; Used for testing
                for die in self.dice:   # Used to move the di from the main area to the hold box
                    if die.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN and not self.rolling_dice:
                        self.hold_die(die)  # Hold the die
                        # Update the remaining rolling dice positions
                        self.update_dice_positions(self.hold_box, self.hold_coordinates)
                        # Update the hold dice positions
                        self.update_dice_positions(self.dice, self.main_coordinates)
                for die in self.hold_box:   # Used to move the die from the hold box to the main area
                    if die.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN and not self.rolling_dice:
                        self.release_die(die)
                        # Update the remaining rolling dice positions
                        self.update_dice_positions(self.hold_box, self.hold_coordinates)
                        # Update the hold dice positions
                        self.update_dice_positions(self.dice, self.main_coordinates)
            # Wait for a random number of seconds from 1-3 to stop the animation and show values
            if self.rolling_dice and (pygame.time.get_ticks() - self.start_time) >= self.wait_time:
                self.game_text.update_message("Dice rolled")
                self.rolling_dice = False
                if self.current_roll == 3:
                    self.game_text.update_message("Select a category")
                else:
                    self.roll_button.disabled = False
                for die in self.dice:
                    die.stop_animation(die.roll())
                self.has_rolled = True  # Set to True to indicate that the dice have been rolled and can be scored
            self.dice_sprites.update()
            self.draw_game()

            pygame.display.flip()

    def draw_game(self):
        self.screen.fill(C.BACKGROUND_COLOR)
        """Draws the game on the screen"""
        # Draw the hold box
        pygame.draw.rect(self.screen, C.RED_COLOR, (C.HOLD_BOX_X,
                                                    C.HOLD_BOX_Y, C.HOLD_BOX_WIDTH,
                                                    C.HOLD_BOX_HEIGHT))
        # Local variable to hold the current score_card to iterate through
        card = self.players[self.current_player].score_card
        # Draw the score_card
        pygame.draw.rect(self.screen, C.SCORE_CARD_COLOR, (C.SCORE_CARD_X, C.SCORE_CARD_Y, C.SCREEN_WIDTH//2,
                                                           C.SCREEN_HEIGHT - C.SC_BACKGROUND_OFFSET))
        # Draw the buttons on the screen
        for button in self.buttons:
            # Change the button color when hovered to yellow
            if not button.disabled:
                if button.is_hovered() and button != self.roll_button:
                    button.color = C.HOVER_COLOR
                    # Change the roll or hold button color to light grey when hovered
                elif button.is_hovered() and button == self.roll_button:
                    button.color = C.LIGHT_GREY_COLOR
                    # Change the scorecard button color back to white when not hovered
                elif button != self.roll_button:  # Roll button is always grey
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
                grid_x = (C.SCORE_CARD_X + C.SCORE_CARD_OFFSET + col * (C.SCREEN_WIDTH//2 - 2 * C.SCORE_CARD_OFFSET)
                          // card.width())
            # Adjust line length to fit the card
            pygame.draw.line(self.screen, C.BLACK_COLOR, (grid_x, C.SCORE_CARD_X+C.SC_BEGIN_LENGTH_OFFSET),
                             (grid_x, C.SCREEN_HEIGHT + C.SCORE_CARD_Y - C.SC_END_LENGTH_OFFSET))

        # Draw the score_card values
        for row in range(card.length()):
            for col in range(card.width()):
                # Don't fill in zeros until after the category has been selected and filled
                if card.filled[row] or col == 0:
                    # Convert the cell value to a text to be drawn
                    cell_value = str(card.score[row][col])
                else:
                    cell_value = ""
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
        # Draw the dice
        self.dice_sprites.draw(self.screen)
        # Draw the game text
        self.game_text.draw(self.screen)
        # Draw the roll counter text
        self.roll_counter_text.draw(self.screen)

    def create_buttons(self):
        """Creates the buttons that the user can use to select the category for each round"""

        # Local variables to hold the x and y coordinates for the buttons
        x = C.SCORE_CARD_X + C.SCORE_CARD_OFFSET - C.BUTTON_X_OFFSET
        y = C.SCORE_CARD_Y + C.SCORE_CARD_OFFSET + C.BUTTON_Y_OFFSET
        # Creates 13 buttons for the 13 rounds/categories
        for n in range(13):
            b = Button(x, y, C.BUTTON_WIDTH, C.CELL_HEIGHT, "", C.FONT, C.WHITE_COLOR, C.WHITE_COLOR,
                       transparent=True)
            b.button_name = YahtzeeGame.button_names[n]
            # Moves the button down to the next section since the totals are not clicked
            if n == 5:
                y += C.SPLIT
            else:
                y += C.CELL_HEIGHT
            self.buttons.append(b)

    def add_roll_count(self):
        """Updates the roll count for the current player"""
        self.current_roll += 1
        
    def hold_die(self, die):
        """Sets the dice hold value to True and moves the dice into the hold_box list"""
        die.held = True
        self.hold_box.append(die)
        self.dice.remove(die)

    def release_die(self, die):
        """Sets the dice hold value to False and moves the dice back into the dice list"""
        die.held = False
        self.dice.append(die)
        self.hold_box.remove(die)

    def update_dice_positions(self, dice_list, coord_list):
        """Updates the dice positions on the screen based on the dice_list and coord_list so that there are not any
        large gaps between dice"""
        for n in range(len(dice_list)):     # Iterate through the dice_list
            x, y = coord_list[n]    # Get the x and y coordinates from the coord_list
            dice_list[n].x = x    # Set the x coordinate for the dice object
            dice_list[n].y = y  # Set the y coordinate for the dice object
            # Set the position of the dice object on the screen
            dice_list[n].rect = dice_list[n].image.get_rect(center=(x, y))

    def get_roll_value(self):
        """Gets the value of the dice roll"""
        return [die.value for die in self.dice_sprites]

    def score_category(self, button):
        """Handles the scoring and selection of the row for the scorecard so that the values can be updated
        appropriately"""
        category_num = YahtzeeGame.button_names.index(button.button_name)
        if self.has_rolled:
            score = 0   # Placeholder for the score of the category
            dice_values = self.get_roll_value()    # Get the values of the dice roll
            if category_num < 6:    # Upper section
                score = self.upper_section(dice_values, category_num + 1)
            elif category_num == 6:     # 3 of a kind
                if self.of_a_kind(dice_values, 3):
                    score = sum(dice_values)
            elif category_num == 7:     # 4 of a kind
                if self.of_a_kind(dice_values, 4):
                    score = sum(dice_values)
            elif category_num == 8:     # Full house
                if self.full_house(dice_values):
                    score = 25
            elif category_num == 9:     # Small straight
                if self.small_straight(dice_values):
                    score = 30
            elif category_num == 10:    # Large straight
                if self.large_straight(dice_values):
                    score = 40
            elif category_num == 11:    # Yahtzee
                if self.of_a_kind(dice_values, 5):
                    score = 50
            elif category_num == 12:    # Chance
                score = sum(dice_values)
            # Update the score card

    def upper_section(self, dice_values, num):
        """Check if the dice values have a 3 or 4 of a kind"""
        count = 0
        # Iterate through the dice values and count the number of times the value appears
        for value in dice_values:
            if value == num + 1:
                count += 1
        return count * (num + 1)

    def of_a_kind(self, dice_values, num):
        """Check if the dice values have a 3 or 4 of a kind"""
        for value in dice_values:
            if dice_values.count(value) >= num:
                return True
        return False

    def full_house(self, dice_values):
        """Check if the dice values have a full house"""
        dice_values.sort()
        num1 = dice_values.count(dice_values[0])
        num2 = dice_values.count(dice_values[-1])
        return (num1 == 2 and num2 == 3) or (num1 == 3 and num2 == 2)

    def small_straight(self, dice_values):
        """Check if the dice values have a small or large straight"""
        return len(set(dice_values)) >= 4

    def large_straight(self, dice_values):
        """Check if the dice values have a large straight"""
        return len(set(dice_values)) == 5


if __name__ == "__main__":
    game = YahtzeeGame()
    game.start_game()
