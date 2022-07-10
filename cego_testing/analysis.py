# random against human

import rlcard
from rlcard.agents import RandomAgent
from rlcard.agents.human_agents.cego_human_agent import HumanAgent

from rlcard.games.cego.utility.game import load_model, ACTION_SPACE, cards2list
import os
import json
import matplotlib.pyplot as plt

from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
)

num_games = 1000000

env = rlcard.make(
    'cego',
    config={
        'seed': 20,
        'game_variant': 'standard',
        'game_activate_heuristic': False,
        'game_judge_by_points': 0,
        'game_train_players': [False, False, False, False],
        'game_analysis_mode': True
    })

device = get_device()

agents = [RandomAgent(env.num_actions) for _ in range(env.num_players)]

env.set_agents(
    [RandomAgent(env.num_actions) for _ in range(env.num_players)]
)


def analyse_card_trick_win_propabilities(path, env):
    '''
        if a trick was won who big is the chance that this card was the winner
    '''
    trick_wins: dict = {}

    for key in ACTION_SPACE:
        trick_wins[key] = 0

    num_trick_wins = 0
    for i in range(num_games):
        print("episode:", i)
        trajectories, payoffs, state = env.run(is_training=False)
        for card in cards2list(state['winning_card_history']):
            trick_wins[card] += 1
            num_trick_wins += 1

    for entry in trick_wins:
        trick_wins[entry] /= (num_games*11)

    sorted_by_prob = {k: v for k, v in sorted(
        trick_wins.items(), key=lambda item: item[1], reverse=True)}
    print(sorted_by_prob)

    for key in sorted_by_prob:
        sorted_by_prob[key] = round((sorted_by_prob[key]*100), 2)

    with open(path, 'w') as f:
        json.dump(sorted_by_prob, f, indent=4)


def analyse_propability_a_card_wins_a_trick(path, env):
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


def analyse_first_mover_advantage(path):
    player_avg_pos_wins: list = [0, 0, 0, 0]

    relative_vals_over_games = [[], [], [], []]
    total_vals_over_games = [0, 0, 0, 0]
    timesteps = []

    for i in range(num_games):
        print("episode:", i)
        timesteps.append(((i+1)*11))
        trajectories, payoffs, state = env.run(is_training=False)
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
            timesteps, relative_vals_over_games[i], label="player_"+str(i+1))
    ax.legend()
    ax.grid()
    fig.savefig(path + "/first_players_advantage.png")

    result = {}

    for i in range(4):
        result['player_'+str(i)] = (total_vals_over_games[i] /
                                    (num_games*11))*100

    result = {k: v for k, v in sorted(
        result.items(), key=lambda item: item[1], reverse=True)}

    with open(path + "/first_players_advantage_result.json", 'w') as f:
        json.dump(result, f, indent=4)


if __name__ == '__main__':
    analyse_first_mover_advantage(
        "analysis_results", env)
