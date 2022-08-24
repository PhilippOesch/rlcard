import os
import torch

import rlcard
from rlcard.agents import NFSPAgent
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
ALL_DL_AGENTS = False

args = {
    "env_name": ["cego"],
    "game_judge_by_points": [1],
    "seed": [12],
    "game_variant": ["standard"],
    "game_activate_heuristic": [True],
    "game_train_players": [[True, True, True, True]],
    "hidden_layers_sizes": [[128, 128], [256, 256], [512, 512], [512, 512, 512]],
    "reservoir_buffer_capacity": [20000, 50000, 100000, 200000],
    "anticipatory_param": [0.1, 0.2, 0.25, 0.35, 0.5],
    "batch_size": [128, 64, 32],
    "train_every": [1],
    "rl_learning_rate": [1e-05],
    "sl_learning_rate": [0.001, 0.0001, 0.00005, 0.00001, 0.000005],
    "min_buffer_size_to_learn": [100],
    "q_replay_memory_size": [100000],
    "q_replay_memory_init_size": [100],
    "q_update_target_estimator_every": [10000],
    "q_discount_factor": [0.95],
    "q_epsilon_start": [1],
    "q_epsilon_end": [0.1],
    "q_epsilon_decay_steps": [int(50000)],
    "q_batch_size": [32],
    "q_train_every": [1],
    "q_mlp_layer": [[512, 512]],
    "num_eval_games": [1000],
    "num_episodes": [50000],
    "evaluate_every": [500]
}


def train(log_dir, env_name, game_judge_by_points, game_variant, game_activate_heuristic,
          game_train_players, seed, hidden_layers_sizes, reservoir_buffer_capacity,
          anticipatory_param, batch_size, train_every, rl_learning_rate, sl_learning_rate,
          min_buffer_size_to_learn, q_replay_memory_size, q_replay_memory_init_size,
          q_update_target_estimator_every, q_discount_factor, q_epsilon_start, q_epsilon_end,
          q_epsilon_decay_steps, q_batch_size, q_train_every,
          q_mlp_layer, num_eval_games=10000, num_episodes=1000,
          evaluate_every=100):
    # Check whether gpu is available
    device = get_device()

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

    agents = []

    nfsp_agent = NFSPAgent(
        num_actions=env.num_actions,
        state_shape=env.state_shape[0],
        hidden_layers_sizes=hidden_layers_sizes,
        reservoir_buffer_capacity=reservoir_buffer_capacity,
        anticipatory_param=anticipatory_param,
        batch_size=batch_size,
        train_every=train_every,
        rl_learning_rate=rl_learning_rate,
        sl_learning_rate=sl_learning_rate,
        min_buffer_size_to_learn=min_buffer_size_to_learn,
        q_replay_memory_size=q_replay_memory_size,
        q_replay_memory_init_size=q_replay_memory_init_size,
        q_update_target_estimator_every=q_update_target_estimator_every,
        q_discount_factor=q_discount_factor,
        q_epsilon_start=q_epsilon_start,
        q_epsilon_end=q_epsilon_end,
        q_epsilon_decay_steps=q_epsilon_decay_steps,
        q_batch_size=q_batch_size,
        q_train_every=q_train_every,
        q_mlp_layers=q_mlp_layer,
        device=device,
    )
    agents.append(nfsp_agent)

    for _ in range(1, env.num_players):
        agents.append(RandomAgent(num_actions=env.num_actions))

    env.set_agents(agents)

    # Start training
    with Logger(log_dir) as logger:
        for episode in range(num_episodes):

            agents[0].sample_episode_policy()

            # Generate data from the environment
            trajectories, payoffs = env.run(is_training=True)

            # Reorganaize the data to be state, action, reward, next_state, done
            trajectories = reorganize(trajectories, payoffs)

            # Feed transitions into agents memories, and train the agent
            for ts in trajectories[0]:
                nfsp_agent.feed(ts)

            # Evaluate the performance.s.
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
    plot_curve(csv_path, fig_path, "NFSP")

    # Save models
    save_path = os.path.join(log_dir, 'model.pth')
    torch.save(nfsp_agent, save_path)
    print('Model saved in', save_path)


if __name__ == '__main__':
    randomSearch(train, args, 'random_search_results/random_search/nfsp_point_var_test',
                 random_search_iterations)
