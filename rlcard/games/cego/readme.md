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

## Card

### Attributes

* **suit**: the suit of the card
* **rank**: the rank of the card