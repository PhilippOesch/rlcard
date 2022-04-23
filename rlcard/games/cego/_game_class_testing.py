from game import CegoGame as Game
from utils import cards2list


if __name__ == "__main__":
    game = Game()
    game.init_game()

    for player in range(len(game.players)):
        print("Player {}'s hand: {}".format(
            player, cards2list(game.players[player].hand)))

    print("Cego Player throw away cards: ",
          cards2list(game.players[0].valued_cards))

    print("Payoffs:", game.payoffs)
