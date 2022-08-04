from rlcard.games.cego.utility.eval import analyse_card_round_position, convert_to_agents, \
    compare_dmc_checkpoints, get_percentages_relative_to_trick, \
    compare_models_in_tournament, get_low_cards, get_high_cards, split_80_20_cards, create_bar_graph, \
    create_bar_graph_colored


seeds = [12, 17, 20, 30, 33]
# seeds = [12]
num_games = 50000

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
# "results/final_models/dmc_models/dmc_cego_final_other_players/dmc/0_2500048000.pth"

dmc_dqn_comparisson_models = [
    "results/final_models/dmc_models/dmc_cego_final_other_players/dmc/0_2500048000.pth",
    "results/final_models/dqn_models/dqn_cego_player_0/checkpoint_8/model.pth",
    "random",
    "random"
]

dqn_dmc_comparisson_models = [
    "results/final_models/dqn_models/dqn_cego_player_0/checkpoint_8/model.pth",
    "results/final_models/dmc_models/dmc_cego_final_other_players/dmc/0_2500048000.pth",
    "random",
    "random"
]

dmc_nfsp_comparisson_models = [
    "results/final_models/dmc_models/dmc_cego_final_other_players/dmc/0_2500048000.pth",
    "results/final_models/nfsp_models/nfsp_cego_player_0/checkpoint_4/model.pth",
    "random",
    "random"
]

nfsp_dmc_comparisson_models = [
    "results/final_models/nfsp_models/nfsp_cego_player_0/checkpoint_4/model.pth",
    "results/final_models/dmc_models/dmc_cego_final_other_players/dmc/0_2500048000.pth",
    "random",
    "random"
]

dmc_comparisson_models = [
    "results/final_models/dmc_models/dmc_cego_final_other_players/dmc/0_2500048000.pth",
    "random",
    "random",
    "random"
]


if __name__ == '__main__':

    # over 1,000 games:
    # compare_dmc_checkpoints(
    #     game_Setting, "results/final_models/dmc_models/dmc_cego_final_other_players/dmc/", 0, 1000, 15)
    # compare_dmc_checkpoints(
    #     game_Setting, "results/final_models/dmc_models/dmc_cego_final_other_players/dmc/", 1, 1000, 15)
    # compare_dmc_checkpoints(
    #     game_Setting, "results/final_models/dmc_models/dmc_cego_final_player_0/dmc/", 0, 1000, 15)
    # compare_dmc_checkpoints(
    #     game_Setting, "results/final_models/dmc_models/dmc_cego_final_player_0/dmc/", 1, 1000, 15)

    # split_80_20_cards(
    #     "results/analysis_results/percentages_card_win_when_played_probs.json", "rlcard/games/cego/jsondata", 80, True)

    # compare_models_in_tournament("results/evaluation/dmc_vs_dqn_2.json",
    #                              game_Setting, num_games, dmc_dqn_comparisson_models, seeds)

    # compare_models_in_tournament("results/evaluation/dqn_vs_dmc_2.json",
    #                              game_Setting, num_games, dqn_dmc_comparisson_models, seeds)

    # compare_models_in_tournament("results/evaluation/dmc_vs_nfsp_2.json",
    #                              game_Setting, num_games, dmc_nfsp_comparisson_models, seeds)

    # compare_models_in_tournament("results/evaluation/nfsp_vs_dmc_2.json",
    #                              game_Setting, num_games, nfsp_dmc_comparisson_models, seeds)

    compare_models_in_tournament("results/evaluation/dmc_2.json",
                                 game_Setting, num_games, dmc_comparisson_models, seeds)

    dmc_comparisson_models

    # results/analysis_results/percentages_trick_win_probs.json
    # create_bar_graph_colored("results/analysis_results/percentages_trick_win_probs.json",
    #                          "results/analysis_results/trick_percentages_visual_colored.png", 80)
    # create_bar_graph_colored("results/analysis_results/percentages_card_win_when_played_probs.json",
    #                          "results/analysis_results/card_percentages_visual_colored.png", 80, True)
