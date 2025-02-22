import os

import torch

import rlcard
from rlcard.agents import DQNAgent
from rlcard.agents.random_agent import RandomAgent

from rlcard.games.cego.utility.random_search import randomSearch

from rlcard.utils import (
    tournament,
    reorganize,
    Logger,
    plot_curve,
    get_device,
    set_seed,
)  # import some useful functions

random_search_iterations = 20

# arguments for the random search

args = {
    "env_name": ["cego"],
    "game_judge_by_points": [1],
    "game_variant": ["standard"],
    "game_activate_heuristic": [True],
    "game_train_players": [[True, True, True, True]],
    "seed": [12],
    "replay_memory_size": [50000, 100000, 200000],
    "update_target_estimator_every": [1000, 2000, 10000],
    "discount_factor": [0.75, 0.8, 0.95, 0.99],
    "epsilon_start": [1.0],
    "epsilon_end": [0.1, 0.05, 0.01],
    "epsilon_decay_steps": [50000],
    "batch_size": [32, 64],
    "mlp_layers": [[512, 512, 512], [512, 256, 128], [512, 512]],
    "num_eval_games": [1000],
    "num_episodes": [50000],
    "evaluate_every": [500],
    "learning_rate": [0.0001, 0.00005, 0.00001, 0.000005]
}


def train(log_dir, env_name, game_variant, game_activate_heuristic,
          game_judge_by_points, game_train_players, seed, replay_memory_size,
          update_target_estimator_every, discount_factor,
          epsilon_start, epsilon_end, epsilon_decay_steps,
          batch_size, mlp_layers, num_eval_games,
          num_episodes, evaluate_every, learning_rate):
    # Check whether gpu is available
    device = get_device()
    print(device)

    set_seed(seed)

    # Make the environment with seed
    env = rlcard.make(
        env_name,
        config={
            'seed': seed,
            'game_variant': game_variant,
            'game_activate_heuristic': game_activate_heuristic,
            'game_judge_by_points': game_judge_by_points,
            'game_train_players': game_train_players
        }
    )

    # # this is our DQN agent
    dqn_agent = DQNAgent(
        num_actions=env.num_actions,
        state_shape=env.state_shape[0],
        mlp_layers=mlp_layers,
        device=device,
        replay_memory_size=replay_memory_size,
        update_target_estimator_every=update_target_estimator_every,
        discount_factor=discount_factor,
        epsilon_start=epsilon_start,
        epsilon_end=epsilon_end,
        epsilon_decay_steps=epsilon_decay_steps,
        batch_size=batch_size,
        learning_rate=learning_rate

    )
    agents = [dqn_agent]
    for _ in range(1, env.num_players):
        agents.append(RandomAgent(num_actions=env.num_actions))

    env.set_agents(agents)  # set agents to the environment

    # Start training
    with Logger(log_dir) as logger:
        for episode in range(num_episodes):

            # Generate data from the environment
            trajectories, payoffs = env.run(is_training=True)

            # Reorganaize the data to be state, action, reward, next_state, done
            trajectories = reorganize(trajectories, payoffs)

            # Feed transitions into agent memory, and train the agent
            for ts in trajectories[0]:
                dqn_agent.feed(ts)

            # Evaluate the performance.
            if episode % evaluate_every == 0:
                logger.log_performance(
                    env.timestep,
                    tournament(
                        env,
                        num_eval_games,
                    )[0]
                )

        # Get the paths
        csv_path, fig_path = logger.csv_path, logger.fig_path

    # Plot the learning curve
    plot_curve(csv_path, fig_path, "DQN")

    # Save model
    save_path = os.path.join(log_dir, 'model.pth')
    torch.save(dqn_agent, save_path)
    print('Model saved in', save_path)


if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "cpu"
    randomSearch(train, args, 'random_search_results/random_search/dqn_point_var_test',
                 random_search_iterations)
