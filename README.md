
## 📦 Download

👉 [Download Yahtzee Project (v1.0)](https://github.com/IsaEch/Yahtzee/releases/download/V1.0/Yahtzee-main.zip)

# Yahtzee
**Game Controls**:
  •	Mouse: Click to adjust player count, click “Play”, “Roll”, and “Next”, and click on the category to score.
  •	Keyboard: Enter the players’ names on the Name Screen.
**Title Screen**:
1.	Play: Begins the game with the currently selected number of players.
2.	<: Decreases the total player count by 1 until it reaches 2 (Figure 3).
3.	>: Increases the total player count by 1 until it reaches 5 (Figure 4).
a.	Note: A visual indicator will appear on the button when the min or max number of players is reached.

 
**Name Screen**:
1.	Player Name Field: Enter the name of the player (Figure 5).
a.	Click on the Text Field to enter text.
b.	The Text Field while display a white border to indicate it is selected and able to receive text (Figure 6, 7).
2.	Enter: Accepts currently entered name as that player’s name and switches the screen to the next Player Name Field or the main Game Screen. 
3.	Note: The Player Name Field cannot be empty before moving onto the next player. The game will not let you to move to the next screen without entering a name first.


 
**Yahtzee Game Screen**:
The screen is split into 2 main sections: the Scorecard and the Dice (Figure 8)
1.	Scorecard: Holds all the score for that player. It consists of 13 different categories as well as bonuses and totals.
a.	Displays the name of the current player.
2.	Yellow Highlight: Indicate Scorecard categories that are not yet scored and available for selection.
3.	Gray Areas: Non-fillable sections that contains either the totals or bonuses.
4.	Dice: 5 dice that roll. The values of the dice affect the scoring for the selected category.
5.	Roll: Rolls the dice in the main dice area to get random values to score.
6.	Roll Counter: Keeps track of the total number of roles per turn.
a.	Max of 3 rolls per turn.
b.	Once a category is scored within a turn, no more rolls available until the next turn.
7.	Game Message: Provides instructions on what to do or what is happening.
8.	ScoreTable: Shows the first initial of all players in the game along with their total score.
a.	Hovering the cursor over an initial displays a tooltip of the player’s name.
9.	Hold Area: The red rectangle that serves as a spot to hold dice while rerolling the others.

 
**Results Screen**:
Displays all players will their final scores (Figure 9).
•	Players are arranged vertically from highest to lowest score.
•	The player with the most points is announced the winner at the top.
o	In the case of a tie, the game message indicates there is a tie (Figure 10).

 
**How to play**:
**Overview**: 
There are 13 different categories that need to be filled. The values of each dice will affect the scoring for the selected category. The categories are also split into the Upper and Lower Sections.
**Sections**:
The **Upper Section** consists of:
1.	Aces
2.	Twos
3.	Threes
4.	Fours
5.	Fives
6.	Sixes
The **Lower Section** consists of:
7.	3 of a Kind
8.	4 of a Kind
9.	Full House
10.	Small Straight
11.	Large Straight
12.	Yahtzee
13.	Chance
There are two **bonus options**:
1.	Upper-Level
2.	Yahtzee
   
**Game Play**: 
1.	Rolls: 
1.	Click “Roll” to roll the dice.
2.	There is a maximum of 3 rolls per turn 
3.	Once the 3 rolls have been used, a category must be selected to score.
4.	If you choose to score before the third roll, you can no longer roll again.
5.	You must roll at least once to begin the turn.
6.	Roll counter updates after every roll to show you how many rolls have been used.
2.	Holding Dice: 
1.	After the first roll, you may move any number of dice to the Hold Box (Red Rectangle).
2.	The Hold Box will hold the selected die and prevent it from being rerolled.
a.	This is the strategic part of Yahtzee that is used to achieve high scores.
3.	In order to hold a die, click on the die you want to move.
4.	The die will automatically move from the main dice area to the Hold Box (Figure 11).
5.	Note: you cannot hold any dice until you have rolled them at least once within the turn. They also cannot be held while rolling the dice.
 
3.	**Releasing Dice**: 
  1.	If you want to move a dice back to the main dice area to be rerolled, click on the desired die, and it will automatically move back to the main dice area (Figure 12).
  •	Note: Dice cannot be released while rolling the other dice.



 
4.	**Switching Players**:
  1.	Once you have scored a category, a “Next” button will appear under the “Roll” button (Figure 13). 
  2.	Clicking the “Next” button begins the next player transition (Figure 14).
  3.	In the middle of the transition, the game displays the name of the next player (Figure 15).
  4.	The game undoes the transition and shows the next player’s scorecard (Figure 16). 
 



5.	**Scoring a category**: 
  a.	To score a category, you click on one of the category rows that contains a yellow highlight when hovered.
  b.	If a row does not highlight when hovered, it means that it has already been filled or the turn is over.
  i.	Note: The row for “Lower Section” will not highlight because it is not a category.
  c.	Categories can only be scored after one dice roll. Any attempts before rolling the dice is ignored.
  d.	The score for each category is updated in the last column labeled “Score”. Additionally, the value of each die is recorded in column 1-5 for personal use.
  e.	The bonuses cannot be scored but are automatically factored when the conditions become true.
  6.	Scoring Rules:
**Upper Section**
  1.	Aces: Count how many values are 1. Multiply the value times the number of times it appears in the set of dice.
  a.	Ex. Dice: 5, 3, 1, 1, 2 -> 2 points
  2.	Twos: Count how many values are 2. Multiply the value times the number of times it appears in the set of dice.
  a.	Ex. Dice: 2, 2, 2, 6, 1 -> 6 points
  3.	Threes: Count how many values are 3. Multiply the value times the number of times it appears in the set of dice.
  a.	Ex. Dice: 3, 3, 3, 3, 3 -> 15 points
  4.	Fours: Count how many values are 4. Multiply the value times the number of times it appears in the set of dice.
  a.	Ex. Dice: 4, 5, 1, 2, 3 -> 4 points
  5.	Fives: Count how many values are 5. Multiply the value times the number of times it appears in the set of dice.
  a.	Ex. Dice: 3, 3, 5, 5, 2 -> 10 points
  6.	Sixes: Count how many values are 6. Multiply the value times the number of times it appears in the set of dice.
  a.	Ex. Dice: 6, 1, 1, 2, 3 -> 6 points
  These category scores make up the Total without the Bonus for the Upper Section.
7.	**Bonus (Upper Section)**: A bonus of 35 points is added only when the Upper Section score reaches 63 points.
8.	**Total of Upper Section**: Upper Section total with Bonus
a.	Ex. Total Section: 74 points, Bonus 35 points -> Total of Upper Section: 109
**Lower Section**
  9.	3 of a Kind: When there are at least 3 of the same value in the set of dice, add the sum of all the dice. 
  a.	Ex. 5, 5, 5, 3, 2 -> 20 points
  b.	However, if there are not at least 3 of the same value in the set of dice, the score is 0. 
  i.	Ex. 1, 2, 3, 4, 5 -> 0 points
  10.	4 of a Kind: When there are at least 4 of the same value in the set of dice, add the sum of all the dice.
  a.	Ex. 1, 1, 1, 1, 4 -> 8 points
  b.	However, if there are not at least 4 of the same value in the set of dice, the score is 0. 
  i.	Ex. 5, 5, 5, 3, 2-> 0 points
  11.	Full House: When there are 3 of a kind and 2 of a kind in the set of dice, the score is 25 points.
  a.	Ex. 2, 2, 2, 5, 5 -> 25 points
  12.	Small Straight: When there is a sequence of 4 values in the set of dice, the score is 30 points. They do not need to be in a consecutive order. Rather, it must be 4 different values in the set of the dice.
  a.	Ex. 5, 3, 2, 4, 4 -> 30 points
  13.	Full Straight: When there is a sequence of 5 values in the set of dice, the score is 40 points. They do not need to be in a consecutive order. Rather, they all must be different values.
  14.	Yahtzee: When all the dice have the same value, the score is 50 points. 
  a.	Ex. 5, 5, 5, 5, 5 -> 50 points
  b.	It also unlocks the ability to gain Yahtzee Bonuses
  15.	Chance: The sum of all values of the dice. 
  a.	Ex. 4, 3, 4, 2, 1 -> 14 points
  b.	Ex. 6, 1, 6, 4, 1 -> 18 points
  16.	**Yahtzee Bonus**: Can only occur when the Yahtzee category is filled with a Yahtzee.
  a.	After completing the Yahtzee Category, each additional Yahtzee is a 100 points bonus
  b.	If another category also has a Yahtzee, its bonus will be added only after the Yahtzee category is filled with a Yahtzee.
  c.	If the Yahtzee category is not filled with a Yahtzee, Yahtzee bonuses cannot be earned even if another category contains a Yahtzee.
  17.	Total of Lower Section: Total points of the Lower Section without the Bonuses.
  18.	**Grand Total**: Total of the Upper and Lower Sections with their bonuses. This is the player’s overall score.




