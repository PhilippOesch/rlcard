# random against human

import rlcard
from rlcard.games.cego.utility.eval import analyse_card_round_position, convert_to_agents

from rlcard.utils import (
    get_device,

)

num_games = 100000

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

comparisson_models = [
    "results/final_models/dmc_cego/dmc/0_5366425600.pth",
    "random",
    "random",
    "random"
]

device = get_device()
agents = convert_to_agents(comparisson_models, env, device)
env.set_agents(agents)


if __name__ == '__main__':
    analyse_card_round_position(
        env, "results/analysis_results/card_round.png", num_games, 0)
