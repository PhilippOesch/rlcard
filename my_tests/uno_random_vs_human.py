# random against human

import rlcard
from rlcard.agents import RandomAgent
from rlcard.agents.human_agents.uno_human_agent import HumanAgent, _print_action

env = rlcard.make('uno')

random1 = RandomAgent(num_actions=env.num_actions)
human_agent = HumanAgent(env.num_actions)

env.set_agents([
    human_agent,
    random1
])

print(env.num_actions)  # 61
print(env.num_players)  # 2
print(env.state_shape)  # [[4, 4, 15], [4, 4, 15]]
print(env.action_shape)  # [None, None]

trajectories, payoffs = env.run(is_training=False)

while (True):
    print(">> Start a new game")

    trajectories, payoffs = env.run(is_training=False)
    # If the human does not take the final action, we need to
    # print other players action
    final_state = trajectories[0][-1]
    action_record = final_state['action_record']
    state = final_state['raw_obs']
    _action_list = []
    for i in range(1, len(action_record)+1):
        if action_record[-i][0] == state['current_player']:
            break
        _action_list.insert(0, action_record[-i])
    for pair in _action_list:
        print('>> Player', pair[0], 'chooses ', end='')
        _print_action(pair[1])
        print('')

    print('===============     Result     ===============')
    if payoffs[0] > 0:
        print('You win!')
    else:
        print('You lose!')
    print('')
    input("Press any key to continue...")
