from rlcard.games.cego.utility.eval import compare_models_in_tournament

import rlcard


seeds = [12, 17, 20, 30, 33]
env_name = 'cego'
game_variant = 'standard'
game_judge_by_points = 0
game_activate_heuristic = True
game_train_env = [False, False, False, False]
num_games = 1000

comparisson_models = [
    "final_models/dmc_models/dmc_cego/dmc/0_2873113600.pth",
    "random",
    "random",
    "random"
]

env = rlcard.make(
    env_name,
    config={
        'game_variant': game_variant,
        'game_judge_by_points': game_judge_by_points,
        'game_activate_heuristic': game_activate_heuristic,
    }
)


if __name__ == '__main__':
    compare_models_in_tournament(
        "final_models/test_result.json", env, num_games, comparisson_models, seeds)
