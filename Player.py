from ScoreCard import ScoreCard


class Player(object):

    def __init__(self, name: str):
        self.name = name
        self.score_card = ScoreCard()
        self.rolls_remaining = 3
        self.score = 0
