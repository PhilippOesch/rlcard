import os

import torch

import rlcard
from rlcard.agents import NFSPAgent
from rlcard.agents.random_agent import RandomAgent

from rlcard.utils import (
    tournament,
    reorganize,
    Logger,
    plot_curve,
    get_device,
    set_seed,
)  # import some useful functions

args = {
    "_log_dir": "experiments/cego_nfsp_result_test/",
    "_env_name": "cego",
    "_seed": 10,
    "_hidden_layers_sizes": [64, 64],
    "_q_mlp_layer": [64, 64],
    "_num_eval_games": 10000,
    "_num_episodes": 1000,
    "_evaluate_every": 100
}


def train(_log_dir, _env_name, _seed, _hidden_layers_sizes,
          _q_mlp_layer, _num_eval_games=10000, _num_episodes=1000,
          _evaluate_every=100):
    pass

    # Check whether gpu is available
    device = get_device()

    set_seed(_seed)

    # Make the environment with seed
    env = rlcard.make(
        _env_name,
        config={
            'seed': _seed,
        }
    )

    agents = []

    for i in range(env.num_players):
        agents.append(NFSPAgent(
            num_actions=env.num_actions,
            state_shape=env.state_shape[0],
            hidden_layers_sizes=_hidden_layers_sizes,
            q_mlp_layers=_q_mlp_layer,
            device=device,
        ))

    env.set_agents(agents)

    # Start training
    with Logger(_log_dir) as logger:
        for episode in range(_num_episodes):

            for i in range(len(agents)):
                agents[i].sample_episode_policy()

            # Generate data from the environment
            trajectories, payoffs = env.run(is_training=True)

            # Reorganaize the data to be state, action, reward, next_state, done
            trajectories = reorganize(trajectories, payoffs)

            # Feed transitions into agents memories, and train the agent
            for i in range(len(trajectories)):
                for ts in trajectories[i]:
                    agents[i].feed(ts)

            # Evaluate the performance.
            if episode % _evaluate_every == 0:
                logger.log_performance(
                    env.timestep,
                    tournament(
                        env,
                        _num_eval_games,
                    )[0]
                )

            # Get the paths
        csv_path, fig_path = logger.csv_path, logger.fig_path

    # Plot the learning curve
    plot_curve(csv_path, fig_path, "DQN")

    # Save models
    for i in range(env.num_players):
        save_path = os.path.join(_log_dir, 'model' + str(i) + '.pth')
        torch.save(agents[i], save_path)
        print('Model saved in', save_path)


if __name__ == "__main__":
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    train(**args)
