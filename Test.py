from YahtzeeGame import YahtzeeGame
from Player import Player
"""This file is only used to test the scoring system of the game. It has no other purpose"""
y = YahtzeeGame()
players = [Player("Nixie"), Player("Lyla"), Player("Milo")]
extra = 10
for player in players:
    player.score_card.score[21][6] = 100 + extra
    extra += 10
    for row in player.score_card.filled:
        player.score_card.filled[row] = True
y.players = players
y.switch_button.disabled = False
y.switch_button.hidden = False
y.has_rolled = False
y.start_game()
