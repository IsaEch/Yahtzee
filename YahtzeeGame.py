import random
from Player import Player
import Constants as C
from Text import Text
from Button import Button
from Dice import Dice
from Results import ResultsScreen
import pygame


class YahtzeeGame(object):

    button_names = ["Aces", "Twos", "Threes", "Fours", "Fives", "Sixes", "3 of a Kind", "4 of a Kind", "Full House",
                    "Small Straight", "Large Straight",
                    "Yahtzee", "Chance"]

    def __init__(self, screen, players):
        """Initializes the game with the players, dice, and buttons"""
        self.players = players
        self.current_player = 0  # Index of the current player
        self.current_roll = 0   # Number of rolls for the current player; Max of 3 rolls per turn
        self.game_started = True
        self.round_played = False
        self.game_finished = False
        self.screen = screen
        self.game_name = Text("YAHTZEE", C.FONT_SIZE,  C.BLACK_COLOR, C.YAHTZEE_X, C.YAHTZEE_Y)
        self.player_name = Text(self.players[self.current_player].name, C.FONT_SIZE, C.BLACK_COLOR, C.PLAYER_X,
                                C.PLAYER_Y, right_justified=True)
        pygame.display.set_caption(C.CAPTION)
        pygame.display.background = C.BACKGROUND_COLOR
        self.roll_button = Button(C.ROLL_BUTTON_X, C.ROLL_BUTTON_Y, C.ROLL_WIDTH, C.ROLL_HEIGHT, "Roll",
                                C.FONT, C.GREY_COLOR, C.WHITE_COLOR)
        self.switch_button = Button(C.NEXT_BUTTON_X, C.NEXT_BUTTON_Y, C.NEXT_WIDTH, C.NEXT_HEIGHT, "Next", C.FONT,
                                    C.GREY_COLOR, C.WHITE_COLOR, hidden=True, disabled=True)
        self.buttons = [self.roll_button, self.switch_button]
        self.dice_sprites = pygame.sprite.Group()   # Create a sprite group for the dice
        self.dice = []  # List to hold the dice objects that can be rolled
        self.main_coordinates = [(945, 200), (1055, 200), (1165, 200), (995, 300), (1105, 300)]
        self.hold_coordinates = [(850, 675), (960, 675), (1070, 675), (1180, 675), (1290, 675)]
        self.hold_box = []    # List to hold the hold boxes for the dice
        # The text object that displays the message onto the screen
        self.game_text = Text("Click roll to start the turn", C.MESSAGE_SIZE, C.WHITE_COLOR, C.MESSAGE_X,
                              C.MESSAGE_Y, centered=True)
        self.roll_counter_text = Text("Roll 0", C.MESSAGE_SIZE, C.WHITE_COLOR, C.ROLL_COUNTER_X,
                                      C.ROLL_COUNTER_Y)
        self.has_rolled = False
        self.transitioning = False
        self.scored_yahztee = False
        self.next_player = Text("Next Player", C.NEXT_SIZE, C.WHITE_COLOR, C.SWITCH_MESSAGE_X,
                                C.SWITCH_MESSAGE_Y, centered=True)
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
        self.initial_coord = []
        self.created_initial_coord = False

    def start_game(self):
        """The main game loop that control the entire game. It handles the events, updates, and drawing of the game"""
        self.create_buttons()
        self.screen.fill(C.BACKGROUND_COLOR)
        while self.game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_started = False
                for button in self.buttons:
                    if button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                        if button == self.roll_button and not button.disabled and len(self.dice) > 0:
                            button.disabled = True
                            self.game_text.update_message("Rolling the dice.")
                            self.add_roll_count()
                            # Random amount of time to roll the dice
                            self.wait_time = random.randint(1000, 3000)
                            # Get the current ticks to start the timer
                            self.start_time = pygame.time.get_ticks()
                            self.rolling_dice = True
                            for die in self.dice:   # Start the animation for each di
                                die.start_animation()
                        elif button == self.roll_button and not button.disabled:
                            self.game_text.update_message("There are no dice to roll.")
                        elif not button.disabled and not self.round_played and self.has_rolled:
                            self.score_category(button, self.players[self.current_player].score_card)
                for die in self.dice:   # Used to move the di from the main area to the hold box
                    if (die.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN and not self.rolling_dice
                            and self.has_rolled):
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
            # Switch the player after the round has been played and after 2 seconds
            if self.round_played and (pygame.time.get_ticks() - self.start_time) >= C.SWITCH_WAIT_TIME:
                self.switch_button.hidden = False
                self.switch_button.disabled = False
            if self.switch_button.is_clicked() and not self.switch_button.disabled:
                if self.check_score_card_filled():
                    self.game_finished = True
                    self.game_started = False
                    results_screen = ResultsScreen(self.screen, self.players)
                    results_screen.game_loop()
                else:
                    self.switch_player()
            self.dice_sprites.update()
            self.draw_game()
            pygame.display.flip()

    def draw_game(self):
        self.screen.fill(C.BACKGROUND_COLOR)
        """Draws all the buttons and rectangles for the game on the screen"""
        # Draw the hold box
        pygame.draw.rect(self.screen, C.RED_COLOR, (C.HOLD_BOX_X, C.HOLD_BOX_Y, C.HOLD_BOX_WIDTH,
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
                if button.is_hovered() and button != self.roll_button and not self.round_played:
                    button.color = C.HOVER_COLOR
                    # Change the roll or hold button color to light grey when hovered
                elif button.is_hovered() and (button == self.roll_button or button == self.switch_button):
                    button.color = C.LIGHT_GREY_COLOR
                    # Change the scorecard button color back to white when not hovered
                elif button != self.roll_button and button != self.switch_button:  # Roll button is always grey
                    button.color = C.WHITE_COLOR
                    # Change the roll or hold button color back to a darker grey when not hovered
                else:
                    button.color = C.GREY_COLOR  # Changes the scorecard buttons black to white
            elif button.disabled and button != self.roll_button:
                button.color = C.WHITE_COLOR
            else:
                button.color = C.LIGHT_GREY_COLOR
            button.draw(self.screen)

        # Draw the grid row
        for row in range(card.length() + 3):
            grid_y = C.CELL_HEIGHT * row + (C.SCORE_CARD_OFFSET*2 - C.SC_X_OFFSET)
            pygame.draw.line(self.screen, C.BLACK_COLOR, (C.SCORE_CARD_X + C.SC_GRID_OFFSET, grid_y),
                    (C.SCREEN_WIDTH//2 + C.SCORE_CARD_Y-C.GRID_Y_OFFSET, grid_y))
        # Draw the grid columns
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
                if (col < 6 and col > 0) and (row > 6 and row < 10):
                    continue    # Skip the upper section totals so that they only have 1 cell to fill
                if (col < 6 and col > 0) and row > 17:
                    continue   # Skip the lower section totals so that they only have 1 cell to fill
                # Render the text
                cell_text = C.FONT.render(cell_value, True, C.BLACK_COLOR)
                # Draw each cell value on the screen and push text to make space for the 1st column
                if col == 0:
                    x = C.CELL_WIDTH * col + C.SCORE_CARD_OFFSET - C.COL_ONE_OFFSET
                elif row == 10:     # Skip the 11th row because it is only the lower section title
                    continue
                elif col == 6 and row == 0:  # Centers the text "score" in the cell
                    x = (C.SCORE_CARD_X + C.SCORE_CARD_OFFSET + col * (C.SCREEN_WIDTH//2 - C.SCORE_COL_OFFSET
                                                                       * C.SCORE_CARD_OFFSET)
                         // card.width())
                else:
                    # Adjust the x position to fit the card
                    x = (C.SCORE_CARD_X + C.SCORE_CARD_OFFSET + col * (C.SCREEN_WIDTH//2 - 2 * C.SCORE_CARD_OFFSET)
                         // card.width())
                    x += C.COLS_OFFSET
                x += C.COLUMN_OFFSET
                y = C.CELL_HEIGHT * row + C.SCORE_CARD_OFFSET + C.VALUES_OFFSET
                self.screen.blit(cell_text, (x, y))

        # Cover1--Transparent rectangle to cover the sections of the upper section that are not to be selected
        transparent_rect = pygame.Surface((C.COVER1_WIDTH, C.COVER1_HEIGHT), pygame.SRCALPHA)
        transparent_rect.fill((*C.GREY_COLOR, 128))  # 128 is the alpha value for 50% transparency
        self.screen.blit(transparent_rect, (C.COVER1_X, C.COVER1_Y))

        # Cover2--Transparent rectangle to cover the sections of the lower section that are not to be selected
        transparent_rect = pygame.Surface((C.COVER2_WIDTH, C.COVER2_HEIGHT), pygame.SRCALPHA)
        transparent_rect.fill((*C.GREY_COLOR, 128))  # 128 is the alpha value for 50% transparency
        self.screen.blit(transparent_rect, (C.COVER2_X, C.COVER2_Y))

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
        # Update the roll counter text
        self.roll_counter_text.update_message("Roll " + str(self.current_roll))
        # Draw the score_table
        self.draw_score_table()
        # Draw the tool tip when hovered
        self.show_tooltip()

    def show_tooltip(self):
        """Shows a tooltip with the player's name when hovered over the score table"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for n, (x, y) in enumerate(self.initial_coord):
            if x < mouse_x < x + C.TOOLTIP_RANGE_X and y < mouse_y < y + C.TOOLTIP_RANGE_Y:
                tooltip_text = self.players[n].name
                tooltip = Text(tooltip_text, C.FONT_SIZE, C.BLACK_COLOR, mouse_x + C.TOOLTIP_RANGE_X, mouse_y)
                text_surface = tooltip.font.render(tooltip_text, True, C.BLACK_COLOR)
                text_width = text_surface.get_width()
                text_height = text_surface.get_height()

                # Draw a translucent white rectangle behind the tooltip
                tooltip_rect = pygame.Surface((text_width, text_height), pygame.SRCALPHA)
                tooltip_rect.fill(C.WHITE_COLOR)  # White with 50% transparency
                self.screen.blit(tooltip_rect, (mouse_x + C.TOOLTIP_RANGE_X, mouse_y))
                tooltip.draw(self.screen)

    def draw_score_table(self):
        """Draws a 2d table on the screen to display the total score for each player"""
        num_players = len(self.players)
        table_width = C.ST_CELL_WIDTH * num_players + (num_players - 1) * C.CELL_PADDING  # Add padding between cells
        table_height = C.ST_CELL_HEIGHT * 2
        center_x = C.SCORE_TABLE_X  # Center the table on the screen
        start_x = center_x - (table_width // 2)
        start_y = C.SCORE_TABLE_Y

        # Adjust the starting x-coordinate to center the box around the text
        adjusted_start_x = start_x - C.FONT_SIZE

        # Draw the white box behind the score table
        pygame.draw.rect(self.screen, C.SCORE_CARD_COLOR, (adjusted_start_x, start_y, table_width + C.FONT_SIZE,
                                                           table_height))

        for index, player in enumerate(self.players):
            x = start_x + index * (C.ST_CELL_WIDTH + C.CELL_PADDING)
            y = start_y + C.ST_TEXT_Y_OFFSET
            # Get the first letter of the player's name
            initial = player.name[0]  # Get the first letter of the player's name
            initial_text = Text(initial, C.FONT_SIZE, C.BLACK_COLOR,
                                x, y)
            # Get the player's score and draw it
            score_text = Text(str(player.score_card.score[21][6]), C.FONT_SIZE, C.BLACK_COLOR, x,  y + C.ST_CELL_HEIGHT)
            if not self.created_initial_coord:
                self.initial_coord.append((x, y))
            initial_text.draw(self.screen)
            score_text.draw(self.screen)
        self.created_initial_coord = True

    def create_buttons(self):
        """Creates the buttons for the scorecard that the user can use to select the category for each round.
        Purposefully separated from draw game and the main game loop to prevent duplication of buttons and causing more
        bugs."""
        # Local variables to hold the x and y coordinates for the buttons; Makes it easier to read within this scope
        x = C.SCORE_CARD_X + C.SCORE_CARD_OFFSET - C.BUTTON_X_OFFSET
        y = C.SCORE_CARD_Y + C.SCORE_CARD_OFFSET + C.BUTTON_Y_OFFSET
        # Creates 13 buttons for the 13 rounds/categories
        for n in range(13):
            # Text and button names are different. Text displays on the screen. Name is used to match the category
            b = Button(x, y, C.BUTTON_WIDTH, C.CELL_HEIGHT, "", C.FONT, C.WHITE_COLOR, C.WHITE_COLOR,
                       transparent=True)
            b.button_name = YahtzeeGame.button_names[n]  # Button name to be used to determine the category when clicked
            # Moves the button down to the next section since the totals are not clicked
            if n == 5:
                y += C.SPLIT
            else:
                y += C.CELL_HEIGHT
            self.buttons.append(b)

    def add_roll_count(self):
        """Increases the roll count for the current player so that the player can only roll 3 times per turn"""
        self.current_roll += 1
        
    def hold_die(self, die):
        """Sets the dice hold value to True and moves the dice into the hold_box list. The dice will not be rolled"""
        die.held = True
        self.hold_box.append(die)
        self.dice.remove(die)

    def release_die(self, die):
        """Sets the dice hold value back to False and moves the dice back into the dice list. The dice can be
        rolled again"""
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
        """Gets the value of the dice roll to be used for scoring purposes"""
        return [die.value for die in self.dice_sprites]

    def score_category(self, button: Button, card: object):
        """Handles the scoring and selection of the row for the scorecard so that the values can be updated
        appropriately onto the scorecard"""
        self.round_played = True    # Set to True to indicate that the round has been played and that the other
        self.start_time = pygame.time.get_ticks()
        # categories cannot be selected
        button.disabled = True  # Disable the button so that it can't be clicked again
        category_num = YahtzeeGame.button_names.index(button.button_name)
        if self.has_rolled:
            score = 0   # Placeholder for the score of the category
            dice_values = self.get_roll_value()    # Get the values of the dice roll
            if self.scored_yahztee and self.of_a_kind(dice_values, 5):
                card.add_yahztee_bonus()
            if category_num < 6:    # Upper section
                score = self.upper_section(dice_values, category_num)
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
                    # Set to True to indicate that a yahztee has been scored and allow for bonuses to be scored
                    self.scored_yahztee = True
                    # Iterate through the score card to check for bonuses for edge case. Yahtzee can be scored in a
                    # different category before the Yahtzee category. Thus, the other categories must be checked after
                    # filling a yahtzee in the yahtzee category
                    for category in card.score:
                        if category[1] == 0:
                            continue
                        elif self.of_a_kind(category[1:6], 5) and category[0] != "Yahtzee":
                            card.add_yahztee_bonus()
                # Set to True to indicate that the Yahtzee category has been filled and shows the yahtzee bonus value
                # (even if it is 0)
                card.filled[18] = True
            elif category_num == 12:    # Chance
                score = sum(dice_values)
            # Update the category number to accurate reflect the rows in the score card
            if category_num < 6:    # Upper section
                category_num += 1
            else:
                category_num += 5   # Lower section
            # Update the score card
            self.roll_button.disabled = True
            card.set_category(category_num, score, dice_values)  # Set the category to filled and update the score
            card.update_grand_upper_total()    # Update the grand upper total
            card.update_grand_total()

    def upper_section(self, dice_values, num):
        """Determines the score for the upper section of the score card and returns the score"""
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
        """Checks if the dice values have a full house (set of 3 and 2)"""
        dice_values.sort()
        num1 = dice_values.count(dice_values[0])
        num2 = dice_values.count(dice_values[-1])
        return (num1 == 2 and num2 == 3) or (num1 == 3 and num2 == 2)

    def small_straight(self, dice_values):
        """Checks if the dice values have a small or large straight"""
        return len(set(dice_values)) >= 4

    def large_straight(self, dice_values):
        """Checks if the dice values have a large straight"""
        return len(set(dice_values)) == 5

    def switch_player(self):
        """Switches the player to the next player in the list"""
        self.current_player += 1    # Increment the current player index
        # Check if the current player index is out of bounds and reset if so
        if self.current_player == len(self.players):
            self.current_player = 0
        player = self.players[self.current_player]  # Get the current player
        self.player_name.update_message(player.name)   # Update player name on the scorecard
        self.current_roll = 0   # Reset the current roll to 0
        self.round_played = False   # Set to False to indicate that the round has not been played
        self.has_rolled = False    # Set to False to indicate that the dice have not been rolled
        self.roll_button.disabled = False
        # Release any and all dice from the hold box
        for die in self.hold_box[:]:  # This had a weird bug where 1 die would stay and [:] fixed it
            self.release_die(die)
        self.update_dice_positions(self.dice, self.main_coordinates)    # Update the dice positions for the main area
        self.update_dice_positions(self.hold_box, self.hold_coordinates)    # Update the hold box positions
        self.game_text.update_message("Click roll to start the turn")

        self.fill_screen_transition()    # Transition effect for the game
        self.draw_next_player_name(player.name)    # Draw the next player's name on the screen
        self.undo_screen_transition()    # Transition effect for the game

        # Update the button disabled status to flect the new current player's score card
        for button in self.buttons:
            if button.button_name in YahtzeeGame.button_names:  # Check if the button is a category button
                # Get the category number to be used for index purposes
                category_num = YahtzeeGame.button_names.index(button.button_name)
                # Adjusts the category number to match the rows in the score card
                if category_num < 6:
                    category_num += 1
                else:
                    category_num += 5
                button.disabled = player.score_card.filled[category_num]

    def fill_screen_transition(self):
        """Creates a screen transition effect when switching players that gradually fills the screen with a color from
        left to right to indicate the end of the round"""
        # Fill the screen with a solid color from left to right
        self.switch_button.disabled = True  # Disable the switch button until the transition is complete
        for n in range(C.SCREEN_WIDTH):
            pygame.draw.rect(self.screen, C.BACKGROUND_COLOR, (0, 0, n, C.SCREEN_HEIGHT))
            pygame.display.flip()

    def undo_screen_transition(self):
        """Undoes the screen transition effect but gradually decreases the fill from left to right"""
        self.switch_button.hidden = True    # Hide the switch button before the transition is complete
        for n in range(C.SCREEN_WIDTH):
            self.draw_game()    # Redraw the game to show the changes
            # Draw the solid color decreases to finish animation effect
            pygame.draw.rect(self.screen, C.BACKGROUND_COLOR, (n, 0, C.SCREEN_WIDTH - n, C.SCREEN_HEIGHT))
            pygame.display.flip()

    def draw_next_player_name(self, name: str):
        """Draws the next player's name on the screen"""
        message = "Next Player: " + name
        self.next_player.update_message(message)   # Update the message to display the next player's name
        self.next_player.draw(self.screen)
        pygame.display.flip()
        pygame.time.wait(C.NEXT_WAIT_TIME)    # Wait for 2 seconds before switching players

    def check_score_card_filled(self):
        """Check if the score card is filled and the game is over"""
        for player in self.players:
            for row in player.score_card.filled:
                if not player.score_card.filled[row]:
                    return False
        return True


if __name__ == "__main__":
    players = [Player("Nixie"), Player("Lyla")]
    screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
    game = YahtzeeGame(screen, players)
    game.start_game()
