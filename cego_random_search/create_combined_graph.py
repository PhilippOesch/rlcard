import json
import os
import csv
import matplotlib.pyplot as plt
from scipy import stats
import torch
import ntpath

import rlcard

from rlcard.games.cego.utils import load_model

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


def create_combined_graph(path_to_models, data_per_graph=10):
    model_dirs = [x[0] for x in os.walk(path_to_models)]

    ys = []
    xs = []

    i = 0

    fig, ax = plt.subplots()
    for model_dir in model_dirs:
        if not os.path.exists(model_dir + '/performance.csv'):
            continue

        i += 1
        ys.append([])
        xs.append([])

        file = open(model_dir + '/performance.csv')

        csvreader = csv.DictReader(file)
        for row in csvreader:
            ys[(i-1) % data_per_graph].append(int(row['timestep']))
            xs[(i-1) % data_per_graph].append(float(row['reward']))

        if i % data_per_graph == 0:
            fig, ax = plt.subplots()
        ax.set(xlabel='timestep', ylabel='reward')
        for idx in range(len(ys)):
            ax.plot(ys[idx], xs[idx], label="model_" +
                    str(idx + i-5), linewidth=2)
        ax.legend()
        ax.grid()

        if i % data_per_graph == 0:
            fig.savefig(path_to_models + '/fig' +
                        str(i//data_per_graph) + '.png', dpi=200)
            ys = []
            xs = []


def compare_model_in_tournament(path_to_models):
    model_dirs = [x[0] for x in os.walk(path_to_models)]

    i = 0

    all_rewards = []

    for model_dir in model_dirs:

        if not os.path.exists(model_dir + '/model.pth'):
            continue

        # Check whether gpu is available
        # device = get_device()
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

    # all_rewards.sort(key= lambda x: x['avg_reward'], reverse= True);

    # with open(path_to_models+'/tournament_result.json', 'w') as f:
    #     json.dump(all_rewards, f, indent=4)

    sort_by_key_and_save_array(
        all_rewards, 'avg_reward', path_to_models+'/tournament_result.json', True)


def read_performance(model_dir, max=79, min=0):
    if not os.path.exists(model_dir + '/performance.csv'):
        return None, None, None, None

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

    slope, intercept, r, p, std_err = stats.linregress(x, y)

    return slope, intercept, y, x


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

    if not os.path.exists(path_to_models + '/lin_reg_graphs/'):
        os.mkdir(path_to_models + '/lin_reg_graphs/')

    for model_dir in model_dirs:
        slope, intercept, y, x = read_performance(
            model_dir, max_value, min_value)
        if x is None:
            continue

        dir_name = path_leaf(model_dir)[1]

        slopes.append({
            'model': model_dir,
            'slope': slope,
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
        slopes, 'slope', path_to_models+'/lin_reg_slope_result_sorted.json', True)


def sort_by_key_and_save_array(array, key, path, descending=True):
    array.sort(key=lambda x: x[key], reverse=descending)

    with open(path, 'w') as f:
        json.dump(array, f, indent=4)


def get_total_ranking(save_folder, paths_to_models):
    array_rewards = []
    array_slopes = []

    slope_rankings = {}
    reward_rankings = {}
    total_ranks = []

    # print(paths_to_models)

    for path in paths_to_models:
        file = open(path + "/tournament_result.json")

        array_rewards.extend(json.load(file))

        otherfile = open(path + "/lin_reg_slope_result_sorted.json")

        array_slopes.extend(json.load(otherfile))

    array_rewards.sort(key=lambda x: x["avg_reward"], reverse=True)
    array_slopes.sort(key=lambda x: x["slope"], reverse=True)

    # for i in range(len(array_rewards)):
    #     array_rewards[i]["rank"]= i+1

    # print(array_rewards)

    # for i in range(len(array_slopes)):
    #     array_slopes[i]["rank"]= i+1

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
        # print("Current_Model:", model)
        print(model)
        # print(slope_rankings[model]['rank'])
        print(reward_rankings[model]['rank'])
        print(slope_rankings[model]['rank'])
        total_ranks.append({
            "model": model,
            "rank": (reward_rankings[model]['rank']*0.5)+(slope_rankings[model]['rank']*0.5),
            "avg_reward": reward_rankings[model]['avg_reward'],
            "slope": slope_rankings[model]['slope']*100000,
        })

    sort_by_key_and_save_array(
        total_ranks, 'rank', save_folder+'/total_ranking.json', False)


if __name__ == '__main__':
    # compare_training_slope('random_search_results/nfsp_point_var_0_tuned_dqn_against_dqn', 79, 0)

    # compare_training_slope(
    #     'random_search_results/nfsp_point_var_0_tuned_dqn', 79, 0)
    # compare_training_slope(
    #     'random_search_results/nfsp_point_var_0_tuned_dqn_against_dqn_second_try', 79, 0)
    # nfsp_point_var_0_tuned_dqn_against_dqn
    # compare_training_slope('random_search_results/nfsp_point_var_0_tuned_dqn_against_dqn', 79, 0)

    compare_training_slope(
        "random_search_results/fix_random_search/dqn_point_var_1")
    compare_training_slope(
        "random_search_results/fix_random_search/nfsp_point_var_0")
    compare_training_slope(
        "random_search_results/fix_random_search/nfsp_point_var_1")
    # get_total_ranking("random_search_results/fix_random_search",
    #                   ["random_search_results/fix_random_search/dqn_point_var_0"])
