import json
import os
import matplotlib.pyplot as plt
from rlcard.games.cego.utils import load_model
from scipy import stats
from rlcard.agents import (
    DQNAgent,
    RandomAgent,
    NFSPAgent
)

import rlcard

from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
)

seeds = [12, 17, 20, 30, 33]
env_name = 'cego'
game_variant = 'standard'
game_judge_by_points = 0
game_activate_heuristic = True
game_train_env= [False, False, False, False]
num_games = 50000


def compare_model_in_tournament(path, path_to_models):

    # Check whether gpu is available
    # device = get_device()
    device = get_device()

    all_rewards = []

    iterations_rewards = [0 for _ in range(len(path_to_models))]
    num_iterations = len(seeds)

    for seed in seeds:
        # Seed numpy, torch, random
        set_seed(seed)

        env = rlcard.make(
            env_name,
            config={
                'seed': seed,
                'game_variant': game_variant,
                'game_judge_by_points': game_judge_by_points,
                'game_activate_heuristic': game_activate_heuristic,

            }
        )

        agents = []
        for position, model_path in enumerate(path_to_models):
            print("model_path: ", model_path)
            print
            agent = load_model(model_path, env, position, device)
            agents.append(agent)
        env.set_agents(agents)

        rewards = tournament(env, num_games)
        for position, reward in enumerate(rewards):
            print(position, path_to_models[position], reward)

        for i in range(len(rewards)):
            iterations_rewards[i]+= rewards[i]


    # average_rewards = sum(iterations_rewards) / len(iterations_rewards)

    average_rewards = [reward/ num_iterations for reward in iterations_rewards]

    for i in range(len(path_to_models)):
        all_rewards.append(
            {
                'model': path_to_models[i],
                'avg_reward': average_rewards[i]
            }
        )

    with open(path, 'w') as f:
        json.dump(all_rewards, f, indent=4)


if __name__ == '__main__':
    models1= [
        "final_models/dqn_cego_player_0/checkpoint_5/model.pth",
        "random",
        "random",
        "random",
    ]
    compare_model_in_tournament("final_models/dqn_t_result.json", models1)
    models2= [
        "final_models/nfsp_cego_player_0/checkpoint_4/model.pth",
        "random",
        "random",
        "random",
    ]
    compare_model_in_tournament("final_models/nfsp_t_result.json", models2)
    models3= [
        "final_models/dqn_cego_player_0/checkpoint_5/model.pth",
        "final_models/nfsp_cego_player_0/checkpoint_4/model.pth",
        "random",
        "random",
    ]
    compare_model_in_tournament("final_models/dqn_vs_nfsp_t_result.json", models3)
    models4= [
        "final_models/nfsp_cego_player_0/checkpoint_4/model.pth",
        "final_models/dqn_cego_player_0/checkpoint_5/model.pth",
        "random",
        "random",
    ]
    compare_model_in_tournament("final_models/nfsp_vs_dqn_t_result.json", models4)
