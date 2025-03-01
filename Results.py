import Constants as C
from pygame import display
from Text import Text
class ResultsScreen(object):

    def __init__(self, screen, players):
        self.screen = screen
        self.players = players

    def draw(self):
        """Draws the results screen with each player's name and total score"""
        self.screen.fill(C.BACKGROUND_COLOR)
        title = Text("Results", C.RESULTS_SIZE, C.WHITE_COLOR, C.SCREEN_WIDTH//2, C.RESULTS_Y, centered=True)
        title.draw(self.screen)

        # Define the starting coordinates for the table
        row_height = C.RESULTS_TABLE_ROW_HEIGHT

        # Create the table headers
        name_header = Text("Name", C.HEADER_SIZE, C.WHITE_COLOR, C.NAME_HEADER_X, C.NAME_HEADER_Y)
        score_header = Text("Score", C.HEADER_SIZE, C.WHITE_COLOR, C.SCORE_HEADER_X, C.SCORE_HEADER_Y)
        # Draw the table headers
        name_header.draw(self.screen)
        score_header.draw(self.screen)

        # Draw the player names and scores
        for i, player in enumerate(self.players):
            name = Text(player.name, C.NAME_SIZE, C.WHITE_COLOR, C.RESULTS_NAMES_X, C.RESULTS_NAMES_Y + (i + 1) * row_height)
            score = Text(str(player.score), C.NAME_SIZE, C.WHITE_COLOR, C.RESULTS_SCORE_X, C.RESULTS_SCORE_Y + (i + 1) * row_height)
            name.draw(self.screen)
            score.draw(self.screen)

        display.flip()

    def set_player_scores(self):
        """"Sets the final scores for each player"""
        for player in self.players:
            player.set_final_score()

    def game_loop(self):
        """Runs the game loop for the results screen"""
        self.set_player_scores()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw()


if __name__ == "__main__":
    from pygame import init
    from Player import Player
    from YahtzeeGame import YahtzeeGame
    import pygame
    init()
    game = YahtzeeGame()
    p1 = Player("Nixie")
    p2 = Player("Lyla")
    p1.score = 100
    p2.score = 200
    players = [p1, p2]
    players.sort(key=lambda x: x.score, reverse=True)
    screen = display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
    results = ResultsScreen(game.screen, players)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        results.draw()
