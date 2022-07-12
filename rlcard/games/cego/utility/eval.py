import matplotlib.pyplot as plt
import csv
import os
import json

from rlcard.games.cego.utility.game import ACTION_SPACE, cards2list

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


def analyse_first_mover_advantage(path, env, num_games):
    relative_vals_over_games = [[], [], [], []]
    total_vals_over_games = [0, 0, 0, 0]
    timesteps = []

    for i in range(num_games):
        print("episode:", i)
        timesteps.append(((i+1)*11))
        _, _, state = env.run(is_training=False)

        for j in range(len(state['winning_player_history'])):
            starter_id = state['start_player_history'][j]
            winner_id = state['winning_player_history'][j]

            relative_winner_id = (winner_id-starter_id) % 4
            total_vals_over_games[relative_winner_id] += 1

        for j in range(4):
            new_avg = total_vals_over_games[j]/((i+1)*11)
            relative_vals_over_games[j].append(new_avg)

    fig, ax = plt.subplots()
    ax.set(xlabel='games', ylabel='reward')

    for i in range(4):
        ax.plot(
            timesteps, relative_vals_over_games[i], label="player_"+str(i))
    ax.legend()
    ax.grid()
    fig.savefig(path + "/first_players_advantage_test.png")

    result = {}

    for i in range(4):
        result['player_'+str(i)] = (total_vals_over_games[i] /
                                    (num_games*11))*100

    result = {k: v for k, v in sorted(
        result.items(), key=lambda item: item[1], reverse=True)}

    with open(path + "/first_players_advantage_result_test.json", 'w') as f:
        json.dump(result, f, indent=4)


def analyse_propability_a_card_wins_a_trick(path, env, num_games):
    trick_wins: dict = {}

    for key in ACTION_SPACE:
        trick_wins[key] = {
            'played': 0,
            'won': 0
        }

    for i in range(num_games):
        print("episode:", i)
        trajectories, payoffs, state = env.run(is_training=False)
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

    with open(path, 'w') as f:
        json.dump(sorted_by_prob, f, indent=4)


def analyse_card_trick_win_propabilities(path, env, num_games):
    '''
        if a trick was won who big is the chance that this card was the winner
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
        trick_wins[entry] /= (num_games*11)

    sorted_by_prob = {k: v for k, v in sorted(
        trick_wins.items(), key=lambda item: item[1], reverse=True)}

    for key in sorted_by_prob:
        sorted_by_prob[key] = round((sorted_by_prob[key]*100), 2)

    with open(path, 'w') as f:
        json.dump(sorted_by_prob, f, indent=4)
