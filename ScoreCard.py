class ScoreCard(object):
    row_descriptions = {0: "Upper Section", 1: "Aces", 2: "Twos", 3: "Threes", 4: "Fours", 5: "Fives", 6: "Sixes",
                        7: "TOTAL SCORE", 8: "BONUS", 9: "TOTAL", 10: "Lower Section", 11: "3 of a kind",
                        12: "4 of a kind", 13: "Full House", 14: "Small Straight", 15: "Large Straight", 16: "Yahtzee",
                        17: "Chance", 18: "Yahtzee Bonus", 19: "TOTAL: Upper", 20: "TOTAL: Lower",
                        21: "GRAND TOTAL"}
    def __init__(self):
        """Creates a 2d list that represents the Yahtzee score card to keep track of the player's score. It also has a
        dictionary that remebers when a category is filled"""
        # Create a 2D list to store the scorecard
        self.score = [[0]*6 for _ in range(22)]
        for n in range(22):
            if n < 22:
                self.score[n][0] = ScoreCard.row_descriptions[n]
            if n < 5:
                self.score[0][n+1] = n+1
        # Create a dictionary to keep track of which cells are filled so that they can't be filled again and so 0's
        # are not filled in before selecting a category
        self.filled = {i: True if i in [0, 7, 8, 9, 10, 19, 20, 21] else False for i in range(22)}

        print(self.score)   # Debugging/Development
        print(self.filled)  # Debugging/Development

    def length(self):
        return len(self.score)

    def width(self):
        return len(self.score[0])


    def __str__(self):
        return f"{self.score}"



if __name__ == '__main__':
    score = ScoreCard()
    print(score)
