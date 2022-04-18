from dealer import CegoDealer as Dealer
import numpy as np
# from utils import cards2list


if __name__ == "__main__":
    np_random = np.random.RandomState()

    dealer = Dealer(np_random)

    print("deck length:", len(dealer.deck))
