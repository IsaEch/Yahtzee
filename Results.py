import Constants as C
from pygame import display
from Text import Text


class ResultsScreen(object):

    def __init__(self, screen, players):
        self.screen = screen
        self.players = players
        self.title = Text("Results", C.RESULTS_SIZE, C.WHITE_COLOR, C.SCREEN_WIDTH//2, C.RESULTS_Y,
                          centered=True)
        self.name_header = Text("Name", C.HEADER_SIZE, C.WHITE_COLOR, C.NAME_HEADER_X, C.NAME_HEADER_Y)
        self.score_header = Text("Score", C.HEADER_SIZE, C.WHITE_COLOR, C.SCORE_HEADER_X, C.SCORE_HEADER_Y)
        self.winner = Text("wins", C.WINNER_SIZE, C.WHITE_COLOR, C.WINNER_X,
                           C.WINNER_Y, centered=True)

    def game_loop(self):
        """Runs the game loop for the results screen"""
        self.set_player_scores()
        self.check_winner()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw()

    def check_winner(self):
        """Checks that the player with the highest score is the winner and there is not a tie"""
        if self.players[0].score == self.players[1].score:
            self.winner.update_message("It's a tie!")
        else:
            self.winner.update_message(f"{self.players[0].name} wins!")

    def draw(self):
        """Draws the results screen with each player's name and total score"""
        self.screen.fill(C.BACKGROUND_COLOR)
        self.title.draw(self.screen)
        self.winner.draw(self.screen)

        # Draw the table headers
        self.name_header.draw(self.screen)
        self.score_header.draw(self.screen)

        # Define the starting coordinates for the table
        row_height = C.RESULTS_TABLE_ROW_HEIGHT

        # Draw the player names and scores
        for i, player in enumerate(self.players):
            name = Text(player.name, C.NAME_SIZE, C.WHITE_COLOR, C.RESULTS_NAMES_X, C.RESULTS_NAMES_Y + (i + 1)
                        * row_height)
            score = Text(str(player.score), C.NAME_SIZE, C.WHITE_COLOR, C.RESULTS_SCORE_X, C.RESULTS_SCORE_Y + (i + 1)
                         * row_height)
            name.draw(self.screen)
            score.draw(self.screen)
        display.flip()

    def set_player_scores(self):
        """"Sets the final scores for each player"""
        for player in self.players:
            player.set_final_score()
        self.players.sort(key=lambda x: x.score, reverse=True)


if __name__ == "__main__":
    from pygame import init
    from Player import Player
    import pygame
    init()
    p1 = Player("Nixie")
    p2 = Player("Lyla")
    p1.score_card.score[21][6] = 100
    p2.score_card.score[21][6] = 200
    players = [p1, p2]
    players.sort(key=lambda x: x.score, reverse=True)
    screen = display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
    results = ResultsScreen(screen, players)
    results.game_loop()

