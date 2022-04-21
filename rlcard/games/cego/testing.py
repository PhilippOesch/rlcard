from dealer import CegoDealer as Dealer
from card import CegoCard as Card
from player import CegoPlayer as Player
import numpy as np
from utils import cards2list, get_cego_player_deck


if __name__ == "__main__":
    np_random = np.random.RandomState()

    dealer = Dealer(np_random)
    deck = dealer.deck
    sorted_deck = sorted(deck)

    players = [
        Player(0, np_random, True),
        Player(1, np_random),
        Player(2, np_random),
        Player(3, np_random)
    ]

    dealer.deal_cards(players[0])
    blinds = dealer.deal_blinds()
    print("Player 0:", cards2list(players[0].hand))
    print("Blinds:", cards2list(blinds))

    new_cards, throw_aways = get_cego_player_deck(players[0].hand, blinds)

    print("new cards:", cards2list(new_cards))
    print("Throw Away:", cards2list(throw_aways))

    print("--------------------------------")
    # print("Sorted Deck:", cards2list(sorted_deck))
