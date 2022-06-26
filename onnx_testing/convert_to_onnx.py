from rlcard.games.cego.utils import load_model
import rlcard
from rlcard.agents.dmc_agent.model import DMCAgent
import torch
from rlcard.utils import (
    get_device,
)  # import some useful functions

env_name = 'cego'
game_variant = 'standard'
game_judge_by_points = 0
game_activate_heuristic = True
game_train_env = [False, False, False, False]
path = "final_models/dmc_cego/dmc/0_800985600.pth"


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
    dummy_input = torch.randn(size=(336, 54))
    model = load_model(path, env, 0, device)
    model_scripted = torch.jit.script(model)
    model_scripted.save('model_scripted.pt')
    # print(model_script)
    # torch.onnx.export(model_script, dummy_input, 'onnx_model.onnx', verbose= True)


if __name__ == '__main__':
    main()
