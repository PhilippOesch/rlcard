# RL_AIService_Cego

This is the Service for the Predicted AI Moves:

## Endpoints

| EndPoint       | Description                                         | Expected Query-Params                                                                                                                             | Return Value   |
| -------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| api/v1/cego/ | Returns best card for the Mode Cego (all its forms) | hand_cards: list, played_cards: list, trick_cards: list, legage_cards: list, round_starter_id: Int, current_player_id: Int, single_player_id: Int | Predicted Move |
| api/v1/solo/ | Returns best card for the Mode Solo                 | hand_cards: list, played_cards: list, trick_cards: list, round_starter_id: Int, current_player_id: Int, single_player_id: Int                     | Predicted Move |
| api/v1/ultimo/ | Returns best card for the Mode Ultimo                 | hand_cards: list, played_cards: list, trick_cards: list, round_starter_id: Int, current_player_id: Int, single_player_id: Int                     | Predicted Move |
| api/v1/bettel/ | Returns best card for the Mode Bettel                 | hand_cards: list, played_cards: list, trick_cards: list, round_starter_id: Int, current_player_id: Int, single_player_id: Int                     | Predicted Move |
| api/v1/piccolo/ | Returns best card for the Mode Bettel                 | hand_cards: list, played_cards: list, trick_cards: list, round_starter_id: Int, current_player_id: Int, single_player_id: Int                     | Predicted Move |
| api/v1/raeuber/ | Returns best card for the Mode Bettel                 | hand_cards: list, played_cards: list, trick_cards: list, round_starter_id: Int, current_player_id: Int, raeuber_id: Int                     | Predicted Move |

### Description of Query-Parameters

- **hand_cards**: cards the current player has on his played.
- **played_cards**: cards that have been played this (previous tricks) (with or without the current trick)
- **trick_cards**: cards of the current trick. The have to be in the order they were played in!
- **legage_cards**: cards thrown away at the start of the game (only expected when part of player knowledge)
- **round_starter_id**: id of player who started the current trick round. Possible values = integer [0..3]
- **current_player_id**: id of player who has to play the next card. Possible values = integer [0..3]
- **single_player_id**: id of player that plays by himself (cego player, solo player, etc.). Possible values = integer [0..3]
- **raeuber_id**: id of the player who called Räuber (Only needed for game mode Räuber). Possible values = integer [0..3]

### Training conditions of models

#### Cego

Only sub games were considered where the Cego player has at least a combined 15 value points on their hand.

#### Solo

Only sub games were considered where the Solo player has either at least 8 trumps on their hand or at least 7 trumps with two trumps that are greater than or equal to **17-trump** and the other four cards are only of two different colors.

### Ultimo

Games where considered where the Ultimo player has at least 8 trumps of which one is of the card "1-trump".

### Bettel

All Games where considered where the Bettel player only has low cards. For the definition of what is considered a low card please read the [thesis](thesis/Philipp_Oeschger_268388_Master_Thesis.pdf) where this project is based on. 

### Piccolo

All Games where considered where the Piccolo player all low cards but exactly one high card. Again please consider reading the [thesis](thesis/Philipp_Oeschger_268388_Master_Thesis.pdf) of this project to find a definition of high and low cards in Cego.

### Räuber

All games where considered.

### Example

Call:

```bash
curl --location --request GET 'http://127.0.0.1:8000/api/v1/cego/?hand_cards=18-trump,15-trump,13-trump,r-d,r-c,b-h,3-h,20-trump,17-trump&played_cards=r-h,16-trump,4-h,2-h,21-trump,6-trump,9-trump,10-trump&trick_cards=8-s,r-s,k-s&legage_cards=11-trump,7-trump,1-trump,k-h,k-d,d-h,2-d,4-d,7-s,3-d&current_player_id=0&round_starter_id=1&single_player_id=0'
```

Response:

```json
{
  "action": "13-trump"
}
```

## Card Encoding

These Values can be used for card inputs:

[Action Space](/src/deepl-ai-service/app/jsondata/action_space.json)

## Folder-Structure

* [app](src/deepl-ai-service/app) – api sub folder
  * *api_v[x]* - folder for a specific api version
    * [plugin](src/deepl-ai-service/app/api_v1/plugins) – helper_classes
    * [testing](src/deepl-ai-service/app/api_v1/testing) - contains tests
    * [main.py](src/deepl-ai-service/app/api_v1/main.py) - main file that is called when the api is initialized
* [jsondata](src/deepl-ai-service/app/jsondata) – contains data such as card encoding and model mapping
  * [action_space.json](src/deepl-ai-service/app/jsondata/action_space.json) – encoding of cards
  * [model_paths.json](src/deepl-ai-service/app/jsondata/model_paths.json) – mapping of game modes to model weights
* [models](src/deepl-ai-service/app/models) - contains the AI models

## Setup

This project uses [Virual Environments](https://docs.python.org/3/tutorial/venv.html) for development and [Docker](https://www.docker.com/) for deployment.
There are two requirement files:

* *requirements.txt*: contains development packages including for testing.
* *docker_requirements.txt*: contains minimal packages needed for deployment.

### Requirements

Python 3:

[Download](https://www.python.org/downloads/)

Install Virtal-Env:

```bash
pip install virtualenv
```

### Setup Developer Environment with Virtualenv

**Jump to folder:**

```bash
cd src/deepl-ai-service
```

**Setup Virtualenv:**

```bash
python3 -m venv venv
```

**Activate Environment**:


MacOs:
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

**Install Dev Dependencies:**

```bash
pip install -r requirements.txt
```

### Development

Activate Env:

```bash
source venv/bin/activate
```

Start Server:

```bash
uvicorn app.api_v1.main:app --reload
```

```bash
pytest
```

### Docker Setup for Deployment

Build Image:

```bash
docker build -t ai_service_image .
```

Start Container with containing Server:

```bash
docker run -d --name ai_service_container -p 8000:80 ai_service_image
```

Service is than available at http://localhost:8000/api/v1/
