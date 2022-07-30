import rlcard
from rlcard.games.cego.utility.eval import analyse_card_round_position, convert_to_agents, compare_dmc_checkpoints


seeds = [12, 17, 20, 30, 33]
# seeds = [12]
num_games = 1000000

game_Setting = {
    'env_name': 'cego',
    'game_variant': 'standard',
    'game_judge_by_points': 0,
    'game_activate_heuristic': True,
    'game_train_env': [False, False, False, False],
    'game_analysis_mode': True
}

# "results/final_models/nfsp_models/nfsp_cego_player_0/checkpoint_4/model.pth"
# "results/final_models/dqn_models/dqn_cego_player_0/checkpoint_8/model.pth",
# "results/final_models/dmc_models/dmc_cego_final_player_0/dmc/0_2500048000.pth"

dmc_comparisson_models = [
    "results/final_models/dmc_models/dmc_cego_final_player_0/dmc/0_2500048000.pth",
    "random",
    "random",
    "random"
]


if __name__ == '__main__':
    # analyse_card_round_position(
    #     game_Setting, "DMC Player 0; Seed: 12", dmc_comparisson_models, 'results/analysis_results/dmc_card_tendency.png', num_games, 0, seeds[0])

    compare_dmc_checkpoints(
        game_Setting, "results/final_models/dmc_models/dmc_cego_final_player_0/dmc/", 1, 1000, 12)
