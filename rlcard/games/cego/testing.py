from dealer import CegoDealer as Dealer
import numpy as np
from utils import compare_trick_winner, cards2list
# from utils import cards2list


if __name__ == "__main__":
    np_random = np.random.RandomState()

    dealer = Dealer(np_random)
    deck = dealer.deck
    sorted_deck = sorted(deck, key=compare_trick_winner)

    # print(deck[0], deck[1], compare_trick_winner(deck[0], deck[1]))

    # print("deck length:", len(dealer.deck))
    print("Deck:", cards2list(sorted_deck))
