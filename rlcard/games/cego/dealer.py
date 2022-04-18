from utils import init_deck

num_blind_cards = 10
num_player_cards = 11


class CegoDealer:
    def __init__(self, np_random):
        self.np_random = np_random
        self.deck = init_deck()
        self.shuffle()

    def shuffle(self):
        self.np_random.shuffle(self.deck)

    def deal_cards(self, player):
        for _ in num_player_cards:
            player.hand.append(self.deck.pop())

    def deal_blinds(self, player):
        for _ in num_blind_cards:
            player.blinds.append(self.deck.pop())
