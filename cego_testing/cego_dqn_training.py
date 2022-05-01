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
    "_log_dir": "experiments/cego_dqn_result_player_0_model4/",
    "_env_name": "cego",
    "_seed": 10,
    "_replay_memory_size": 20000,
    "_update_target_estimator_every": 1000,
    "_discount_factor": 0.99,
    "_epsilon_start": 1.0,
    "_epsilon_end": 0.1,
    "_epsilon_decay_steps": 20000,
    "_batch_size": 32,
    "_mlp_layers": [512, 512],
    "_num_eval_games": 10000,
    "_num_episodes": 1000,
    "_evaluate_every": 100,
    "_learning_rate": 0.0001
}


def train(_log_dir, _env_name, _seed, _replay_memory_size,
          _update_target_estimator_every, _discount_factor,
          _epsilon_start, _epsilon_end, _epsilon_decay_steps,
          _batch_size, _mlp_layers, _num_eval_games,
          _num_episodes, _evaluate_every, _learning_rate):

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
        mlp_layers=_mlp_layers,
        device=device,
        replay_memory_size=_replay_memory_size,
        update_target_estimator_every=_update_target_estimator_every,
        discount_factor=_discount_factor,
        epsilon_start=_epsilon_start,
        epsilon_end=_epsilon_end,
        epsilon_decay_steps=_epsilon_decay_steps,
        batch_size=_batch_size,
        learning_rate=_learning_rate

    )
    random_agent1 = RandomAgent(num_actions=env.num_actions)
    random_agent2 = RandomAgent(num_actions=env.num_actions)
    random_agent3 = RandomAgent(num_actions=env.num_actions)

    agents = [dqn_agent, random_agent1, random_agent2, random_agent3]

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
    # os.environ["CUDA_VISIBLE_DEVICES"] = "cuda"
    train(**args)
