import optuna
from optuna.pruners import MedianPruner
from optuna.samplers import TPESampler
from optuna.visualization import plot_optimization_history, plot_param_importances

N_TRIALS = 100  # Maximum number of trials
N_JOBS = 1 # Number of jobs to run in parallel
N_STARTUP_TRIALS = 5  # Stop random sampling after N_STARTUP_TRIALS
N_EVALUATIONS = 2  # Number of evaluations during the training
N_TIMESTEPS = int(2e4)  # Training budget
EVAL_FREQ = int(N_TIMESTEPS / N_EVALUATIONS)
N_EVAL_ENVS = 5
N_EVAL_EPISODES = 10
TIMEOUT = int(60 * 15)  # 15 minutes

env_name= "cego"
game_judge_by_points= 0
seed= 12
game_variant= "standard",
game_activate_heuristic: True

train_every = 1
min_buffer_size_to_learn= 100
q_replay_memory_init_size= 100
q_epsilon_decay_steps= int(50000)
num_eval_games= 10000
num_episodes= 40000
evaluate_every= 400

def sample_a2c_params(trial: optuna.Trial) -> Dict[str, Any]:
    """
    Sampler for A2C hyperparameters.

    :param trial: Optuna trial object
    :return: The sampled hyperparameters for the given trial.
    """
    # Discount factor between 0.9 and 0.9999
    hidden_layers_sizes = trial.suggest_categorical("hidden_layers_sizes", [[128, 128],[256, 256],[512, 512], [512, 512, 512]])
    # reservoir_buffer_capacity = trial.suggest_categorical("reservoir_buffer_capacity", [20000, 50000, 100000])
    reservoir_buffer_capacity = trial.suggest_int("reservoir_buffer_capacity", 20000, 100000, 500)
    anticipatory_param = trial.suggest_float("anticipatory_param", 0.1, 0.5, log=True)
    batch_size = 2** trial.suggest_int("batch_size", 5, 7, 1)
    rl_lr = trial.suggest_float("rl_lr", 0.000005, 0.1, log=True)
    sl_lr = trial.suggest_float("sl_lr", 0.000005, 0.1, log=True)
    q_replay_memory_size= trial.suggest_int("q_replay_memory_size", 20000, 200000, 10000)
    q_update_target_estimator_every = trial.suggest_int("q_update_target_estimator_every", 1000, 20000, 1000)
    q_discount_factor = 1.0 - trial.suggest_float("gamma", 0.0001, 0.25, log=True)
    q_epsilon_start = trial.suggest_float("epsilon", 0.01, 0.1, log=True)
    q_epsilon_end = trial.suggest_float("epsilon_end", 0.0001, 0.1, log=True)
    q_batch_size= trial.suggest_categorical("q_batch_size", [32, 64])
    q_mlp_layer_size= trial.suggest_categorical("q_mlp_layer_size", [[256, 256],[512, 512], [512, 512, 512], [512, 256, 128]])


    ### END OF YOUR CODE

    # Display true values
    trial.set_user_attr("gamma_", q_discount_factor)
    trial.set_user_attr("batch_size", batch_size)

    return {
        "hidden_layers_sizes": hidden_layers_sizes,
        "reservoir_buffer_capacity": reservoir_buffer_capacity,
        "anticipatory_param": anticipatory_param,
        "batch_size": batch_size,
        "rl_lr": rl_lr,
        "sl_lr": sl_lr,
        "q_replay_memory_size": q_replay_memory_size,
        "q_update_target_estimator_every": q_update_target_estimator_every,
        "q_discount_factor": q_discount_factor,
        "q_epsilon_start": q_epsilon_start,
        "q_epsilon_end": q_epsilon_end,
        "q_batch_size": q_batch_size,
        "q_mlp_layer_size": q_mlp_layer_size,
    }