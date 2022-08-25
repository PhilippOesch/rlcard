# An Application of Modern Reinforcement Learning Algorithms to The Card Game Cego 

## General Information

* **supervised by**:  Prof. Dr. Maja Temerinac-Ott
* **cosupervised by**: Prof. Jirka Dell´Oro-Friedl
* **submitted on**: 31.08.2022
* **submitted by**: 
    * Philipp Oeschger
    * matriculation number: 268388
    * Bregstraße 90
    * 78120 Furtwangen im Schwarzwald
    * philipp.oeschger@hs-furtwangen.de

* [Link to Master Thesis](thesis/Philipp_Oeschger_268388_Master_Thesis.pdf)

## About this Repository

This repository contains the full source code of the thesis.

The framework is a fork of [RLCard](https://github.com/datamllab/rlcard) and, therefore, the **src/rl_env** folder contains external source code. The following files / folders in **src/rl_env** do **not** contain external code:

* [src/rl_env/rlcard/games/cego](src/rl_env/rlcard/games/cego)
* [src/rl_env/rlcard/envs/cego.py](src/rl_env/rlcard/envs/cego.py)
* [src/rl_env/rlcard/agents/human_agents/cego_human_agent.py](src/rl_env/rlcard/agents/human_agents/cego_human_agent.py)
* [src/rl_env/results](src/rl_env/results)
* [src/rl_env/python_scripts](src/rl_env/python_scripts)

## Description of the structure:

### Class Diagramm of Game Implementation:
![Class Diagram](readme_imgs/class_diagram_rlcard_cego_simple.drawio.png)

### File Stucture of **src** folder:
* [rlcard/games/cego](rlcard/games/cego): The implementation of the game logic.
    * jsondata: contains card encoding, high cards and low cards list.
    * testing: contains script for testing the environment
    * utility: contains utility function modules for:
        * evaluations
        * game implementation
        * custom logging
        * random search Hyper parameter optimization
    * ... game classes described in class diagram
* [rlcard/envs/cego.py](rlcard/envs/cego.py): The environment class for the game.
* [rlcard/agents/human_agents/cego_human_agent.py](rlcard/agents/human_agents/cego_human_agent.py): An agent that serves as testing interface to play against AI models.
* [results](results): contains various results, including evaluations, model training, random search results: ...
* [python_scripts](python_scripts): script for training, hyperparameter search and evaluation.
    * cego_random_search: random search scripts for dqn and nfsp.
    * final_model_training: contains,
        * evaluation of models
        * analysis of the game environment
        * scripts for final dmc, dqn, and nfsp training
* [deepl-ai-service](deepl-ai-service): The API that makes the model available.
    * this is a seperate service that requires a seperate setup
    * [more details here](src/deepl-ai-service/README.md)
* [thesis](thesis): contains the Thesis PDF.

## Setting up the Environment

The following tools are needed to setup the environment:

* [Python 3](https://www.python.org/downloads/) (Python 3.9 was used)
* [Virtualenv](https://pypi.org/project/virtualenv/)

### Open rl_env_folder

```bash
cd src/rl_env
```

### Create an environment

Mac OS:

```bash
source venv/bin/activate
```

Linux:

```bash
source venv/Scripts/activate
```

Windows:

```bash
.\venv\Scripts\activate
```

### Activate Environment

MacOS:

```bash
source venv/bin/activate
```

Linux:

```bash
source venv/Scripts/activate
```

Windows:

```bash
.\venv\Scripts\activate
```

### Install the Dependencies

1.

```bash
pip install -r requirements.txt
```

2.

```bash
pip3 install -e .
```

### Run Tests for RL-Env:

```bash
python -m unittest discover 
```