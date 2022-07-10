import matplotlib.pyplot as plt
import csv
import os
import json

from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
)


def load_model(model_path, env=None, position=None, device=None):
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
    try:
        float(num)
        return True
    except ValueError:
        return False


def create_cego_dmc_graph(model_path) -> None:
    '''
    Creates a training graph for a dmc_model
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

    fig.savefig(model_path + '/fig.png')


def create_combined_graph(path_to_models, data_per_graph=10):
    '''
    Combines model graphs of specified path into one graph
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

        if i % data_per_graph == 0:
            fig.savefig(path_to_models + '/fig' +
                        str(i//data_per_graph) + '.png', dpi=200)
            ys = []
            xs = []


def play_tournament_and_update_rewards(rewards, env, path_to_models, num_games, device, seed=None):
    if seed != None:
        set_seed(seed)
        env.seed(seed)

    agents = []
    for position, model_path in enumerate(path_to_models):
        agent = load_model(model_path, env, position, device)
        agents.append(agent)
    env.set_agents(agents)

    tournament_reward = tournament(env, num_games)
    for position, rew in enumerate(tournament_reward):
        print(position, path_to_models[position], rew)

    for i in range(len(rewards)):
        rewards[i] += tournament_reward[i]


def compare_models_in_tournament(save_path, env, num_games, path_to_models, seeds=None) -> None:

    device = get_device()

    all_rewards: list = []

    iterations_rewards = [0 for _ in range(len(path_to_models))]
    num_iterations = len(seeds) if seeds != None else 1

    if seeds == None:
        play_tournament_and_update_rewards(iterations_rewards, env, path_to_models,
                                           num_games, device)
    else:
        for seed in seeds:
            play_tournament_and_update_rewards(iterations_rewards, env, path_to_models,
                                               num_games, device, seed)

    average_rewards = [
        reward / num_iterations for reward in iterations_rewards]

    for i in range(len(path_to_models)):
        all_rewards.append(
            {
                'model': path_to_models[i],
                'avg_reward': average_rewards[i]
            }
        )

    with open(save_path, 'w') as f:
        json.dump(all_rewards, f, indent=4)
