from rlcard.games.cego import Game

from rlcard.games.cego import Dealer
from rlcard.games.cego import Player
from rlcard.games.cego import JudgerRaeuber
from rlcard.games.cego import Round

from typing import Any

class CegoGameRaeuber(Game):
    ''' This is the Räuber Variant of Cego

    In Räuber: 
    - every player plays against on another
    - the player loses who gets the most points

    '''

    def init_game(self) -> tuple[dict, Any]:
        self.points = [0 for _ in range(self.num_players)]

        # Initialize a dealer that can deal cards
        self.dealer = Dealer(self.np_random)

        # Initialize players to play the game
        self.players = [Player(i, self.np_random)
                        for i in range(self.num_players)]

        self.judger = JudgerRaeuber(self.np_random)

        # deal cards to player
        for i in range(self.num_players):
            self.dealer.deal_cards(self.players[i])

        # deal blind cards
        self.blind_cards = self.dealer.deal_blinds()

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