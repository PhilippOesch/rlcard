# Cego RLCard

## Card

### Attributes

* **suit**: the suit of the card
* **rank**: the rank of the card

### Card Encoding

File: ./jsondata/action_space.json

"\[rank\]-\[suit\]"

| Index | Cards |
|:-----:|:-----:|
| 0-7 | Clubs |
| 8-15 | Spades |
| 16-23 | Hearts |
| 24-31 | Diamonds |
| 32-53 | Trumps |
| 54 | Action for throwing away card from hand (cego-player) |
| 55 | Action for taking card with you (cego-player) |
