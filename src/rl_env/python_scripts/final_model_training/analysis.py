from rlcard.games.cego.utility.eval import analyze_card_round_position

num_games = 1000

game_Settings = {
    'env_name': 'cego',
    'game_variant': 'standard',
    'game_judge_by_points': 0,
    'game_activate_heuristic': True,
    'game_train_env': [False, False, False, False],
    'game_analysis_mode': True
}

comparison_models = [
    "results/final_models/dmc_models/dmc_cego_final/dmc/0_2500048000.pth",
    "random",
    "random",
    "random"
]

if __name__ == '__main__':
    analyze_card_round_position(
        game_Settings,
        "Cego card play tendency",
        comparison_models,
        "experiments/cego_card_round_play.png",
        num_games,
        0,
        15
    )
