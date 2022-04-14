import os

import torch

import rlcard
from rlcard.agents import DQNAgent
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
    "_log_dir": "experiments/uno_dqn_result/",
    "_env_name": "uno",
    "_seed": 10,
    "_mlp_layer": [128, 128],
    "_num_eval_games": 10000,
    "_num_episodes": 1000,
}


def train(_log_dir, _env_name, _seed, _mlp_layer, _num_eval_games=10000, _num_episodes=1000):

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

    # # this is our DQN agent
    agent = DQNAgent(
        num_actions=env.num_actions,
        state_shape=env.state_shape[0],
        mlp_layers=_mlp_layer,
        device=device,
    )

    # because uno is a 2 player game we need a random agent as comparison
    random_agent = RandomAgent(num_actions=env.num_actions)

    agents = [agent, random_agent]

    env.set_agents(agents)

    with Logger(_log_dir) as logger:
        for episode in range(_num_episodes):

            # Generate data from the environment
            trajectories, payoffs = env.run(is_training=True)

            # Reorganaize the data to be state, action, reward, next_state, done
            trajectories = reorganize(trajectories, payoffs)

            # Feed transitions into agent memory, and train the agent
            for ts in trajectories[0]:
                agent.feed(ts)

            # Evaluate the performance.
            if episode % 50 == 0:
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

    # Save model
    save_path = os.path.join(_log_dir, 'model.pth')
    torch.save(agent, save_path)
    print('Model saved in', save_path)


if __name__ == "__main__":
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    train(**args)
