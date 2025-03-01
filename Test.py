from YahtzeeGame import YahtzeeGame
from Player import Player
"""This file is only used to test the scoring system of the game. It has no other purpose"""
y = YahtzeeGame()
players = [Player("Nixie"), Player("Lyla"), Player("Milo")]
y.players = players
y.switch_button.disabled = False
y.switch_button.hidden = False
y.has_rolled = True
y.start_game()
