from rlcard.games.cego.utility.eval import analyse_card_round_position, convert_to_agents, \
    compare_dmc_checkpoints, get_percentages_relative_to_trick, \
    compare_models_in_tournament, get_low_cards, get_high_cards, split_80_20_cards, create_bar_graph, \
    create_bar_graph_colored, plot_curve, plot_combined, tournament_appg_and_wp_cego, refactor_training_graph


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
    # pass
    # over 1,000 games:

    compare_dmc_checkpoints(
        game_Setting,
        "results/final_models/dmc_models/dmc_bettel_final_other_players/dmc/",
        "bettel_player_0_seed_15_1000_games.csv",
        [True, False, False, False],
        1000,
        15)

    compare_dmc_checkpoints(
        game_Setting,
        "results/final_models/dmc_models/dmc_bettel_final_other_players/dmc/",
        "bettel_player_1_seed_15_1000_games.csv",
        [False, True, False, False],
        1000,
        15)

    compare_dmc_checkpoints(
        game_Setting,
        "results/final_models/dmc_models/dmc_bettel_final_other_players/dmc/",
        "bettel_other_players_seed_15_1000_games.csv",
        [False, True, True, True],
        1000,
        15)

    compare_dmc_checkpoints(
        game_Setting,
        "results/final_models/dmc_models/dmc_bettel_final_other_players/dmc/",
        "bettel_other_players_seed_15_1000_games.csv",
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
            'path': "results/final_models/dmc_models/dmc_ultimo_final_other_players/dmc/ultimo_player_0_seed_15_1000_games.csv",
            'team': 0,
            'name': "1 AI single player vs 3 random other players"
        },
        {
            'path': "results/final_models/dmc_models/dmc_ultimo_final_other_players/dmc/ultimo_player_1_seed_15_1000_games.csv",
            'team': 1,
            'name': "1 AI other player vs 3 random players"
        },
        {
            'path': "results/final_models/dmc_models/dmc_ultimo_final_other_players/dmc/ultimo_other_players_seed_15_1000_games.csv",
            'team': 1,
            'name': "3 AI other players vs 1 random single player"
        }
    ]

    # csv_paths = [
    #     {
    #         'path': 'results/final_models/dmc_models/dmc_cego_final_other_players/dmc/cego_player_0_seed_15_1000_games.csv',
    #         'team': 0,
    #         'name': 'DMC'
    #     },
    # ]

    plot_combined(
        csv_paths,
        'results/final_models/dmc_models/dmc_ultimo_final_other_players/ultimo_traing_progress_graph.png',
        'checkpoint',
        'APPG',
        'Training Progress - Ultimo'
    )

    # refactor_training_graph(
    #     'results/final_models/nfsp_models/nfsp_cego_player_0/performance.csv',
    #     'NFSP',
    #     'APPG',
    #     'timestep',
    #     'Training Progress - Bettel',
    #     'results/final_models/nfsp_models/nfsp_cego_player_0/training_progress_nfsp.png',
    #     200
    # )
