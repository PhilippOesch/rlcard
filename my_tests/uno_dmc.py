import os
import argparse

import torch

import rlcard
from rlcard.agents.dmc_agent import DMCTrainer

# Make the environment
env = rlcard.make("uno")

# setting args
args = {
    'env': env,
    'cuda': '',
    'load_model': False,
    'xpid': 'uno_dmc',
    'savedir': 'experiments/uno_dmc_result',
    'save_interval': 30,
    'num_actor_devices': 1,
    'num_actors': 3,
    'training_device': '0',
}


def train(args):

    # Initialize the DMC trainer
    trainer = DMCTrainer(
        env,
        cuda=args["env"],
        load_model=args["cuda"],
        xpid=args["xpid"],
        savedir=args["savedir"],
        save_interval=args["save_interval"],
        num_actor_devices=args["num_actor_devices"],
        num_actors=args["num_actors"],
        training_device=args["training_device"],
    )

    trainer.start()


if __name__ == "__main__":
    os.environ["CUDA_VISIBLE_DEVICES"] = args["cuda"]
    train(args)
