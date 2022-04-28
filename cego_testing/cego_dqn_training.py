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
    "_log_dir": "experiments/cego_dqn_result_player_2/",
    "_env_name": "cego",
    "_seed": 10,
    "_mlp_layer": [512, 512],
    "_num_eval_games": 10000,
    "_num_episodes": 10000,
    "_evaluate_every": 100
}


def train(_log_dir, _env_name, _seed, _mlp_layer, _num_eval_games=10000, _num_episodes=1000, _evaluate_every=100):

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
    dqn_agent = DQNAgent(
        num_actions=env.num_actions,
        state_shape=env.state_shape[0],
        mlp_layers=_mlp_layer,
        device=device,
    )
    random_agent1 = RandomAgent(num_actions=env.num_actions)
    random_agent2 = RandomAgent(num_actions=env.num_actions)
    random_agent3 = RandomAgent(num_actions=env.num_actions)

    agents = [random_agent1, dqn_agent, random_agent2, random_agent3]

    env.set_agents(agents)  # set agents to the environment

    # Start training
    with Logger(_log_dir) as logger:
        for episode in range(_num_episodes):

            # Generate data from the environment
            trajectories, payoffs = env.run(is_training=True)

            # Reorganaize the data to be state, action, reward, next_state, done
            trajectories = reorganize(trajectories, payoffs)

            # Feed transitions into agent memory, and train the agent
            for ts in trajectories[0]:
                dqn_agent.feed(ts)

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

    # Save model
    save_path = os.path.join(_log_dir, 'model.pth')
    torch.save(dqn_agent, save_path)
    print('Model saved in', save_path)


if __name__ == "__main__":
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    train(**args)
