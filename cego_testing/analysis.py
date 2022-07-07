# random against human

import rlcard
from rlcard.agents import RandomAgent
from rlcard.agents.human_agents.cego_human_agent import HumanAgent, _print_action

from rlcard.games.cego.utils import load_model, ACTION_SPACE, cards2list
import os
import json

from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
)

num_games = 1000000

env = rlcard.make(
    'cego',
    config={
        'seed': 20,
        'game_variant': 'standard',
        'game_activate_heuristic': False,
        'game_judge_by_points': 0,
        'game_train_players': [False, False, False, False],
        'game_analysis_mode': True
    })

device = get_device()

agents = [RandomAgent(env.num_actions) for _ in range(env.num_players)]

env.set_agents(
    [RandomAgent(env.num_actions) for _ in range(env.num_players)]
)


def analyse_card_trick_win_propabilities(path):
    trick_wins: dict = {}

    for key in ACTION_SPACE:
        trick_wins[key] = 0

    num_trick_wins = 0
    for i in range(num_games):
        print("episode:", i)
        trajectories, payoffs, state = env.run(is_training=False)
        for card in cards2list(state['winning_card_history']):
            trick_wins[card] += 1
            num_trick_wins += 1

    for entry in trick_wins:
        trick_wins[entry] /= (num_games*11)

    sorted_by_prob = {k: v for k, v in sorted(
        trick_wins.items(), key=lambda item: item[1], reverse=True)}
    print(sorted_by_prob)

    with open(path, 'w') as f:
        json.dump(sorted_by_prob, f, indent=4)


if __name__ == '__main__':
    analyse_card_trick_win_propabilities(
        'analysis_results/trick_win_probs.json')
