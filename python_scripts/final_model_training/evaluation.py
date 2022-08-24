from rlcard.games.cego.utility.eval import analyse_card_round_position, convert_to_agents, \
    compare_dmc_checkpoints, get_percentages_relative_to_trick, \
    compare_models_in_tournament, get_low_cards, get_high_cards, split_80_20_cards, create_bar_graph, \
    create_bar_graph_colored, plot_curve, plot_combined, tournament_appg_and_wp_cego, refactor_training_graph


# seeds = [12, 17, 20, 30, 33]
seeds = [31, 43, 67, 78, 112]
# seeds = [12]
num_games = 50000

game_Setting = {
    'env_name': 'cego',
    'game_variant': 'solo',
    'game_judge_by_points': 0,
    'game_activate_heuristic': True,
    'game_train_env': [False, False, False, False],
    'game_analysis_mode': True
}

# "results/final_models/nfsp_models/nfsp_cego_player_0/checkpoint_4/model.pth"
# "results/final_models/dqn_models/dqn_cego_player_0/checkpoint_8/model.pth",
# "results/final_models/dmc_models/dmc_cego_final_other_players/dmc/0_2500048000.pth"


setup_1 = [
    "results/final_models/dmc_models/dmc_solo_final_other_players/dmc/0_1500048000.pth",
    "random",
    "random",
    "random",
]

setup_2 = [
    "random",
    "results/final_models/dmc_models/dmc_solo_final_other_players/dmc/1_1500048000.pth",
    "random",
    "random",
]

setup_3 = [
    "results/final_models/dmc_models/dmc_solo_final_other_players/dmc/0_1500048000.pth",
    "results/final_models/dmc_models/dmc_solo_final_other_players/dmc/1_1500048000.pth",
    "random",
    "random",
]

setup_4 = [
    "results/final_models/dmc_models/dmc_solo_final_other_players/dmc/0_1500048000.pth",
    "results/final_models/dmc_models/dmc_solo_final_other_players/dmc/1_1500048000.pth",
    "results/final_models/dmc_models/dmc_solo_final_other_players/dmc/2_1500048000.pth",
    "results/final_models/dmc_models/dmc_solo_final_other_players/dmc/3_1500048000.pth",
]


if __name__ == '__main__':
    # pass
    # over 1,000 games:

    # compare_models_in_tournament(
    #     "results/evaluation/all_sub_games/solo_setup_1.csv",
    #     game_Setting,
    #     num_games,
    #     setup_1,
    #     seeds
    # )

    # compare_models_in_tournament(
    #     "results/evaluation/all_sub_games/solo_setup_2.csv",
    #     game_Setting,
    #     num_games,
    #     setup_2,
    #     seeds
    # )

    # compare_models_in_tournament(
    #     "results/evaluation/all_sub_games/solo_setup_3.csv",
    #     game_Setting,
    #     num_games,
    #     setup_3,
    #     seeds
    # )

    # compare_models_in_tournament(
    #     "results/evaluation/all_sub_games/solo_setup_4.csv",
    #     game_Setting,
    #     num_games,
    #     setup_4,
    #     seeds
    # )

    # compare_models_in_tournament(
    #     "results/evaluation/all_sub_games/raeuber_setup_5.csv",
    #     game_Setting,
    #     num_games,
    #     setup_5,
    #     seeds
    # )

    compare_dmc_checkpoints(
        game_Setting,
        "results/final_models/dmc_models/dmc_solo_final_other_players/dmc/",
        "solo_player_0_seed_15_1000_games.csv",
        [True, False, False, False],
        1000,
        15)

    compare_dmc_checkpoints(
        game_Setting,
        "results/final_models/dmc_models/dmc_solo_final_other_players/dmc/",
        "solo_player_1_seed_15_1000_games.csv",
        [False, True, False, False],
        1000,
        15)

    compare_dmc_checkpoints(
        game_Setting,
        "results/final_models/dmc_models/dmc_solo_final_other_players/dmc/",
        "solo_2_ai_players_seed_15_1000_games.csv",
        [True, True, False, False],
        1000,
        15)

    # compare_dmc_checkpoints(
    #     game_Setting,
    #     "results/final_models/dmc_models/dmc_piccolo_final_other_players/dmc/",
    #     "piccolo_3_ai_players_seed_15_1000_games.csv",
    #     [False, True, True, True],
    #     1000,
    #     15)

    compare_dmc_checkpoints(
        game_Setting,
        "results/final_models/dmc_models/dmc_solo_final_other_players/dmc/",
        "solo_all_players_seed_15_1000_games.csv",
        [True, True, True, True],
        1000,
        15)

    # tournament_appg_and_wp_cego("results/evaluation/dmc_vs_dqn_2.json",
    #                             game_Setting, num_games, dmc_dqn_comparisson_models, seeds)

    # tournament_appg_and_wp_cego("results/evaluation/dqn_vs_dmc_2.json",
    #                             game_Setting, num_games, dqn_dmc_comparisson_models, seeds)

    # tournament_appg_and_wp_cego("results/evaluation/dmc_vs_nfsp_2.json",
    #                             game_Setting, num_games, dmc_nfsp_comparisson_models, seeds)

    # tournament_appg_and_wp_cego("results/evaluation/nfsp_vs_dmc_2.json",
    #                             game_Setting, num_games, nfsp_dmc_comparisson_models, seeds)

    # tournament_appg_and_wp_cego("results/evaluation/dmc_2.json",
    #                             game_Setting, num_games, dmc_comparisson_models, seeds)

    csv_paths = [
        {
            'path': "results/final_models/dmc_models/dmc_raeuber_final_other_players/dmc/raeuber_player_0_seed_15_1000_games.csv",
            'team': 0,
            'name': "setup-1"
        },
        {
            'path': "results/final_models/dmc_models/dmc_raeuber_final_other_players/dmc/raeuber_2_ai_players_seed_15_1000_games.csv",
            'team': 1,
            'name': "setup-2"
        },
        {
            'path': "results/final_models/dmc_models/dmc_raeuber_final_other_players/dmc/raeuber_all_players_seed_15_1000_games.csv",
            'team': 0,
            'name': "setup-3"
        }
    ]

    # csv_paths = [
    #     {
    #         'path': 'results/final_models/dmc_models/dmc_cego_final_other_players/dmc/cego_player_0_seed_15_1000_games.csv',
    #         'team': 0,
    #         'name': 'DMC'
    #     },
    # ]

    # plot_combined(
    #     csv_paths,
    #     'results/final_models/dmc_models/dmc_raeuber_final_other_players/raeuber_traing_progress_graph.png',
    #     'checkpoint',
    #     'WP',
    #     'Training Progress - Räuber'
    # )

    # refactor_training_graph(
    #     'results/final_models/nfsp_models/nfsp_cego_player_0/performance.csv',
    #     'NFSP',
    #     'APPG',
    #     'timestep',
    #     'Training Progress - Bettel',
    #     'results/final_models/nfsp_models/nfsp_cego_player_0/training_progress_nfsp.png',
    #     200
    # )
