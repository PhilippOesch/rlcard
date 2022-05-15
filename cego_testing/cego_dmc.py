import torch

import rlcard
from rlcard.agents.dmc_agent import DMCTrainer

from training_utils import save_args_params

args = {
    'env': 'cego',
    'game_variant': 'standard',
    'game_judge_by_points': 2,
    'seed': 12,
    'load_model': False,
    'xpid': 'dmc',
    'num_actor_devices': 1,
    'num_actors': 4,
    'training_device': '0',
    'log_dir': 'experiments/cego_dmc_standard',
    'total_frames': 100000000000,
    'exp_epsilon': 0.01,
    'batch_size': 32,
    'unroll_length': 100,
    'num_buffers': 50,
    'num_threads': 4,
    'max_grad_norm': 40,
    'learning_rate' : 0.0001,
    'alpha' : 0.99,
    'momentum' : 0,
    'epsilon' : 0.00001
}


def train():
    save_args_params(args)
    pass
