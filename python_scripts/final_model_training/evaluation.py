from rlcard.games.cego.utility.eval import compare_models_in_tournament, compare_dmc_checkpoints, compare_dmc_checkpoints


# seeds = [12, 17, 20, 30, 33]
seeds = [12]
env_name = 'cego'
game_variant = 'standard'
game_judge_by_points = 0
game_activate_heuristic = True
game_train_env = [False, False, False, False]
num_games = 10000

comparisson_models = [
    "results/final_models/dmc_models/dmc_cego_final_player_0/dmc/0_365756800.pth",
    "random",
    "random",
    "random"
]

game_Setting = {
    'env_name': env_name,
    'game_variant': game_variant,
    'game_judge_by_points': game_judge_by_points,
    'game_activate_heuristic': game_activate_heuristic,
    'game_train_env': game_train_env
}


if __name__ == '__main__':
    # compare_models_in_tournament(
    #     "results/analysis_results/test.json", game_Setting, num_games, comparisson_models, seeds)
    # compare_dmc_checkpoints(game_Setting, "results/final_models/dmc_models/dmc_cego_final_player_0/dmc/", 0)
    compare_dmc_checkpoints(
        game_Setting, 'results/final_models/dmc_models/dmc_cego_final_player_0/dmc/', 0, 1000, 20)
