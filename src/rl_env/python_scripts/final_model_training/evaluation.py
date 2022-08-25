from rlcard.games.cego.utility.eval import compare_models_in_tournament

seeds = [31, 43, 67, 78, 112]
num_games = 1000

game_Settings = {
    'env_name': 'cego',
    'game_variant': 'standard',
    'game_judge_by_points': 0,
    'game_activate_heuristic': True,
    'game_train_env': [False, False, False, False],
    'game_analysis_mode': True
}

setup = [
    "results/final_models/dmc_models/dmc_cego_final/dmc/0_2500048000.pth",
    "results/final_models/dmc_models/dmc_cego_final/dmc/1_2500048000.pth",
    "results/final_models/dmc_models/dmc_cego_final/dmc/2_2500048000.pth",
    "results/final_models/dmc_models/dmc_cego_final/dmc/3_2500048000.pth",
]


if __name__ == '__main__':
    compare_models_in_tournament(
        "experiments/test.json", 
        game_Settings, 
        num_games,
        setup,
        seeds
    )
