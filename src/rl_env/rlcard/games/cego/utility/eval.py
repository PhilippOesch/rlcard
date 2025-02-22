import matplotlib.pyplot as plt
import csv
import os
import json
import rlcard
import ntpath
import numpy as np
from scipy import stats
import seaborn as sns
import re
from rlcard.games.cego.utility.game import ACTION_SPACE, cards2list

from rlcard.utils import (
    get_device,
    set_seed,
)

ROUND_NUM = 11


def load_model(model_path, env=None, position=None, device=None) -> object:
    '''
        load model as agent

    Input:
        model_path (str): path to model
        env (Env): the environment object
        position (int): the position of the agent
        device (object): the device to run the agent

    Output:
        model (object)
    '''
    agent = None
    if os.path.isfile(model_path):  # Torch model
        import torch
        agent = torch.load(model_path, map_location=device)
        agent.set_device(device)
    elif model_path == 'random':  # Random model
        from rlcard.agents import RandomAgent
        agent = RandomAgent(num_actions=env.num_actions)
    print("loaded model: {}".format(model_path))

    return agent


def isfloat(num) -> bool:
    '''
        helper function that finds out wheather the object is a float

    Input: 
        num (Any): potential number
    '''
    try:
        float(num)
        return True
    except ValueError:
        return False


def create_cego_dmc_graph(model_path) -> None:
    '''
        Creates a training graph from the dmc-model logs
    '''
    file = open(model_path + '/dmc/logs.csv')

    csvreader = csv.DictReader(file)

    y = []
    x_cego = []
    x_other = []
    tick = 0

    for row in csvreader:
        if isfloat(row['mean_episode_return_1']):
            x_cego.append(float(row['mean_episode_return_0']))
            y.append(tick)
            tick += 1
        if isfloat(row['mean_episode_return_1']):
            x_other.append(float(row['mean_episode_return_1']))

    fig, ax = plt.subplots()
    ax.plot(y, x_cego, label='Cego Player')
    ax.plot(y, x_other, label='Other Players')
    ax.set(xlabel='Tick', ylabel='reward')
    ax.legend()
    ax.grid()

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    fig.savefig(model_path + '/fig.png')


def create_combined_graph(path_to_models, data_per_graph=10) -> None:
    '''
        Combines model graphs of specified path into one graph

    Input:
        path_to_models: array of model paths
        data_per_graph: how many models to display in one. Otherwise
            the graphs are split
    '''
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

        os.makedirs(os.path.dirname(path_to_models), exist_ok=True)
        if i % data_per_graph == 0:
            fig.savefig(path_to_models + '/fig' +
                        str(i//data_per_graph) + '.png', dpi=200)
            ys = []
            xs = []


def play_tournament_and_update_rewards(rewards, game_Settings, path_to_models, num_games, seed=None, i=None) -> None:
    '''
    gets a reward array, play a tournament and updated the reward array

    Params:
        rewards (list): Current rewards,
        game_Settings (dict): Dictionary of the game settings
        path_to_models (list): Paths to Models
        num_games (int): Number of Games
        seed (int): The random seed
    '''

    device = get_device()

    env = rlcard.make(
        game_Settings["env_name"],
        config={
            'game_variant': game_Settings["game_variant"],
            'game_judge_by_points': game_Settings["game_judge_by_points"],
            'game_activate_heuristic': game_Settings["game_activate_heuristic"],
            'game_train_env': game_Settings['game_train_env']
        }
    )

    if seed != None:
        set_seed(seed)
        env.seed(seed)

    agents = convert_to_agents(path_to_models, env, device)
    env.set_agents(agents)

    tournament_reward = tournament(env, num_games, episode=i)
    for position, rew in enumerate(tournament_reward):
        print(position, path_to_models[position], rew)

    for i in range(len(rewards)):
        rewards[i] += tournament_reward[i]


def tournament(env, num, debug=True, episode=None) -> list[int]:
    ''' 
        Evaluate the performance of the agents in the environment.
        This function is copied form rlcard.utils.utils and changed to allow debugging outputs.

    Args:
        env (Env class): The environment to be evaluated.
        num (int): The number of games to play.

    Returns:
        A list of average payoffs for each player
    '''
    payoffs = [0 for _ in range(env.num_players)]
    counter = 0
    while counter < num:
        if debug:
            print('episode:', episode, 'game num:', counter)
        _, _payoffs = env.run(is_training=False)
        if isinstance(_payoffs, list):
            for _p in _payoffs:
                for i, _ in enumerate(payoffs):
                    payoffs[i] += _p[i]
                counter += 1
        else:
            for i, _ in enumerate(payoffs):
                payoffs[i] += _payoffs[i]
            counter += 1
    for i, _ in enumerate(payoffs):
        payoffs[i] /= counter
    return payoffs


def convert_to_agents(path_to_models, env, device) -> list[object]:
    '''
        convert a list of model paths into a list of agents
    '''
    agents = []
    for position, model_path in enumerate(path_to_models):
        agent = load_model(model_path, env, position, device)
        agents.append(agent)
    return agents


def tournament_appg_and_wp_cego(save_path, games_settings, num_games, path_to_models, seeds=None) -> None:
    '''
        a tournament, but both APPG and WP are calculated
    '''

    device = get_device()

    won_games = [0, 0, 0, 0]
    won_points = [0, 0, 0, 0]

    result = {}

    for seed in seeds:
        set_seed(seed)

        # for each seed, a new environment is created
        env = rlcard.make(
            games_settings["env_name"],
            config={
                'seed': seed,
                'game_variant': games_settings["game_variant"],
                'game_judge_by_points': games_settings["game_judge_by_points"],
                'game_activate_heuristic': games_settings["game_activate_heuristic"],
                'game_train_env': games_settings['game_train_env']
            }
        )

        agents = convert_to_agents(path_to_models, env, device)
        env.set_agents(agents)

        for game in range(num_games):
            print("Game:", game)
            _, payoffs = env.run(is_training=False)

            for i in range(len(payoffs)):
                won_points[i] += payoffs[i]

            if payoffs[0] > payoffs[1]:
                won_games[0] += 1
            else:
                for i in range(1, len(payoffs)):
                    won_games[i] += 1

    # save in file
    for i in range(len(path_to_models)):
        result[str(i)+"_"+path_to_models[i]] = {
            'appg': won_points[i] / (num_games * len(seeds)),
            'wp': won_games[i] / (num_games * len(seeds))
        }

    with open(save_path, 'w') as f:
        json.dump(result, f, indent=4)


def compare_models_in_tournament(save_path, games_settings, num_games, path_to_models, seeds=None) -> None:
    '''
        function to compare models in a tournament

    Input:
        save_path (str): Path of where to save the results in json format
        game_settings (dict): a dictionary of the env settings
        num_games (int): the number of games to play for each random seed
        path_to_models (list[str]): a list of the model paths to compare
        seeds: (list[int]) a list of random seeds
    '''
    all_rewards: list = []

    iterations_rewards = [0 for _ in range(len(path_to_models))]
    num_iterations = len(seeds) if seeds != None else 1

    if seeds == None:
        print("Tournament: ", 0)
        print("--------------------------------")
        play_tournament_and_update_rewards(iterations_rewards, games_settings, path_to_models,
                                           num_games, i=0)
    else:
        for i in range(len(seeds)):
            print("Tournament: ", i)
            print("--------------------------------")
            play_tournament_and_update_rewards(iterations_rewards, games_settings, path_to_models,
                                               num_games, seeds[i], i=i)

    average_rewards = [
        reward / num_iterations for reward in iterations_rewards]

    for i in range(len(path_to_models)):
        all_rewards.append(
            {
                'model': path_to_models[i],
                'avg_reward': average_rewards[i]
            }
        )

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'w') as f:
        json.dump(all_rewards, f, indent=4)


def analyze_first_mover_advantage(path, env, num_games) -> None:
    '''
        This function analyzes whether the player who plays 
            the first card in the trick has an advantage over other players.
    '''

    relative_vals_over_games = [[], [], [], []]
    total_vals_over_games = [0, 0, 0, 0]
    timesteps = []

    for i in range(num_games):
        print("episode:", i)
        timesteps.append(((i+1)*ROUND_NUM))
        _, _, state = env.run(is_training=False)

        for j in range(len(state['winning_player_history'])):
            starter_id = state['start_player_history'][j]
            winner_id = state['winning_player_history'][j]

            relative_winner_id = (winner_id-starter_id) % 4
            total_vals_over_games[relative_winner_id] += 1

        for j in range(4):
            new_avg = total_vals_over_games[j]/((i+1)*ROUND_NUM)
            relative_vals_over_games[j].append(new_avg)

    fig, ax = plt.subplots()
    ax.set(xlabel='games', ylabel='reward')

    for i in range(4):
        ax.plot(
            timesteps, relative_vals_over_games[i], label="player_"+str(i))
    ax.legend()
    ax.grid()
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path + "/first_players_advantage_test.png")

    result = {}

    for i in range(4):
        result['player_'+str(i)] = (total_vals_over_games[i] /
                                    (num_games*ROUND_NUM))*100

    result = {k: v for k, v in sorted(
        result.items(), key=lambda item: item[1], reverse=True)}

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + "/first_players_advantage_result_test.json", 'w') as f:
        json.dump(result, f, indent=4)


def analyze_probability_a_card_wins_a_trick(path, env, num_games) -> None:
    '''
        Approximate the probability that a card won a trick when played.
            P(W_i| CP_i)
    '''
    trick_wins: dict = {}

    for key in ACTION_SPACE:
        trick_wins[key] = {
            'played': 0,
            'won': 0
        }

    for i in range(num_games):
        print("episode:", i)
        _, _, state = env.run(is_training=False)
        for trick in state['played_tricks']:
            for card in trick:
                trick_wins[str(card)]['played'] += 1

        for card in cards2list(state['winning_card_history']):
            trick_wins[card]['won'] += 1

    result: dict = {}

    for card in trick_wins:
        result[card] = trick_wins[card]['won'] / trick_wins[card]['played']

    sorted_by_prob = {k: v for k, v in sorted(
        result.items(), key=lambda item: item[1], reverse=True)}

    for key in sorted_by_prob:
        sorted_by_prob[key] = round((sorted_by_prob[key]*100), 2)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(sorted_by_prob, f, indent=4)


def analyze_card_trick_win_probabilities(path, env, num_games) -> None:
    '''
        Approximate the probability that a card won a trick
            P(W_i)
    '''
    trick_wins: dict = {}

    for key in ACTION_SPACE:
        trick_wins[key] = 0

    num_trick_wins = 0
    for i in range(num_games):
        print("episode:", i)
        _, _, state = env.run(is_training=False)
        for card in cards2list(state['winning_card_history']):
            trick_wins[card] += 1
            num_trick_wins += 1

    for entry in trick_wins:
        trick_wins[entry] /= (num_games*ROUND_NUM)

    sorted_by_prob = {k: v for k, v in sorted(
        trick_wins.items(), key=lambda item: item[1], reverse=True)}

    for key in sorted_by_prob:
        sorted_by_prob[key] = round((sorted_by_prob[key]*100), 2)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(sorted_by_prob, f, indent=4)


def compare_randsearch_models_in_tournament(path_to_models, filename, seeds, env_params, num_games) -> None:
    '''
        Comparison and ranking of random search models.

    Input:
        path_to_models (list): paths to models
        filename (str): Name of the result-file
        seeds (list): random Seeds to test for each run
        env_params (dict): Params of Environment,
        num_games (int): Number of games to play for each random seed


    env_params:
        env_name (str): Environment Name
        game_variant (str): Name of the Sub game
        game_judge_by_points (int): Way to judge the points by
        game_activate_heuristic (bool): Use Heuristic for game environments
    '''
    import torch

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
                env_params['env_name'],
                config={
                    'seed': seed,
                    'game_variant': env_params['game_variant'],
                    'game_judge_by_points': env_params['game_judge_by_points'],
                    'game_activate_heuristic': env_params['game_activate_heuristic']
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
        all_rewards, 'avg_reward', path_to_models+'/' + filename, True)


def sort_by_key_and_save_array(array, key, path, descending=True) -> None:
    '''
        helper function for sorting and saving arrays
    '''
    array.sort(key=lambda x: x[key], reverse=descending)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(array, f, indent=4)


def get_total_ranking(save_folder, paths_to_models, filename="total_ranking.json") -> None:
    '''
        compare rank of slopes and rewards and create a total ranking

    Input: 
        save_folder (str): folder to save the file
        paths_to_models (list[str]): list of model paths to rank
        filename (str): the filename to save
    '''

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


def read_performance(model_dir, max=79, min=0) -> tuple[object, object, object, object, object]:
    '''
        read the csv_performance file and perform a linear regression

    Input:
        model_dir (str): directory of the model
        max (int): max value for normalization of rewards
        min (int): min value for normalization of rewards
    '''

    # early return when not defined
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


def get_ys(x, slope, intercept) -> list:
    '''
        get y values for linear regression straight line to visualize
    '''
    ys = []
    for x_i in x:
        ys.append(slope*x_i+intercept)

    return ys


def path_leaf(path) -> object:
    '''
        helper function to get folder structure
    '''
    return ntpath.split(path)


def compare_training_slope(path_to_models, max_value=79, min_value=0) -> None:
    '''
        create slope ranking

    Input:
        model_dir (str): directory of the model
        max (int): max value for normalization of rewards
        min (int): min value for normalization of rewards
    '''

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

        os.makedirs(os.path.dirname(path_to_models), exist_ok=True)
        fig.savefig(path_to_models + '/lin_reg_graphs/lin_reg_' +
                    dir_name + '.png', dpi=200)

    sort_by_key_and_save_array(
        stds, 'std', path_to_models+'/std_result_sorted.json', False)

    sort_by_key_and_save_array(
        slopes, 'slope', path_to_models+'/lin_reg_slope_result_sorted.json', True)


def analyze_card_round_position(game_Setting, title, paths_to_models,  save_path, num_games, player_id, seed) -> None:
    '''
        analyze the position of in what round specific cards are played for a player.
        This function visualizes this in a heat map

    Input:
        game_Setting (dict): Environment settings
        title (str): The title of the heatmap that is created
        paths_to_models (list): environment models
        path (str): path to save the heatmap to
        num_games (int): number of games to play
        player_id (int): id of the player to observe
        seed (int): random seed
    '''

    device = get_device()

    env = rlcard.make(
        game_Setting['env_name'],
        config={
            'seed': seed,
            'game_variant': game_Setting['game_variant'],
            'game_activate_heuristic': game_Setting['game_activate_heuristic'],
            'game_judge_by_points': game_Setting['game_judge_by_points'],
            'game_train_players': game_Setting['game_train_env'],
            'game_analysis_mode': True
        }
    )
    agents = convert_to_agents(paths_to_models, env, device)
    env.set_agents(agents)

    card_nums = {}
    heatmap: dict = {}
    for key in ACTION_SPACE:
        heatmap[key] = [0] * ROUND_NUM
        card_nums[key] = 0

    for i in range(num_games):
        print("episode:", i)
        trajectories, _, _ = env.run(is_training=False)
        actions = [entry[1] for entry in trajectories[0]
                   [-1]['action_record'] if entry[0] == player_id]

        for i in range(len(actions)):
            heatmap[actions[i]][i] += 1
            card_nums[actions[i]] += 1

    for key in card_nums:
        if card_nums[key] != 0:
            for i in range(len(heatmap[key])):
                if heatmap[key][i] != 0:
                    heatmap[key][i] = heatmap[key][i] / card_nums[key]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_title(title, fontsize=16)
    sns.heatmap(list(heatmap.values()), fmt="d")
    ax.set_xlabel('Round', fontsize=14)
    ax.set_ylabel('Card', fontsize=14)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=200)


def sorted_alphanumeric(data) -> object:
    '''
        helper function to sort files in a natural way
    '''
    def convert(text): return int(text) if text.isdigit() else text.lower()
    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


def compare_dmc_checkpoints(game_settings, path_to_dmc_models, save_path, is_ai_array, num_games, seed) -> None:
    '''
        this function serves to observe the checkpoints of a DMC model and compare each player for each checkpoint with another

    Input:
        game_settings (dict): environment settings
        path_to_dmc_models (str): the path to the checkpoint models
        file_name (str): Path to save the results to
        is_ai_array (list[bool]): list of length= 4; True = load model, False = load random agent
        num_games (int): number of checkpoint comparison games
        seed (int): random seed
    '''
    files = [f for f in sorted_alphanumeric(os.listdir(
        path_to_dmc_models)) if os.path.isfile(os.path.join(path_to_dmc_models, f))]

    reward_results = []
    checkpoint_files = []

    device = get_device()

    env = rlcard.make(
        game_settings['env_name'],
        config={
            'seed': seed,
            'game_variant': game_settings['game_variant'],
            'game_judge_by_points': game_settings['game_judge_by_points'],
            'game_activate_heuristic': game_settings['game_activate_heuristic']
        }
    )

    file_list = [[], [], [], []]

    for file in files:
        if(file.startswith("0_")):
            file_list[0].append(file)
        if(file.startswith("1_")):
            file_list[1].append(file)
        if(file.startswith("2_")):
            file_list[2].append(file)
        if(file.startswith("3_")):
            file_list[3].append(file)

    for i in range(len(file_list[0])):
        agents = []

        checkpoint_files.append(i)

        for y in range(4):
            if is_ai_array[y]:
                agents.append(load_model(path_to_dmc_models +
                              file_list[y][i], env, y, device))
            else:
                agents.append(load_model("random", env, y, device))
        env.set_agents(agents)
        reward = tournament(env, num_games, debug=False)
        reward_results.append(":".join([str(reward[0]), str(reward[1])]))

    with open(path_to_dmc_models + '/' +
              save_path, 'w', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(['checkpoint', 'reward'])
        writer.writerows(zip(checkpoint_files, reward_results))


def plot_curve(csv_path, save_path, name="") -> None:
    ''' 
        Read data from csv file and plot the results
    '''
    with open(csv_path) as csvfile:
        reader = csv.DictReader(csvfile)
        xs = []
        p0 = []
        p1 = []
        for row in reader:
            xs.append(int(row['timestep']))
            rewards = row['reward'].split(":")
            p0.append(float(rewards[0]))
            p1.append(float(rewards[1]))
        fig, ax = plt.subplots()
        ax.set_title(name)
        ax.plot(xs, p0, label="single_player")
        ax.plot(xs, p1, label="other_players")
        ax.set(xlabel='timestep', ylabel='reward')
        ax.legend()
        ax.grid()

        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path)


def create_bar_graph(path, save_path) -> None:
    '''
        helper function to create bar graph
    '''
    x = []
    y = []

    with open(path, 'r') as json_file:
        data = json.load(json_file)

    result = 0
    i = 0
    for key in data:
        x.append(i)
        y.append(data[key])
        i += 1

    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.set(xlabel='card', ylabel='WP')

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig.savefig(save_path)


def create_bar_graph_colored(path, save_path, highcards_percentage=80, is_card_relative=False) -> None:
    '''
        helper function to create colored bar graph with high/ low card split

    Input
        path (str): path to card probabilities
        save_path (str): path to save the bar graph
        highcards_percentage (float): high card split in %
        is_card_relative (bool): relative to card play frequency?
    '''
    x = []
    y = []

    with open(path, 'r') as json_file:
        data = json.load(json_file)

    result = 0
    i = 0

    low_cards = []
    high_cards = []
    colors = []
    for key in data:
        if result >= highcards_percentage:
            low_cards.append(i)
            colors.append('tab:blue')
        else:
            high_cards.append(i)
            colors.append('mediumvioletred')
        if is_card_relative:
            result += (data[key]*(44/54))/11
        else:
            result += data[key]
        x.append(i)
        y.append(data[key])
        i += 1

    fig, ax = plt.subplots()
    ax.bar(x, y, color=colors)
    ax.set(xlabel='card', ylabel='WP')

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig.savefig(save_path)


def split_80_20_cards(path, save_path, highcards_percentage=80, is_card_relative=False) -> None:
    '''
        split cards into high and low cards

    Input:
        path (str): path to card win probabilities
        save_path (str): path to save the results to
        highcards_percentage (float): percentage that account for total high card win probabilites
        is_card_relative: relative to card frequency?
    '''

    with open(path, 'r') as json_file:
        data = json.load(json_file)

    high_cards = {}
    low_cards = {}
    result = 0
    high_result = 0

    sort_orders = sorted(data.items(), key=lambda x: x[1], reverse=False)

    for i in sort_orders:
        if is_card_relative:
            result += (i[1]*(44/54))/11
        else:
            result += i[1]

        if result > (100-highcards_percentage):
            high_cards[i[0]] = i[1]
            if is_card_relative:
                high_result += (i[1]*(44/54))/11
            else:
                high_result += i[1]
        else:
            low_cards[i[0]] = i[1]

    print(len(low_cards))
    print("low cards", low_cards)
    print("low_cards_sum:", high_result)
    print("-------------------------")
    print(len(high_cards))
    print("high cards", high_cards)
    print("hight_cards_sum:", (result - high_result))

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path + "/low_cards.json", 'w') as f:
        json.dump(low_cards, f, indent=4)

    with open(save_path + "/high_cards.json", 'w') as f:
        json.dump(high_cards, f, indent=4)


def plot_combined(csv_dict, save_path, x_name, y_name, name="") -> None:
    """
        helper function for combining result in graph

        csv_dict= [
            {
                'path': '...',
                'team': 0 or 1,
                'name': '...'
            },
            ...
        ]
    """
    ys = [[] for _ in range(len(csv_dict))]
    x = []

    for i in range(len(csv_dict)):
        with open(csv_dict[i]['path']) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
                if i == 0:
                    x.append(int(row[x_name]))

                rewards = row[y_name].split(":")
                ys[i].append(float(rewards[csv_dict[i]['team']]))

    fig, ax = plt.subplots()
    ax.set_title(name)

    for i in range(len(csv_dict)):
        ax.plot(x, ys[i], label=csv_dict[i]['name'])
    ax.set(xlabel=x_name, ylabel=y_name)
    ax.legend()
    ax.grid()

    save_dir = os.path.dirname(save_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig.savefig(save_path)


def refactor_training_graph(csv_path, name, y_name, x_name, title, save_path, num_checkpoints) -> None:
    '''
        helper function to refactor training graphs
    '''

    xs = []
    ys = []

    with open(csv_path) as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            if i == num_checkpoints:
                break

            xs.append(int(row['timestep']))
            ys.append(float(row['reward']))
            i += 1

    fig, ax = plt.subplots()
    ax.set_title(name)
    ax.plot(xs, ys, label=name)
    ax.set(xlabel=x_name, ylabel=y_name)
    ax.legend()
    ax.grid()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig.savefig(save_path)
