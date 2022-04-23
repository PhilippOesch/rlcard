from copy import deepcopy
import numpy as np
from utils import set_cego_player_deck

from dealer import CegoDealer as Dealer
from player import CegoPlayer as Player
from judger import CegoJudger as Judger

num_cards_per_player = 11
num_blind_cards = 10


class CegoGame:

    def __init__(self, allow_step_back=False):
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.num_players = 4  # there are always 4 players in this game
        self.payoffs = [0 for _ in range(self.num_players)]

        self.dealer = None
        self.players = None
        self.judger = None
        self.round = None
        self.round_counter = None
        self.history = None
        self.trick_history = None
        self.blind_cards = None

    def configure(self, game_config):
        """Specify some game specific parameters, such as number of players"""
        self.num_players = game_config['game_num_players']

    def init_game(self):
        # Initialize a dealer that can deal cards
        self.dealer = Dealer(self.np_random)

        # Initialize players to play the game
        self.players = [Player(i, self.np_random)
                        for i in range(self.num_players)]

        # player 0 is the cego player
        self.players[0].is_cego_player = True

        self.judger = Judger(self.np_random)

        # deal cards to player
        for i in range(self.num_players):
            self.dealer.deal_cards(self.players[i])

        # deal blind cards to cego player
        self.blind_cards = self.dealer.deal_blinds()
        # update cego player deck
        set_cego_player_deck(self.players[0], self.blind_cards)

        # Cego player gets the points from the throw away cards
        self.payoffs = self.judger.receive_payoffs(
            self.payoffs,
            self.players,
            0,
            self.players[0].valued_cards
        )
