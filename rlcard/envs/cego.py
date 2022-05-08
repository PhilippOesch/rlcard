import numpy as np
from collections import OrderedDict

import rlcard
from rlcard.envs import Env
from rlcard.games.cego import GameStandard, GameSolo
from rlcard.games.cego.utils import ACTION_LIST, ACTION_SPACE
from rlcard.games.cego.utils import cards2list, encode_observation_var0, encode_observation_var1

DEFAULT_GAME_CONFIG = {
    'game_num_players': 4,
    'game_variant': 'standard',
    'game_judge_by_points': 0, # 0: judge by points, 1: judge by game, 2: judge by game var2 
}


def map_to_Game(variant_name):
    switcher: dict = {
        'standard': GameStandard,
        'solo': GameSolo,
    }

    return switcher.get(variant_name, "Invalid variant name")


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

        # select the proper game variant
        variant = config['game_variant'] if 'game_variant' in config else 'standard'
        self.game = map_to_Game(variant)()

        # select wheater the game payoffs are judged by points or by wins
        self.game.judge_by_points= config['game_judge_by_points'] if 'game_judge_by_points' in config else 0

        super().__init__(config)
        self.state_shape = [[336] for _ in range(self.num_players)]
        self.action_shape = [None for _ in range(self.num_players)]

    def _extract_state(self, state) -> OrderedDict:
        ''' Extract the observation for each player

        '''
        extracted_state: dict = OrderedDict()
        legal_actions: OrderedDict = self._get_legal_actions()

        # setup extracted state
        extracted_state['obs'] = encode_observation_var1(state)
        extracted_state['legal_actions'] = legal_actions
        extracted_state['raw_obs'] = state
        extracted_state['raw_legal_actions'] = [
            a for a in state['legal_actions']]
        extracted_state['action_record'] = self.action_recorder

        return extracted_state

    def get_payoffs(self):
        ''' Get the payoffs of the players'''

        payoffs = self.game.get_payoffs()
        return np.array(payoffs)

    def _decode_action(self, action_id):
        ''' Decode the action id into the action
        '''

        legal_ids = self._get_legal_actions()

        # if the action is legal, return the action
        if action_id in legal_ids:
            return ACTION_LIST[action_id]

        # else return a random legal action
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
