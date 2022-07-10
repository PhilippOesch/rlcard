import json
import os
import csv
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import torch
import ntpath

import rlcard

from rlcard.games.cego.utility.eval import load_model

from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
)

sub_path = 'random_search_results/'
path_to_models = sub_path+'/nfsp_point_var_0'

seeds = [12, 17, 20, 30, 33]
env_name = 'cego'
game_variant = 'standard'
game_judge_by_points = 0
game_activate_heuristic = True
num_games = 1000


def compare_model_in_tournament(path_to_models):
    model_dirs = [x[0] for x in os.walk(path_to_models)]

    i = 0

    all_rewards = []

    for model_dir in model_dirs:

        if not os.path.exists(model_dir + '/model.pth'):
            continue

        device = torch.device("cpu")

        iterations_rewards = []

        for seed in seeds:
            # Seed numpy, torch, random
            set_seed(seed)

            models = [model_dir + '/model.pth', 'random', 'random', 'random']

            env = rlcard.make(
                env_name,
                config={
                    'seed': seed,
                    'game_variant': game_variant,
                    'game_judge_by_points': game_judge_by_points,
                    'game_activate_heuristic': game_activate_heuristic
                }
            )

            agents = []
            for position, model_path in enumerate(models):
                agents.append(load_model(model_path, env, position, device))
            env.set_agents(agents)

            rewards = tournament(env, num_games)
            for position, reward in enumerate(rewards):
                print(position, models[position], reward)

            iterations_rewards.append(
                rewards[0]
            )

        average_rewards = sum(iterations_rewards) / len(iterations_rewards)

        all_rewards.append(
            {
                'model': model_dir,
                'avg_reward': average_rewards
            }
        )

    sort_by_key_and_save_array(
        all_rewards, 'avg_reward', path_to_models+'/tournament_result.json', True)


def read_performance(model_dir, max=79, min=0) -> tuple[object, object, object, object, object]:
    if not os.path.exists(model_dir + '/performance.csv'):
        return None, None, None, None, None

    file = open(model_dir + '/performance.csv')
    csvreader = csv.reader(file)
    header = next(csvreader)
    x = []
    y = []
    for row in csvreader:
        if(len(row) == 0):
            continue
        x.append(int(row[0]))
        y.append(float(row[1])/float(max+min))

    result = stats.linregress(x, y)
    std = np.std(y)

    return result.slope, result.intercept, std, y, x


def get_ys(x, slope, intercept):
    ys = []
    for x_i in x:
        ys.append(slope*x_i+intercept)

    return ys


def path_leaf(path):
    return ntpath.split(path)


def compare_training_slope(path_to_models, max_value=79, min_value=0):
    model_dirs = [x[0] for x in os.walk(path_to_models)]

    slopes = []
    stds = []

    if not os.path.exists(path_to_models + '/lin_reg_graphs/'):
        os.mkdir(path_to_models + '/lin_reg_graphs/')

    for model_dir in model_dirs:
        slope, intercept, std, y, x = read_performance(
            model_dir, max_value, min_value)
        if x is None:
            continue

        dir_name = path_leaf(model_dir)[1]

        slopes.append({
            'model': model_dir,
            'slope': slope,
        })

        stds.append({
            'model': model_dir,
            'std': std,
        })

        fig, ax = plt.subplots()
        ax.set(xlabel='timestep', ylabel='reward_normalized (max:1, min:0)')
        ax.plot(x, y, label=dir_name, linewidth=2)
        ax.plot(x, get_ys(x, slope, intercept),
                label="linear regression: "+dir_name, linewidth=2)
        ax.legend()
        ax.grid()
        fig.savefig(path_to_models + '/lin_reg_graphs/lin_reg_' +
                    dir_name + '.png', dpi=200)

    sort_by_key_and_save_array(
        stds, 'std', path_to_models+'/std_result_sorted.json', False)

    sort_by_key_and_save_array(
        slopes, 'slope', path_to_models+'/lin_reg_slope_result_sorted.json', True)


def sort_by_key_and_save_array(array, key, path, descending=True):
    array.sort(key=lambda x: x[key], reverse=descending)

    with open(path, 'w') as f:
        json.dump(array, f, indent=4)


def get_total_ranking(save_folder, paths_to_models, filename="total_ranking.json") -> None:
    array_rewards: list[dict] = []
    array_slopes: list[dict] = []

    slope_rankings: dict = {}
    reward_rankings: dict = {}
    total_ranks: list[dict] = []

    for path in paths_to_models:
        file = open(path + "/tournament_result.json")

        array_rewards.extend(json.load(file))

        otherfile = open(path + "/lin_reg_slope_result_sorted.json")

        array_slopes.extend(json.load(otherfile))

    array_rewards.sort(key=lambda x: x["avg_reward"], reverse=True)
    array_slopes.sort(key=lambda x: x["slope"], reverse=True)

    for idx, reward in enumerate(array_rewards):
        reward_rankings[reward['model']] = {
            'rank': idx+1,
            'avg_reward': reward['avg_reward'],
        }

    for idx, slope in enumerate(array_slopes):
        slope_rankings[slope['model']] = {
            'rank': idx+1,
            'slope': slope['slope'],
        }

    print(reward_rankings)

    for model in reward_rankings:
        total_ranks.append({
            "model": model,
            "rank": (reward_rankings[model]['rank']*0.5)+(slope_rankings[model]['rank']*0.5),
            "avg_reward": reward_rankings[model]['avg_reward'],
            "slope": slope_rankings[model]['slope']*100000,
        })

    sort_by_key_and_save_array(
        total_ranks, 'rank', save_folder+"/"+filename, False)


if __name__ == '__main__':
    get_total_ranking("random_search_results/fix_random_search",
                      ["random_search_results/fix_random_search/dqn_point_var_0",
                       "random_search_results/fix_random_search/dqn_point_var_1"],
                      "total_ranking_dqn.json")
    get_total_ranking("random_search_results/fix_random_search",
                      ["random_search_results/fix_random_search/nfsp_point_var_0",
                       "random_search_results/fix_random_search/nfsp_point_var_1"],
                      "total_ranking_nfsp.json")
