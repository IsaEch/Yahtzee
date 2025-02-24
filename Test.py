from YahtzeeGame import YahtzeeGame
"""This file is only used to test the scoring system of the game. It has no other purpose"""
y = YahtzeeGame()
count = 0
for die in y.dice_sprites:
    if count < 3:
        die.value = 5
    else:
        die.vale = 1
    count += 1
y.has_rolled = True

y.start_game()
