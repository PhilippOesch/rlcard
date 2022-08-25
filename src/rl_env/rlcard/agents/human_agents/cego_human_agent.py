from rlcard.games.cego.card import CegoCard


class HumanAgent(object):
    """ This human agent can be used to play against trained models
        for the game cego
    """

    def __init__(self, num_actions):
        self.use_raw = True
        self.num_actions = num_actions

    @staticmethod
    def step(state):
        print(state['raw_obs'])
        _print_state(state['raw_obs'], state['action_record'])
        action = int(input('>> You choose action (integer): '))
        while action < 0 or action >= len(state['legal_actions']):
            print('Action illegel...')
            action = int(input('>> Re-choose action (integer): '))
        return state['raw_legal_actions'][action]

    def eval_step(self, state):
        ''' Predict the action given the curent state for evaluation. The same to step here.

        Args:
            state (numpy.array): an numpy array that represents the current state

        Returns:
            action (int): the action predicted (randomly chosen) by the random agent
        '''
        return self.step(state), {}


def _print_state(state, action_record):
    _action_list = []
    print("Action Record:", action_record)
    for i in range(1, len(action_record)+1):
        if action_record[-1][0] == state['current_player']:
            break
        _action_list.insert(0, action_record[-i])
    for pair in _action_list:
        print('>> Player', pair[0], 'chooses ', end='')
        _print_action(pair[1])
        print('')

    print('\n==== Last Round Winner: Player',
          state['last_round_winner'], '====')

    print('\n==== Round', state['current_trick_round'], ' ====')
    print('\n=============== Your Hand ===============')
    CegoCard.print_cards(state['hand'])
    print('\n=============== Trick Cards ===============')
    CegoCard.print_cards(state['trick'])
    print('')
    print('======== Actions You Can Choose =========')
    for i, action in enumerate(state['legal_actions']):
        print(str(i)+': ', end='')
        CegoCard.print_cards(action)
        if i < len(state['legal_actions']) - 1:
            print(', ', end='')
    print('\n')


def _print_action(action):
    ''' Print out an action in a nice form

    Args:
        action (str): A string a action
    '''
    CegoCard.print_cards(action)
