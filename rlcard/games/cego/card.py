from termcolor import colored
from utils import compare_card_rank


def map_suit_to_color(suit):
    switcher = {
        "c": "grey",
        "d": "red",
        "h": "red",
        "s": "grey",
        "trump": "yellow",
    }
    return switcher.get(suit, "Invalid suit")


def map_suit_to_symbol(suit):
    switcher = {
        "c": "♣",
        "d": "♦",
        "h": "♥",
        "s": "♠",
        "trump": "★",
    }

    return switcher.get(suit, "Invalid suit")


class CegoCard:

    info = {
        "suits": ["c", "d", "h", "s", "trump"],
        "ranks": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                  "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                  "21", "gstieß",
                  "b", "r", "d", "k"],
        "cards": [
            "7-c", "8-c", "9-c", "10-c", "b-c", "r-c", "d-c", "k-c",
            "7-s", "8-s", "9-s", "10-s", "b-s", "r-s", "d-s", "k-s",
            "4-d", "3-d", "2-d", "1-d", "b-d", "r-d", "d-d", "k-d",
            "4-h", "3-h", "2-h", "1-h", "b-h", "r-h", "d-h", "k-h",
            "1-trump", "2-trump", "3-trump", "4-trump", "5-trump",
            "6-trump", "7-trump", "8-trump", "9-trump", "10-trump",
            "11-trump", "12-trump", "13-trump", "14-trump", "15-trump",
            "16-trump", "17-trump", "18-trump", "19-trump", "20-trump",
            "21-trump", "gstieß-trump"
        ],
        "color_card_values": {
            "k": 4.5,
            "d": 3.5,
            "r": 2.5,
            "b": 1.5,
        },
        "trump_card_values": {
            "1": 4.5,
            "21": 4.5,
            "gstieß": 4.5,
        }
    }

    def __init__(self, suit, rank):
        ''' Initialize the class of CegoCard

        Args:
            suit (str): The suit of card
            trait (str): The trait of card
        '''
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + '-' + self.suit

    def __gt__(self, other):
        if self.suit == other.suit:
            return self.rank > other.rank
        else:
            return self.suit > other.suit

    def get_value(self):
        if self.rank in CegoCard.info["color_card_values"]:
            return CegoCard.info["color_card_values"][self.rank]

        if self.suit == "trump" and self.rank in CegoCard.info["trump_card_values"]:
            return CegoCard.info["trump_card_values"][self.rank]

        return 0.5

    @staticmethod
    def split_ranks():
        black_cards_ranks = CegoCard.info["ranks"][6:10] + \
            CegoCard.info["ranks"][22:]
        red_card_ranks = CegoCard.info["ranks"][0:4][::-1] + \
            CegoCard.info["ranks"][22:]
        trump_card_ranks = CegoCard.info["ranks"][:22]

        return black_cards_ranks, red_card_ranks, trump_card_ranks

    @staticmethod
    def print_cards(cards):
        if isinstance(cards, str):
            cards = [cards]
        for i, card in enumerate(cards):
            rank, suit = card.split('-')

        print(colored(rank+"-" + map_suit_to_symbol(suit),
              map_suit_to_color(suit)), end="")

        if i < len(cards) - 1:
            print(', ', end='')
