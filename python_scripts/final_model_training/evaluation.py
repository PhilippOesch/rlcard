from rlcard.games.cego.utility.eval import compare_models_in_tournament


# seeds = [12, 17, 20, 30, 33]
seeds= [12]
env_name = 'cego'
game_variant = 'standard'
game_judge_by_points = 0
game_activate_heuristic = True
game_train_env = [False, False, False, False]
num_games = 10000

comparisson_models = [
    "random",
    "results/final_models/nfsp_all_nfsp_agents/model_final_1.pth",
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
    compare_models_in_tournament(
        "results/analysis_results/test.json", game_Setting, num_games, comparisson_models, seeds)
