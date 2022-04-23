import numpy as np
from collections import OrderedDict

import rlcard
from rlcard.envs import Env
from rlcard.games.cego import Game
from rlcard.games.cego.utils import ACTION_LIST, ACTION_SPACE, ACTION_TO_IDX_DICT
from rlcard.games.cego.utils import cards2list, get_tricks_played

DEFAULT_GAME_CONFIG = {
    'game_num_players': 4,
}


class CegoEnv(Env):
    ''' Cego Environment
    '''

    def __init__(self, config):
        ''' Initialize the Cego environment
        '''
        self.name = 'cego'
        self.default_game_config = DEFAULT_GAME_CONFIG
        self.game = Game()
        super().__init__(config)
        '''
            plane 0: [0] own cards
            plane 0: [1] valued cards
            plane 0: [2] winner of trick
            plane 0: [3] target of trick
            plane 0: [4] cards in trick
            plane 0: [5] cards played
            plane 0: [6]
                [0-3]: who is part of the team
                [4-7]: who wins the current round
                [8-11]: player who started the trick round
            plane 1: 54 - cards
        '''
        self.state_shape = [[7, 54] for _ in range(self.num_players)]
        self.action_shape = [None for _ in range(self.num_players)]

    def _extract_state(self, state):

        extracted_state = {}
        legal_actions = self._get_legal_actions()
        obs = np.zeros((7, 54), dtype=int)
        hand_cards_idx = [ACTION_TO_IDX_DICT[card] for card in state['hand']]
        values_cards_idx = [ACTION_TO_IDX_DICT[card]
                            for card in state['valued_cards']]

        winner_card_idx = state['winner_card']
        target_card_idx = state['target']
        trick_card_idx = [ACTION_TO_IDX_DICT[card] for card in state['trick']]
        played_cards_idx = get_tricks_played(state['played_tricks'])

        winner_idx = state['winner']
        start_player_idx = state['start_player']
        current_player_idx = state['current_player']

        # setup observation
        obs[0, hand_cards_idx] = 1
        obs[1, values_cards_idx] = 1
        if winner_card_idx is not None:
            obs[2, winner_card_idx] = 1
        if target_card_idx is not None:
            obs[3, target_card_idx] = 1
        obs[4, trick_card_idx] = 1
        obs[5, played_cards_idx] = 1

        if current_player_idx == 0:
            obs[6, 0] = 1
        else:
            obs[6, [1, 2, 3]] = 1

        obs[6, (winner_idx+4)] = 1
        obs[6, (start_player_idx+8)] = 1

        # setup extracted state
        extracted_state['legal_actions'] = legal_actions
        extracted_state['obs'] = obs
        extracted_state['raw_obs'] = state
        extracted_state['raw_legal_actions'] = [
            a for a in state['legal_actions']]
        extracted_state['action_record'] = self.action_recorder

        return extracted_state

    def get_payoffs(self):
        return np.array(self.game.get_payoffs())

    def _decode_action(self, action_id):
        legal_ids = self._get_legal_actions()
        if action_id in legal_ids:
            return ACTION_LIST[action_id]

        return ACTION_LIST[np.random.choice(legal_ids)]

    def _get_legal_actions(self):
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
