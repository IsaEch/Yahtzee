class ScoreCard(object):
    row_descriptions = {0: "Upper Section", 1: "Aces", 2: "Twos", 3: "Threes", 4: "Fours", 5: "Fives", 6: "Sixes",
                        7: "TOTAL SCORE", 8: "BONUS", 9: "TOTAL", 10: "Lower Section", 11: "3 of a kind",
                        12: "4 of a kind", 13: "Full House", 14: "Small Straight", 15: "Large Straight", 16: "Yahtzee",
                        17: "Chance", 18: "Yahtzee Bonus", 19: "TOTAL: Upper", 20: "TOTAL: Lower",
                        21: "GRAND TOTAL"}
    def __init__(self):
        """Creates a 2d list that represents the Yahtzee score card to keep track of the player's score. It also has a
        dictionary that remembers when a category is filled"""
        # Create a 2D list to store the scorecard
        self.score = [[0]*7 for _ in range(22)]
        for n in range(22):
            if n < 22:
                self.score[n][0] = ScoreCard.row_descriptions[n]
            if n < 5:
                self.score[0][n+1] = n+1
        self.score[0][6] = "Score"
        # Create a dictionary to keep track of which cells are filled so that they can't be filled again and so 0's
        # are not filled in before selecting a category
        self.filled = {i: True if i in [0, 7, 8, 9, 10, 19, 20, 21] else False for i in range(22)}

        print(self.score)   # Debugging/Development
        print(self.filled)  # Debugging/Development

    def length(self):
        """Returns the length of the scorecard"""
        return len(self.score)

    def width(self):
        """Returns the width of the scorecard"""
        return len(self.score[0])

    def set_category(self, category_row: int, score: int, dice_list: list):
        """Set the score for a specific category on the scorecard and calls the update methods for the totals"""
        for n in range(1, 6):
            self.score[category_row][n] = dice_list[n-1]
        self.score[category_row][6] = score
        self.filled[category_row] = True
        # Update the total score for the corresponding section (upper or lower)
        if category_row < 7:
            self.update_upper_total(score)
        else:
            self.update_lower_total(score)
        # Update the bonus for the upper section if the total score is greater than or equal to 63
        self.update_bonus()

    def update_upper_total(self, score: int):
        """Update the upper total. Not to be confused with the total score with bonus"""
        self.score[7][6] += score
        print(self.score[7][1])

    def update_lower_total(self, score: int):
        """Update the lower total. Not to be confused with the total score with bonus"""
        self.score[20][1] += score

    def update_bonus(self):
        """Updates the bonus for the upper section"""
        if self.score[7][1] >= 63:
            self.score[8][1] = 35

    def __str__(self):
        """"Currently only using for debugging/development"""
        return f"{self.score}"


if __name__ == '__main__':
    score = ScoreCard()
    print(score)
