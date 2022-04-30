from rlcard.games.cego.utils import init_deck


class CegoDealer:
    ''' The class to deal the cards to the players 

    Class Attributes:
        - num_blind_cards: the number of blind cards
        - num_player_cards: the number of cards each player gets

    Instance Attributes:
        - np_random: numpy random state
        - deck: the deck of cards
    '''

    num_blind_cards = 10
    num_player_cards = 11

    def __init__(self, np_random):
        self.np_random = np_random
        self.deck = init_deck()
        self.shuffle()

    def shuffle(self) -> None:
        self.np_random.shuffle(self.deck)

    def deal_cards(self, player) -> None:
        for _ in range(CegoDealer.num_player_cards):
            player.hand.append(self.deck.pop())

    def deal_blinds(self) -> list:
        blinds = []
        for _ in range(CegoDealer.num_blind_cards):
            blinds.append(self.deck.pop())
        return blinds
