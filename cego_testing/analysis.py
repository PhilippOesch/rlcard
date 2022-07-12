# random against human

import rlcard
from rlcard.agents import RandomAgent
from rlcard.agents.human_agents.cego_human_agent import HumanAgent
import matplotlib.pyplot as plt

from rlcard.games.cego.utility.eval import analyse_card_trick_win_propabilities, analyse_propability_a_card_wins_a_trick, analyse_first_mover_advantage

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
        'game_variant': 'solo',
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


if __name__ == '__main__':
    # analyse_propability_a_card_wins_a_trick(
    #     "analysis_results/percentages_card_win_when_played_probs.json", env, num_games)

    analyse_first_mover_advantage("analysis_results", env, num_games)
