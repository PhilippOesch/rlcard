import torch
import os
import json
from collections import OrderedDict
import numpy as np
from fastapi import HTTPException
from pydantic import BaseModel

black_card_ranks: list = ['7', '8', '9', '10', 'b', 'r', 'd', 'k']
red_card_ranks: list = ['4', '3', '2', '1', 'b', 'r', 'd', 'k']
trump_card_ranks: list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                          '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                          '21', 'gstiess']

ACTION_SPACE_FILE_PATH: str = 'app/jsondata/action_space.json'
MODEL_PATHS_FILE_PATH: str = 'app/jsondata/model_paths.json'

ACTION_SPACE: OrderedDict = None  # action to index mapping
ACTION_LIST: list = None  # raw list of actions
MODEL_PATHS: dict = None  # dictionary for model mapping


class ActionPrediciton(BaseModel):
    '''
        class for an action prediction result
    '''
    action: str


def init() -> tuple:
    '''
        initialices model mapping and action encoding
    '''
    with open(os.path.join(ACTION_SPACE_FILE_PATH), 'r') as file:
        action_space = json.load(file, object_pairs_hook=OrderedDict)
        action_list = list(action_space.keys())

    with open(os.path.join(MODEL_PATHS_FILE_PATH), 'r') as file:
        raw_paths = json.load(file)
        model_paths = {}
        for key in raw_paths:
            model_paths[key] = []
            for val in raw_paths[key]:
                model_paths[key].append({
                    'model': None,
                    'path': val
                })

    return action_space, action_list, model_paths


def get_device() -> object:
    '''
        load device (required for model)
    '''
    if torch.cuda.is_available():
        device = torch.device('cuda:0')
        print('--> Running on the GPU')
    else:
        device = torch.device('cpu')
        print('--> Running on the CPU')

    return device


device = get_device()


def load_model(agent=None, model_path=None, device=None) -> object:
    '''
        loads an AI-Model
    '''
    if agent != None:
        return agent
    if os.path.isfile(model_path):  # Torch model
        agent = torch.load(model_path, map_location=device)
        agent.set_device(device)

    return agent


def check_cards_valid(hand_cards, legage_cards, played_cards, trick_cards) -> bool:
    '''
        checks whether all card have a valid key code
    '''

    hand_cards, legage_cards, played_cards, trick_cards = format_card_params(
        hand_cards, legage_cards, played_cards, trick_cards)
    all_cards = []
    if hand_cards != None:
        all_cards.extend(hand_cards)
    if legage_cards != None:
        all_cards.extend(legage_cards)
    if played_cards != None:
        all_cards.extend(played_cards)
    if trick_cards != None:
        all_cards.extend(trick_cards)
    valid_cards = [card for card in all_cards if card in ACTION_SPACE]
    return len(all_cards) == len(valid_cards)


def handle_errors(
    game_mode: str = None,
    hand_cards: str = None,
    legage_cards: str = None,
    played_cards: str = None,
    trick_cards: str = None,
    current_player_id: int = None,
    start_player_id: int = None,
    single_player_id: int = None
) -> None:
    '''
        Error handling for the following scenarios:
        *   hand cards provided
        *   current_player_id provided
        *   start_player_id provided (player that started the round)
        *   single_player_id provided (for all but game mode Raeuber)
        *   raeuber_id provided (only for game mode Raeuber)
        *   1-trump in hand deck (only for game mode Ultimo)
        *   hand deck has less or an equal of 11 card
    '''
    if hand_cards == None or hand_cards == '':
        raise HTTPException(
            status_code=400, detail='please provide information about the hand cards')
    if current_player_id == None or current_player_id == '':
        raise HTTPException(
            status_code=400, detail='please provide current_player_id')
    if start_player_id == None or start_player_id == '':
        raise HTTPException(
            status_code=400, detail='please provide start_player_id')

    print(game_mode)
    if (single_player_id == None or single_player_id == '') and game_mode != 'raeuber':
        raise HTTPException(
            status_code=400, detail='please provide single_player_id')
    if (single_player_id == None or single_player_id == '') and game_mode == 'raeuber':
        raise HTTPException(
            status_code=400, detail='please provide raeuber_id (The player who called raeuber)')
    if not check_cards_valid(hand_cards, legage_cards, played_cards, trick_cards):
        raise HTTPException(
            status_code=400, detail='Not all card codes provided are valid')

    hand_card_array: list = hand_cards.split(',')
    has_geiss: bool = '1-trump' in hand_card_array

    if game_mode == 'ultimo' and not has_geiss:
        raise HTTPException(
            status_code=400, detail='ultimo deck does not provide 1-trump card')
    if len(hand_card_array) > 11:
        print('len', len(hand_card_array))
        raise HTTPException(
            status_code=400, detail='hand card deck is to large (has more than 11 cards)')


def predict(
    mode: str = None,
    hand_cards: str = None,
    legage_cards: str = None,
    played_cards: str = None,
    trick_cards: str = None,
    current_player_id: int = None,
    round_starter_id: int = None,
    single_player_id: int = None,
    is_raeuber: bool = False
) -> str:
    '''
        The function action prediction function
    '''

    # format the card informations
    hand_cards, legage_cards, played_cards, trick_cards = format_card_params(
        hand_cards, legage_cards, played_cards, trick_cards)

    # extracting winner card and winner id
    current_winning_card, current_winning_id = get_winning_card(trick_cards)

    # adjust ids relativ to model
    current_player_id: int = (current_player_id - single_player_id) % 4
    round_starter_id: int = (round_starter_id - single_player_id) % 4
    single_player_id: int = 0

    # mapping of models
    model: object = load_model(
        MODEL_PATHS[mode][current_player_id]['model'],
        MODEL_PATHS[mode][current_player_id]['path'],
        device
    )

    # format the observation
    obs = to_obs(hand_cards, legage_cards, played_cards, current_winning_card, trick_cards,
                 current_player_id, round_starter_id, current_winning_id, is_raeuber)

    # setup of state-dict required for model-prediction
    state: dict = {}
    state['obs'] = obs
    state['raw_legal_actions'] = get_legal_actions(hand_cards, trick_cards)
    legal_ids: dict = {
        ACTION_SPACE[action]: None for action in state['raw_legal_actions']}
    state['legal_actions'] = OrderedDict(legal_ids)

    # The prediciton
    model_pred = model.eval_step(state)
    action_id: int = model_pred[0]

    # check if predicted action is a valid action
    if action_id in legal_ids:
        return ACTION_LIST[action_id]

    # if the prediction is not a legal move, return a random legal move
    return ACTION_LIST[np.random.choice(legal_ids)]


def format_card_params(
    hand_cards: str = None,
    legage_cards: str = None,
    played_cards: str = None,
    trick_cards: str = None,
):
    if hand_cards != None and hand_cards != '':
        hand_cards = hand_cards.split(',')
        hand_cards = [card.strip() for card in hand_cards]
    else:
        hand_cards = None
    if legage_cards != None and legage_cards != '':
        legage_cards = legage_cards.split(',')
        legage_cards = [card.strip() for card in legage_cards]
    else:
        legage_cards = None
    if played_cards != None and played_cards != '':
        played_cards = played_cards.split(',')
        played_cards = [card.strip() for card in played_cards]
    else:
        played_cards = None
    if trick_cards != None and trick_cards != '':
        trick_cards = trick_cards.split(',')
        trick_cards = [card.strip() for card in trick_cards]
    else:
        trick_cards = None

    return hand_cards, legage_cards, played_cards, trick_cards


def to_obs(
    hand_cards: str = None,
    legage_cards: str = None,
    played_cards: str = None,
    winning_card: str = None,
    trick_cards: str = None,
    current_player_id: int = None,
    start_player_id: int = None,
    current_winner_id: int = None,
    is_raeuber: bool = False
) -> list:
    '''
    Observation Representation
        - [0-53] own cards
        - [54-107] cards playable by other players
        - [108-161] winner of trick
        - [162-215] first trick card
        - [216-269] second trick card
        - [270-323] third trick card
        - [324-335] Game Information
            - [324-327]: who is part of the team
            - [328-331]: who wins the current round
            - [332-335]: player who started the trick round
    '''
    obs: list = np.zeros((336), dtype=int)

    hand_cards_idx: list = []
    hand_cards_idx: list = [ACTION_SPACE[card] for card in hand_cards]
    obs[hand_cards_idx] = 1

    known_cards_idx: list = get_known_cards_idxs(
        hand_cards, legage_cards, played_cards, trick_cards, 54)
    obs[range(54, 108)] = 1
    obs[known_cards_idx] = 0

    if winning_card != '' and winning_card != None:
        obs[108 + ACTION_SPACE[winning_card]] = 1

    if trick_cards != None and len(trick_cards) > 0:
        for idx in range(len(trick_cards)):
            obs[162 + (idx*54) + ACTION_SPACE[trick_cards[idx]]] = 1

    encode_obs_game_info(obs, current_player_id, start_player_id,
                         current_winner_id, 324, is_raeuber)

    return obs


def get_known_cards_idxs(hand_cards, legage_cards, played_cards, trick_cards, start_idx=0) -> list:
    '''
        creates an array that contains all the card ids known by the player.
    '''
    known_cards = []

    if hand_cards is not None and hand_cards != '':
        known_cards.extend([card for card in hand_cards])
    if legage_cards is not None and legage_cards != '':
        known_cards.extend([card for card in legage_cards])
    if played_cards is not None and played_cards != '':
        known_cards.extend([card for card in played_cards])
    if trick_cards is not None and trick_cards != '':
        known_cards.extend([card for card in trick_cards])
    card_idxs = [start_idx + ACTION_SPACE[card] for card in known_cards]
    return card_idxs


def encode_obs_game_info(obs, current_player_id, start_player_id, current_winner_id, start_idx, is_raeuber=False) -> None:
    '''
        encodes the following player information
        * players in same team
        * winner player
        * player who started the round
    '''

    if is_raeuber:
        obs[start_idx+current_player_id] = 1
    else:
        if current_player_id == 0:
            obs[start_idx] = 1
        else:
            obs[[start_idx+1, start_idx+2, start_idx+3]] = 1

    if current_winner_id != None:
        obs[start_idx+4 + current_winner_id] = 1

    if start_player_id != None:
        obs[start_idx+8+start_player_id] = 1


def get_legal_actions(hand_cards, trick_cards) -> list:
    '''
        get the legal actions generated based on the current trick cards and the hand deck.
    '''

    legal_actions: list = []

    if trick_cards == None or len(trick_cards) == 0:
        return hand_cards

    target: str = trick_cards[0]
    _, target_suit = target.split('-')

    for card in hand_cards:
        _, suit = card.split('-')
        if suit == target_suit:
            legal_actions.append(str(card))

    if len(legal_actions) > 0:
        return legal_actions

    for card in hand_cards:
        _, suit = card.split('-')
        if suit == 'trump':
            legal_actions.append(str(card))

    if len(legal_actions) > 0:
        return legal_actions

    return hand_cards


def get_winning_card(trick: list) -> tuple:
    '''
        get the card and player and card that currently wins the trick
    '''
    if trick == None or len(trick) == 0:
        return None, None

    winning_card = trick[0]
    winning_player_idx = 0
    for i in range(1, len(trick)):
        if compare_trick_winner(winning_card, trick[i]) < 0:
            winning_card = trick[i]
            winning_player_idx = i

    return winning_card, winning_player_idx


def compare_trick_winner(target, compare_to_card) -> int:
    '''
        function for comparing individual cards

        Input:
            target: the currently winning card
            compare_to_card: the card the currently winning card is compared against
    '''
    target_rank, target_suit = target.split('-')
    compare_to_card_rank, compare_to_card_suit = compare_to_card.split('-')

    if target_suit == compare_to_card_suit:
        if target_suit == 'trump':
            return trump_card_ranks.index(target_rank) - trump_card_ranks.index(compare_to_card_rank)
        elif target_suit == 'd' or target_suit == 'h':
            return red_card_ranks.index(target_rank) - red_card_ranks.index(compare_to_card_rank)
        else:
            return black_card_ranks.index(target_rank) - black_card_ranks.index(compare_to_card_rank)
    elif compare_to_card_suit == 'trump':
        return -1
    else:
        return 1


def handle_get_request(
    mode: str = None,
    hand_cards: str = None,
    legage_cards: str = None,
    played_cards: str = None,
    trick_cards: str = None,
    current_player_id: int = None,
    round_starter_id: int = None,
    single_player_id: int = None,
    is_raeuber: bool = False
) -> ActionPrediciton:
    '''
        function that handles requests for each game mode
    '''

    handle_errors(mode, hand_cards, legage_cards, played_cards, trick_cards,
                  current_player_id, round_starter_id, single_player_id)

    action: str = predict(mode, hand_cards, legage_cards, played_cards,
                          trick_cards, current_player_id, round_starter_id, single_player_id, is_raeuber)

    return {'action': action}


# initialize
ACTION_SPACE, ACTION_LIST, MODEL_PATHS = init()
