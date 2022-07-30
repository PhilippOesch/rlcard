import os

import torch

import rlcard
from rlcard.agents import NFSPAgent
from rlcard.agents.random_agent import RandomAgent

from rlcard.games.cego.utility.training import save_args_params

from rlcard.utils import (
    tournament,
    reorganize,
    MyLogger,
    plot_curve,
    get_device,
    set_seed,
)  # import some useful functions

# arguments for the random search
# nfsp_poinr_var_0_tuned_dqn/model_12
args = {
    "log_dir": "results/final_models/nfsp_all_nfsp_agents",
    "env_name": "cego",
    "game_variant": "standard",
    "game_activate_heuristic": True,
    "game_judge_by_points": 0,
    "game_train_players": [True, True, True, True],
    "seed": 20,  # training seed
    "hidden_layers_sizes": [512, 512],
    "reservoir_buffer_capacity": 100000,
    "anticipatory_param": 0.5,
    "batch_size": 32,
    "rl_learning_rate": 1e-05,
    "sl_learning_rate": 0.0001,
    "min_buffer_size_to_learn": 100,
    "q_replay_memory_size": 100000,
    "q_replay_memory_init_size": 100,
    "q_update_target_estimator_every": 10000,
    "q_discount_factor": 0.95,
    "q_epsilon_start": 1,
    "q_epsilon_end": 0.1,
    "q_epsilon_decay_steps": 100000,
    "q_batch_size": 32,
    "train_every": 1,
    "q_train_every": 1,
    "q_mlp_layer": [512, 512],
    "num_eval_games": 1000,
    "num_episodes": 1000000,
    "evaluate_every": 1000,
    "save_model_every": 50000,
}


def train(log_dir, env_name, game_judge_by_points, game_variant, game_activate_heuristic,
          game_train_players, seed, hidden_layers_sizes, reservoir_buffer_capacity,
          anticipatory_param, batch_size, train_every, rl_learning_rate, sl_learning_rate,
          min_buffer_size_to_learn, q_replay_memory_size, q_replay_memory_init_size,
          q_update_target_estimator_every, q_discount_factor, q_epsilon_start, q_epsilon_end,
          q_epsilon_decay_steps, q_batch_size, q_train_every,
          q_mlp_layer, num_eval_games=10000, num_episodes=1000,
          evaluate_every=100, save_model_every=50000):
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

    # compare first agent against random agents
    tournament_env = rlcard.make(
        env_name,
        config={
            'seed': seed,
            'game_variant': game_variant,
            'game_activate_heuristic': game_activate_heuristic,
            'game_judge_by_points': game_judge_by_points,
            'game_train_players': [False, False, False, False]
        }
    )
    agents = []
    for _ in range(env.num_players):
        agents.append(
            NFSPAgent(
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
        )

    env.set_agents(agents)  # set agents to the environment

    # init tournament agents
    tournament_agents_0 = [
        agents[0],
        RandomAgent(num_actions=tournament_env.num_actions),
        RandomAgent(num_actions=tournament_env.num_actions),
        RandomAgent(num_actions=tournament_env.num_actions)
    ]

    tournament_agents_1 = [
        RandomAgent(num_actions=tournament_env.num_actions),
        agents[1],
        RandomAgent(num_actions=tournament_env.num_actions),
        RandomAgent(num_actions=tournament_env.num_actions)
    ]

    checkpoint_count = 0

    # Start training
    with MyLogger(log_dir) as logger:
        prev_avg_reward = 0
        cur_avg_reward = 0
        cur_avg_steps = 1

        for episode in range(num_episodes):

            for i in range(len(agents)):
                agents[i].sample_episode_policy()
            # Generate data from the environment
            trajectories, payoffs = env.run(is_training=True)

            # Reorganaize the data to be state, action, reward, next_state, done
            trajectories = reorganize(trajectories, payoffs)

            # Feed transitions into agent memory, and train the agent
            for i in range(len(trajectories)):
                for ts in trajectories[i]:
                    agents[i].feed(ts)

            # Evaluate the performance.
            if episode % evaluate_every == 0:
                tournament_env.set_agents(tournament_agents_0)
                tournament_reward_0 = tournament(
                    tournament_env,
                    num_eval_games,
                )[0]
                tournament_env.set_agents(tournament_agents_1)
                tournament_reward_1 = tournament(
                    tournament_env,
                    num_eval_games,
                )[1]

                logger.log_performance(
                    env.timestep,
                    ":".join([tournament_reward_0, tournament_reward_1])
                )
                cur_avg_reward = (tournament_reward_0 + cur_avg_reward *
                                  (cur_avg_steps-1) / cur_avg_steps)
                cur_avg_steps += 1

            if episode % save_model_every == 0 or episode == 0:
                if(prev_avg_reward > cur_avg_reward):
                    break

                prev_avg_reward = cur_avg_reward
                cur_avg_reward = 0
                cur_avg_steps = 1

                logger.save_csv()
                os.mkdir(log_dir + "/checkpoint_"+str(checkpoint_count))
                csv_path, fig_path = logger.csv_path, log_dir + \
                    "/checkpoint_" + str(checkpoint_count)+"/fig.png"
                for i in range(len(agents)):
                    save_path = os.path.join(
                        log_dir + "/checkpoint_"+str(checkpoint_count), 'model_' + str(i) + '.pth')
                    torch.save(agents[i], save_path)
                plot_curve(csv_path, fig_path, "NFSP")
                checkpoint_count += 1
                print('Model saved in', save_path)

        logger.save_csv()
        os.mkdir(log_dir + "/checkpoint_"+str(checkpoint_count))
        csv_path, fig_path = logger.csv_path, log_dir
        save_path = os.path.join(log_dir, 'model_final.pth')
        for i in range(len(agents)):
            save_path = os.path.join(log_dir, 'model_final_'+str(i)+'.pth')
            torch.save(agents[i], save_path)
        plot_curve(csv_path, fig_path, "NFSP")
        print('Model saved in', save_path)


if __name__ == '__main__':
    save_args_params(args)
    os.environ["CUDA_VISIBLE_DEVICES"] = "cpu"
    train(**args)
