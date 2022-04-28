# Cego RLCard

# Cego Environment

## The Classes

* **CegoCard**: the card class
* **CegoDealer**: the class for dealing cards
* **CegoPlayer**: the player class
* **CegoRound**: represents a round of Cego
* **CegoJudger**: Judges the round of Cego
* **Utils**: helper classes

### Card Encoding

For know the part of the game, where the cego player selects the blind cards will be ignored for the reason of simplifying the action space.

File: ./jsondata/action_space.json

"\[rank\]-\[suit\]"

| Index | Cards |
|:-----:|:-----:|
| 0-7 | Clubs |
| 8-15 | Spades |
| 16-23 | Hearts |
| 24-31 | Diamonds |
| 32-53 | Trumps |

## State Representation

The state the player can possibly observe is the following (not all information is encoded within the observation jet).

| Key | Description | Example |
|:---:|:-----------:|:-------:|
| **hand** | The cards, the player currently has on his hand: List | ['7-c', 'k-s', '1-trump', 'gstieß-trump'] |
| **trick** | The cards currently in the trick: List | ['7-c', 'k-s', '1-trump', 'gstieß-trump']  |
| **target** | The card that has to be served: str | '11-trump' |
| **winner_card** | The card that currently wins the trick: str | 'gstieß-trump' |
| **winner_player** | The player that currently wins the trick: int | 2 |
| **valued_cards** | cards that the cego player (only the cego player knows of these) has layed aside: List | ['7-c', 'k-s', '1-trump', 'gstieß-trump' ...] |
| **legal_actions** | The action the player is allowed to play: List | ['12-trump', '14-trump'] |
| **start_player** | The player who started the current round: int | 0 |
| **num_players** | The Number of players playing: int | 4 |
| **current_player** | The current player: int | 2 |
| **current_trick_winner** | The player who currently wins the trick: int| 1 |
| **played_tricks** | The tricks that have already been played: 2D-List | [['7-c', 'k-s', '1-trump', 'gstieß-trump'], [...], ...] |
| **last_round_winner** | The winner of the last round: int | 3 |

The Observation Shape has the Size of **7 x 54**. For the first 6 planes the Shape **54** represents the amount of different cards. The last plane is used to encode general information about the game. 

The following table shows the encoding of the different planes:

| Plane | Description |
|:-----:|:-----------:|
| 0 | The cards the player has on his hand |
| 1 | The cards the cego player (only he can see them) has taken layed aside |
| 2 | The winning card of the trick |
| 3 | All the cards within the current trick |
| 4 | The cards that already have been played |
| 5 | [0-3]: For the player, part of the team the value is 1 <br> [4-7]: The player who currently would win the trick is encoded (one hot) <br>[8-11]: The player who started the current round is encoded (one hot) |

## Classes

### Card

This class contains the static attribute info, which contains information about the card suits, ranks and values of the cards, as well as a couple static helper methods for printing and comparing.

#### Attributes

* **suit**: the suit of the card
* **rank**: the rank of the card

### Round 

This class represents a single round. The first player of the round is the winner of the previous round. Cego consists of 11 rounds.

### Judger

The judger class generates the payoffs for the players.

If the player who receives the reward is the cego player only this player receives it. If the player who receives the reward is not the cego player, everybody but the cego player receives the reward.

### Dealer

The object, responsible for shuffling and dealing the cards to the players (11 each). This class also deals the blind cards (10 cards).

### Player

This class represents a player in the game. There is one special case of player, the cego player, which is indicated through the boolean-attibute **is_cego_player**. In this case the player gets a list **valued_cards**, which contains the cards the cego player has layed aside.

### Utils

Helper functions are within file **utils.py**.

### Game

This class represent the game itself and manages the full game state.

### Testing

**test.py** contains the test cases for the game.
