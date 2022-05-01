import os

import torch
import rlcard
from rlcard.agents import (
    NFSPAgent,
    RandomAgent
)

from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
)

args = {
    "_seed": 10,
    "_models": [
        ["experiments/cego_dqn_result_player_0/model.pth",
         "random", "random", "random"]],
    "_env_name": "cego",
    "_num_games": 10000,
}


def load_model(model_path, env=None, position=None, device=None):
    import torch
    if os.path.isfile(model_path):  # Torch model
        agent = torch.load(model_path, map_location=device)
        agent.set_device(device)
    elif model_path == 'random':  # Random model
        from rlcard.agents import RandomAgent
        agent = RandomAgent(num_actions=env.num_actions)

    return agent


def evaluate(_seed, _models, _env_name, _num_games):

    # Check whether gpu is available
    device = get_device()

    # Seed numpy, torch, random
    set_seed(_seed)

    # Make the environment with seed
    env = rlcard.make(_env_name, config={'seed': _seed})

    # Load models
    agents = []
    for position, model_path in enumerate(_models):
        agents.append(load_model(model_path, env, position, device))
    env.set_agents(agents)

    # Evaluate
    rewards = tournament(env, _num_games)
    for position, reward in enumerate(rewards):
        print(position, _models[position], reward)


if __name__ == '__main__':
    evaluate(args["_seed"], args["_models"][0],
             args["_env_name"], args["_num_games"])
