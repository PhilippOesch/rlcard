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

## About this Repository

This repository contains the full source code of the thesis.

The framework is a fork of [RLCard](https://github.com/datamllab/rlcard) and, therefore, parts of this repository are external source code. The following folders/ files contain thesis specific content and are not external source code:

* [rlcard/games/cego](rlcard/games/cego)
* [rlcard/envs/cego.py](rlcard/envs/cego.py)
* [rlcard/agents/human_agents/cego_human_agent.py](rlcard/agents/human_agents/cego_human_agent.py)
* [results](results)
* [python_scripts](python_scripts)
* [thesis](thesis)

## Setting up the Environment

The following tools are needed to setup the environment:

* [Python 3](https://www.python.org/downloads/) (Python 3.9 was used)
* [Virtualenv](https://pypi.org/project/virtualenv/)

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
