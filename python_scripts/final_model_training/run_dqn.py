import os

import torch

import rlcard
from rlcard.agents import DQNAgent
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
# dqn_point_var_0/model_4
args = {
    "log_dir": "results/final_models/dqn/test_dqn_cego_player_1",
    "env_name": "cego",
    "game_variant": "standard",
    "game_activate_heuristic": True,
    "game_judge_by_points": 0,
    "game_train_players": [True, True, True, True],
    "seed": 20,
    "replay_memory_size": 100000,
    "update_target_estimator_every": 10000,
    "discount_factor": 0.95,
    "epsilon_start": 1.0,
    "epsilon_end": 0.1,
    "epsilon_decay_steps": 100000,
    "batch_size": 32,
    "mlp_layers": [512, 512],
    "num_eval_games": 1000,
    "num_episodes": 1000000,
    "evaluate_every": 1000,
    "save_model_every": 50000,
    "learning_rate": 1e-05,
}


def train(log_dir, env_name, game_variant, game_activate_heuristic,
          game_judge_by_points, game_train_players, seed, replay_memory_size,
          update_target_estimator_every, discount_factor,
          epsilon_start, epsilon_end, epsilon_decay_steps,
          batch_size, mlp_layers, num_eval_games,
          num_episodes, evaluate_every, save_model_every, learning_rate):
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
    agents = [
        RandomAgent(num_actions=env.num_actions),
        dqn_agent,
        RandomAgent(num_actions=env.num_actions),
        RandomAgent(num_actions=env.num_actions)
    ]

    env.set_agents(agents)  # set agents to the environment

    checkpoint_count = 0

    # Start training
    with MyLogger(log_dir) as logger:
        prev_avg_reward = 0
        cur_avg_reward = 0
        cur_avg_steps = 1

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
                tournament_reward = tournament(
                    env,
                    num_eval_games,
                )[1]

                logger.log_performance(
                    env.timestep,
                    tournament_reward
                )

                cur_avg_reward = (tournament_reward + cur_avg_reward *
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
                save_path = os.path.join(
                    log_dir + "/checkpoint_"+str(checkpoint_count), 'model.pth')
                torch.save(dqn_agent, save_path)
                plot_curve(csv_path, fig_path, "DQN")
                checkpoint_count += 1
                print('Model saved in', save_path)

        logger.save_csv()
        os.mkdir(log_dir + "/checkpoint_"+str(checkpoint_count))
        csv_path, fig_path = logger.csv_path, log_dir
        save_path = os.path.join(log_dir, 'model_final.pth')
        torch.save(dqn_agent, save_path)
        plot_curve(csv_path, fig_path, "DQN")
        print('Model saved in', save_path)


if __name__ == '__main__':
    save_args_params(args)
    os.environ["CUDA_VISIBLE_DEVICES"] = "cpu"
    train(**args)
