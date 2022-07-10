from rlcard.games.cego import Game

from rlcard.games.cego import Dealer
from rlcard.games.cego import Player
from rlcard.games.cego import JudgerUltimo
from rlcard.games.cego import Round
from rlcard.games.cego import Game

from rlcard.games.cego.utility.game import cards2list

from typing import Any


class CegoGameUltimo(Game):
    ''' This is the Ultimo Variant of Cego

    The Player who plays alone (player 0) has to win the last trick with the card "1-trump"
    '''

    def init_game(self) -> tuple[dict, Any]:
        self.points = [0 for _ in range(self.num_players)]
        self.winning_card_history = []
        self.start_player_history = [0]
        self.winning_player_history = []

        # Initialize a dealer that can deal cards
        if self.activate_heuristic:
            self.dealer = Dealer(self.np_random, 'ultimo_strict')
        else:
            self.dealer = Dealer(self.np_random, 'ultimo')

        # Initialize players to play the game
        self.players = [Player(i, self.np_random)
                        for i in range(self.num_players)]

        # player 0 is the solo player
        self.players[0].is_single_player = True

        self.judger = JudgerUltimo(self.np_random)

        # deal cards to player
        for i in range(self.num_players):
            self.dealer.deal_cards(self.players[i])

        # deal blind cards
        self.blind_cards = self.dealer.deal_blinds()

        # Count the round. There are 4 rounds in each game.
        self.round_counter = 0

        # player who starts the game
        self.current_player = 0

        self.round = Round(self.np_random)
        self.round.start_new_round(0)

        state = self.get_state(self.current_player)

        self.history = []
        self.trick_history = []

        return state, self.round.current_player_idx

    def on_round_over(self):
        self.trick_history.append(cards2list(self.round.trick.copy()))
        self.last_round_winner_idx = self.round.winner_idx
        self.points = self.judger.update_points(
            self.points,
            self.players,
            self.last_round_winner_idx,
            self.round.trick.copy(),
            self.round.winner_card
        )
        self.winning_card_history.append(self.round.winner_card)
        self.winning_player_history.append(self.round.winner_idx)
        self.start_player_history.append(self.round.winner_idx)
        self.round.start_new_round(self.last_round_winner_idx)
        self.round_counter += 1

    def is_over(self) -> bool:
        # if the player has more then one trick, the game is over
        cardlist = cards2list(self.round.trick)

        if '1-trump' in cardlist and self.round_counter+1 < Game.num_rounds:
            return True
        return self.round_counter >= Game.num_rounds

    def get_payoffs(self) -> list:
        if self.judge_by_points == 0:
            return self.judger.judge_game_zero_to_one(self.points)
        if self.judge_by_points == 1:
            return self.judger.judge_game_minusone_to_one(self.points)
