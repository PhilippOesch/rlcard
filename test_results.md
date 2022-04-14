# Test results of RL-Models in Uno

## DQN:

### Parameters

* seed: 10
* episodes: 1000
* evaluation games: 10000
* MLP-layer: 128, 128

### Training:
![Uno_Training_DQN](./experiments/uno_dqn_result/fig.png)

## NFSP:

### Parameters

* seed: 10
* episodes: 1000
* evaluation games: 10000
* MLP-layer: 128, 128
* hidden-layer_-sizes: 128, 128

### Training
![Uno_Training_NFSP](./experiments/uno_nfsp_result/fig.png)

Tournament Result:

| Comparison | Agent 0 | Agent 1 |
|----------|:-------------:|------:|
| DQN vs. Random | 0.019 | -0.019 |
| NFSP vs. Random | 0.0032 | -0.0032 |
| DQN vs. NFSP | 0.0048 | -0.0048 |
