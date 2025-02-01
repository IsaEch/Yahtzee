class ScoreCard(object):
    row_descriptions = {0: "Aces", 1: "Twos", 2: "Threes", 3: "Fours", 4: "Fives", 5: "Sixes", 6: "TOTAL SCORE",
                        7: "BONUS", 8: "TOTAL"}
    def __init__(self):
        self.score = [[0]*6 for _ in range(13)]
        for n in range(13):
            if n < 9:
                self.score[n][0] = ScoreCard.row_descriptions[n]

    def length(self):
        return len(self.score)

    def width(self):
        return len(self.score[0])


    def __str__(self):
        return f"{self.score}"



if __name__ == '__main__':
    score = ScoreCard()
    print(score)
