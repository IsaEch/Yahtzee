from ScoreCard import ScoreCard

class Player(object):

    def __init__(self, name: str):
        self.name = name
        self.score_card = ScoreCard()
        self.score = 0

    def set_final_score(self):
        """Sets the final score for the player"""
        self.score = self.score_card.score[21][6]