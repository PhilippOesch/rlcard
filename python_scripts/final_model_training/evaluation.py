from rlcard.games.cego.utility.eval import analyse_card_round_position, convert_to_agents, \
    compare_dmc_checkpoints, get_percentages_relative_to_trick, get_low_card, \
    compare_models_in_tournament, get_low_cards, get_high_cards


# seeds = [12, 17, 20, 30, 33]
seeds = [12]
num_games = 1000000

game_Setting = {
    'env_name': 'cego',
    'game_variant': 'ultimo',
    'game_judge_by_points': 0,
    'game_activate_heuristic': True,
    'game_train_env': [False, False, False, False],
    'game_analysis_mode': True
}

# "results/final_models/nfsp_models/nfsp_cego_player_0/checkpoint_4/model.pth"
# "results/final_models/dqn_models/dqn_cego_player_0/checkpoint_8/model.pth",
# "results/final_models/dmc_models/dmc_cego_final_player_0/dmc/0_2500048000.pth"

comparisson_models = [
    "random",
    "random",
    "random",
    "random"
]


if __name__ == '__main__':

    # compare_dmc_checkpoints(
    #     game_Setting, "results/final_models/dmc_models/dmc_cego_final_other_players/dmc/", 1, 1000, 12)

    # compare_models_in_tournament("results/analysis_results/compare_ultimo_with_heuristic_1_mill_seed_12.json",
    #                              game_Setting, num_games, comparisson_models, seeds)

    get_low_cards(
        "results/analysis_results/percentages_card_win_when_played_probs.json",
        "rlcard/games/cego/jsondata/low_cards.json"
    )

    get_high_cards(
        "results/analysis_results/percentages_card_win_when_played_probs.json",
        "rlcard/games/cego/jsondata/high_cards.json"
    )
