from copy import deepcopy
import numpy as np
from typing import Any

from rlcard.games.cego.utils import set_cego_player_deck
from rlcard.games.cego import Dealer
from rlcard.games.cego import Player
from rlcard.games.cego import Judger
from rlcard.games.cego import Round

num_cards_per_player = 11
num_blind_cards = 10


class CegoGame:
    num_rounds = 11
    num_actions = 54  # one action for each card

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

    def init_game(self) -> tuple[dict, Any]:
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

        # Count the round. There are 4 rounds in each game.
        self.round_counter = 0

        # cego player starts the game
        self.current_player = 0

        self.round = Round(self.np_random)
        self.round.start_new_round(0)

        state = self.get_state(self.current_player)

        self.history = []
        self.trick_history = []

        return state, self.round.current_player_idx

    def get_state(self, player_id) -> dict:
        """ get state """

        state = self.round.get_state(self.players[player_id])
        state['num_players'] = self.get_num_players()
        state['current_player'] = self.round.current_player_idx
        state['current_trick_round'] = self.round_counter
        state['played_tricks'] = self.round.trick_history
        return state

    def step(self, action) -> tuple[dict, Any]:

        if self.allow_step_back:
            # save current state for potential step back
            the_round = deepcopy(self.round)
            the_players = deepcopy(self.players)
            the_dealer = deepcopy(self.dealer)
            the_round_counter = deepcopy(self.round_counter)
            the_trick_history = deepcopy(self.trick_history)
            the_playoffs = deepcopy(self.payoffs)
            self.history.append(
                (the_round, the_players, the_dealer, the_round_counter, the_trick_history, the_playoffs))

        # playing of a single step
        self.round.proceed_round(self.players, action)

        """ if the round is over:
            1. save the trick in history
            3. get the winner
            2. update the payoffs
            4. start a new round
            5. count up the round

            """
        if self.round.is_over:
            self.trick_history.append(self.round.trick.copy())
            round_winner_idx = self.round.winner_idx
            self.playoffs = self.receive_payoffs(
                self.payoffs,
                self.players,
                round_winner_idx,
                self.round.trick.copy()
            )
            self.round.start_new_round(round_winner_idx)
            self.round_counter += 1

        player_id = self.round.current_player_idx
        state = self.get_state(player_id)

        return state, player_id

    def step_back(self) -> bool:
        if len(self.history) > 0:
            self.round, self.players, self.dealer, \
                self.round_counter, self.trick_history, self.payoffs = self.history.pop()
            return True
        return False

    def get_num_players(self) -> int:
        return self.num_players

    @staticmethod
    def get_num_actions() -> int:
        return CegoGame.num_actions

    def get_player_id(self) -> int:
        return self.round.current_player

    def is_over(self) -> bool:
        return self.round_counter >= CegoGame.num_rounds

    def get_payoffs(self) -> list:
        return self.payoffs

    def get_legal_actions(self) -> list:
        return self.round.get_legal_actions(self.round.current_player)
