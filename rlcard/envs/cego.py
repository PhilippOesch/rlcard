import numpy as np
from collections import OrderedDict

import rlcard
from rlcard.envs import Env
from rlcard.games.cego import Game
from rlcard.games.cego.utils import ACTION_LIST, ACTION_SPACE
from rlcard.games.cego.utils import cards2list, get_tricks_played, set_observation

DEFAULT_GAME_CONFIG = {
    'game_num_players': 4,
}


class CegoEnv(Env):
    ''' Cego Environment

    Instance Attributes:
        - name (str): the name of the game
        - default_game_config (dict): the default game config
        - game (Game): the game instance
        - state_shape (list): the shape of the state space
        - action_shape (list): the shape of the action space
    '''

    def __init__(self, config):
        ''' Initialize the Cego environment
        '''
        self.name = 'cego'
        self.default_game_config = DEFAULT_GAME_CONFIG
        self.game = Game()
        super().__init__(config)
        self.state_shape = [[6, 54] for _ in range(self.num_players)]
        self.action_shape = [None for _ in range(self.num_players)]

    def _extract_state(self, state) -> OrderedDict:
        ''' Extract the observation for each player

        Parameters:
            - state (dict): the state of the game

        Observation Representation
            - plane 0: [0] own cards
            - plane 0: [1] valued cards
            - plane 0: [2] winner of trick
            - plane 0: [3] cards in trick
            - plane 0: [4] cards played
            - plane 0: [5]
                - [0-3]: who is part of the team
                - [4-7]: who wins the current round
                - [8-11]: player who started the trick round
            - plane 1: 54 - cards
        '''
        extracted_state: dict = OrderedDict()
        legal_actions: OrderedDict = self._get_legal_actions()
        obs = np.zeros((6, 54), dtype=int)  # observation is a (6, 54) tensor

        winner_card_idx: int = None
        hand_cards_idx: list = []
        values_cards_idx: list = []
        trick_card_idx: list = []
        played_cards_idx: list = []

        hand_cards_idx = [ACTION_SPACE[card] for card in state['hand']]
        values_cards_idx = [ACTION_SPACE[card]
                            for card in state['valued_cards']]

        if state['winner_card'] in ACTION_SPACE:
            winner_card_idx = ACTION_SPACE[state['winner_card']]
        if state['trick'] is not None:
            trick_card_idx = [ACTION_SPACE[card] for card in state['trick']]
        if state['played_tricks'] is not None:
            played_cards_idx = get_tricks_played(state['played_tricks'])

        winner_idx = state['winner']
        start_player_idx = state['start_player']
        current_player_idx = state['current_player']

        # setup observation
        obs[0][hand_cards_idx] = 1
        obs[1][values_cards_idx] = 1

        # TODO: Create a Helper function, that set the second plane of an observation

        if winner_card_idx is not None:
            # print(type(winner_card_idx))
            # print(len(winner_card_idx))
            # # obs[2][winner_card_idx] = 1
            # print('winner_card_idx: ', winner_card_idx)
            # set_observation(obs, 2, winner_card_idx)
            obs[2][winner_card_idx] = 1
        if trick_card_idx != None:
            obs[3][trick_card_idx] = 1
        if state['played_tricks'] is not None:
            obs[4][played_cards_idx] = 1

        if current_player_idx == 0:
            obs[5][0] = 1
        else:
            obs[5][[1, 2, 3]] = 1

        if winner_idx != None:
            obs[5][winner_idx+4] = 1

        if start_player_idx != None:
            obs[5][start_player_idx+8] = 1

        # setup extracted state
        extracted_state['obs'] = obs
        extracted_state['legal_actions'] = legal_actions
        extracted_state['raw_obs'] = state
        extracted_state['raw_legal_actions'] = [
            a for a in state['legal_actions']]
        extracted_state['action_record'] = self.action_recorder

        return extracted_state

    def get_payoffs(self) -> np.NDArray:
        ''' Get the payoffs of the players'''

        payoffs = self.game.get_payoffs()
        return np.array(payoffs)

    def _decode_action(self, action_id):
        ''' Decode the action id into the action
        '''

        legal_ids = self._get_legal_actions()
        if action_id in legal_ids:
            return ACTION_LIST[action_id]

        return ACTION_LIST[np.random.choice(legal_ids)]

    def _get_legal_actions(self) -> OrderedDict:
        ''' Get the legal actions of the current state'''

        legal_actions = self.game.get_legal_actions()
        legal_ids = {ACTION_SPACE[action]: None for action in legal_actions}
        return OrderedDict(legal_ids)

    def get_perfect_information(self) -> dict:
        ''' Get the perfect information of the current state '''
        state = {}
        state['num_players'] = self.num_players
        state['hand_cards'] = [cards2list(player.hand)
                               for player in self.game.players]
        state['valued_cards'] = [cards2list(player.valued_cards)
                                 for player in self.game.players]
        state['trick'] = cards2list(self.game.round.trick)
        state['played_tricks'] = [cards2list(trick)
                                  for trick in self.game.trick_history]
        state['current_player'] = self.game.round.current_player
        state['legal_actions'] = self.game.round.get_legal_actions(
            self.game.players[state['current_player']]
        )
        return state
