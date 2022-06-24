from rlcard.games.cego.utils import load_model
import rlcard
import torch
from rlcard.utils import (
    get_device,
)  # import some useful functions

env_name = 'cego'
game_variant = 'standard'
game_judge_by_points = 0
game_activate_heuristic = True
game_train_env = [False, False, False, False]
path = "final_models/dmc_cego/dmc/0_608972800.pth"


def main():

    device = get_device()

    env = rlcard.make(
        env_name,
        config={
            'game_variant': game_variant,
            'game_judge_by_points': game_judge_by_points,
            'game_activate_heuristic': game_activate_heuristic,
            'game_train_env': game_train_env
        }
    )
    dummy_input = torch.zeros(1, 336)

    model = load_model(path, env, 0, device)
    torch.onnx.export(model, dummy_input, 'onnx_model.onnx', verbore= True)


if __name__ == '__main__':
    main()
