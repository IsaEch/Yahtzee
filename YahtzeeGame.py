from Player import Player
import Constants as C
import pygame


class YahtzeeGame(object):

    def __init__(self):
        self.players = [Player("Jack")]
        self.current_player = 0
        self.game_started = False
        self.game_finished = False
        self.screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        pygame.display.set_caption(C.CAPTION)
        pygame.display.background = C.BACKGROUND_COLOR

    def start_game(self):
        self.game_started = True
        self.screen.fill(C.BACKGROUND_COLOR)
        while self.game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_started = False
            self.draw_game()
            pygame.display.flip()

    def draw_game(self):
        # Local variable to hold the current score_card to iterate through
        card = self.players[self.current_player].score_card
        # Draw the score_card
        pygame.draw.rect(self.screen, C.SCORE_CARD_COLOR, (C.SCORE_CARD_X_Y, C.SCORE_CARD_X_Y, C.SCREEN_WIDTH//2,
                                                           C.SCREEN_HEIGHT-20))

        # Draw the grid
        for row in range(card.length()):
            grid_y = C.CELL_HEIGHT * row + C.SCORE_CARD_OFFSET
            pygame.draw.line(self.screen, C.BLACK_COLOR, (C.SCORE_CARD_X_Y, grid_y),
                             (C.SCREEN_WIDTH//2 + C.SCORE_CARD_X_Y, grid_y))
        for col in range(card.length()):
            grid_x = C.CELL_WIDTH * col + C.SCORE_CARD_OFFSET if col == 0 else C.CELL_WIDTH * col + C.SC_DESC_OFFSET
            pygame.draw.line(self.screen, C.BLACK_COLOR, (grid_x, C.SCORE_CARD_X_Y),
                             (grid_x, C.SCREEN_HEIGHT + C.SCORE_CARD_X_Y))

        # Draw the score_card values
        for row in range(card.length()):
            for col in range(card.width()):
                # Convert the cell value to a text to be drawn
                cell_value = str(self.players[self.current_player].score_card.score[row][col])
                # Render the text
                cell_text = C.FONT.render(cell_value, True, C.BLACK_COLOR)
                # Draw each cell value on the screen and push text to make space for the 1st column
                x = C.CELL_WIDTH * col + C.SCORE_CARD_OFFSET if col == 0 else (C.CELL_WIDTH * col
                                                                               + C.SC_DESC_OFFSET)
                y = C.CELL_HEIGHT * row + C.SCORE_CARD_OFFSET
                self.screen.blit(cell_text, (x, y))


if __name__ == "__main__":
    game = YahtzeeGame()
    game.start_game()
