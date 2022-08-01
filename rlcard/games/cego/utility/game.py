import numpy as np
import json
import os
from collections import OrderedDict

import rlcard

from rlcard.games.cego.card import CegoCard as Card

# Read required docs
ROOT_PATH = rlcard.__path__[0]

with open(os.path.join(ROOT_PATH, 'games/cego/jsondata/action_space.json'), 'r') as file:
    ACTION_SPACE = json.load(file, object_pairs_hook=OrderedDict)
    ACTION_LIST = list(ACTION_SPACE.keys())

with open(os.path.join(ROOT_PATH, 'games/cego/jsondata/high_cards.json'), 'r') as file:
    HIGH_CARDS = json.load(file, object_pairs_hook=OrderedDict)

with open(os.path.join(ROOT_PATH, 'games/cego/jsondata/low_cards.json'), 'r') as file:
    LOW_CARDS = json.load(file, object_pairs_hook=OrderedDict)


def init_deck() -> list:
    ''' initialize the cego deck'''

    deck = []
    card_info = Card.info

    for card in card_info["cards"]:
        rank, suit = card.split('-')
        deck.append(Card(suit, rank))

    return deck


def cards2list(cards) -> list:
    ''' convert cards to list of str'''

    cards_list = []

    for card in cards:
        cards_list.append(str(card))

    return cards_list


def cards2value(cards) -> float:
    ''' get the value of a list of cards'''

    value = 0
    for card in cards:
        value += card.get_value()

    return value


def get_tricks_played(tricks) -> list:
    ''' get all the cards out of the tricks list'''

    card_idxs = []
    for trick in tricks:
        for card in trick:
            card_idxs.append(ACTION_SPACE[str(card)])

    return card_idxs


def get_known_cards(hand, valued_cards, tricks_played, current_trick, start_idx=0) -> list:
    ''' get all cards that are already out of the game '''

    known_cards = []
    if hand is not None:
        known_cards.extend(hand)
    if valued_cards is not None:
        known_cards.extend(valued_cards)
    if tricks_played is not None:
        known_cards.extend([card for trick in tricks_played for card in trick])
    if current_trick is not None:
        known_cards.extend(current_trick)
    card_idxs = [start_idx + ACTION_SPACE[card] for card in known_cards]

    # print("cards:", card_idxs)
    return card_idxs


def get_cards_played(tricks_played, current_trick) -> list:
    ''' get all the cards out of the game list'''

    tricks = tricks_played[:]
    tricks.append(current_trick)

    # print("get_cards_played:",tricks)

    card_idxs = []
    for trick in tricks:
        for card in trick:
            card_idxs.append(ACTION_SPACE[str(card)])

    return card_idxs


def set_cego_player_deck(player, blind_cards) -> None:
    """ 
    this function is a helper function for selecting 
    the cards from the blind deck for the cego player

    the selection process is rule based:

        1. sort the blind and hand cards by rank descending
        2. throw away worst ranked card from blind
        3. take best 2 cards from hand
    """

    #  get hand cards
    hand_cards = player.hand
    player.og_hand_cards = hand_cards

    # sort cards
    sorted_blinds = sorted(blind_cards, reverse=True)
    sorted_hand = sorted(hand_cards, reverse=True)

    # generate new hand
    new_hand = sorted_blinds[:-1] + sorted_hand[0:2]

    # generate throw aways
    throw_away = sorted_hand[2:]
    throw_away.append(sorted_blinds[-1])

    # set player cards
    player.hand = new_hand
    player.valued_cards = throw_away


def set_observation(obs, plane, indexes):
    ''' set observation of a specific plane 

    Parameters:
        - obs (dict): the observation
        - plane (int): the plane to be set
        - indexes (list): the indexes to be set
    '''
    for index in indexes:
        obs[plane][index] = 1


def encode_observation_var1(state, is_raeuber=False):
    ''' the shape of this encoding is (336)

    Parameters:
        - state (dict): the state of the game

    Returns:
        - obs (list): the observation

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
    obs = np.zeros((336), dtype=int)

    hand_cards_idx: list = []

    hand_cards_idx = [ACTION_SPACE[card] for card in state['hand']]

    obs[hand_cards_idx] = 1

    known_cards_idxs = get_known_cards(
        state['hand'], state['valued_cards'], state['played_tricks'], state['trick'], 54)

    obs[range(54, 108)] = 1
    # unset all cards that are out of the game
    obs[known_cards_idxs] = 0

    if state['winner_card'] != 'None':
        obs[108 + ACTION_SPACE[state['winner_card']]] = 1

    for i in range(len(state["trick"])):
        obs[162 + (i*54) + ACTION_SPACE[state["trick"][i]]] = 1

    encode_obs_game_info(state, obs, 324, is_raeuber)

    return obs


def encode_observation_perfect_information(state, is_raeuber=False):
    ''' the shape of this encoding is (498)

    Parameters:
        - state (dict): the state of the game

    Returns:
        - obs (list): the observation

    Observation Representation
        - [0-53] cards player 0
        - [54-107] cards player 1
        - [108-161] cards player 2
        - [162-215] cards player 3
        - [216-269] out_of_game_cards
        - [270-323] winner of trick
        - [324-377] first trick card
        - [378-431] second trick card
        - [432-485] third trick card
        - [486-497] Game Information
            - [486-489]: who is part of the team
            - [490-493]: who wins the current round
            - [494-497]: player who started the trick round
    '''
    obs = np.zeros((498), dtype=int)

    for i in range(len(state['hand_cards'])):
        hand_cards_idx = [i*54 + ACTION_SPACE[card]
                          for card in state['hand_cards'][i]]
        obs[hand_cards_idx] = 1

    known_cards_idxs = get_known_cards(
        None, state['valued_cards'], state['played_tricks'], state['trick'], 216)

    obs[known_cards_idxs] = 1

    if state['winner_card'] != 'None':
        obs[270 + ACTION_SPACE[state['winner_card']]] = 1

    for i in range(len(state["trick"])):
        obs[324 + (i*54) + ACTION_SPACE[state["trick"][i]]] = 1

    encode_obs_game_info(state, obs, 486, is_raeuber)

    return obs


def encode_obs_game_info(state, obs, start_idx, is_raeuber=False):
    winner_idx = state['winner']
    start_player_idx = state['start_player']
    current_player_idx = state['current_player']

    if is_raeuber:
        obs[start_idx+current_player_idx] = 1
    else:
        if current_player_idx == 0:
            obs[start_idx] = 1
        else:
            obs[[start_idx+1, start_idx+2, start_idx+3]] = 1

    if winner_idx != None:
        obs[start_idx+4 + winner_idx] = 1

    if start_player_idx != None:
        obs[start_idx+8+start_player_idx] = 1


def valid_cego(cego_player_cards) -> bool:
    ''' This function checks if it would be valid for the 
    for the cego player to play cego.

    Parameters:
        - cego_player_cards (list): the cards of the cego player

    Returns:
        - valid (bool): The base is that the player has
            at least 15 points on his hand.
            - http://cegofreunde.jimdofree.com/taktik-und-tipps/
    '''

    value = cards2value(cego_player_cards)
    return value >= 15


def valid_ultimo(player_cards, strict=False) -> bool:
    ''' This function checks if it is possible 
    for the ultimo player to play ultimo.

    Parameters:
        - cego_player_cards (list): the cards of the cego player

    Returns:
        - valid (bool): Player has 1-trump on his hand
    '''
    has1_trump = "1-trump" in cards2list(player_cards)
    trumps = [card for card in player_cards if card.suit == 'trump']
    high_trumps = [card for card in trumps if card.suit == 'trump'
                   and (card.rank == 'gstiess' or int(card.rank) >= 17)]

    if strict:
        return has1_trump and len(trumps) >= 8 and len(high_trumps) >= 2
    else:
        return has1_trump


def valid_solo(solo_player_cards) -> bool:
    ''' This function checks if it would be valid for the 
    for the solo player to play solo.

    Parameters:
        - cego_player_cards (list): the cards of the cego player

    Returns:
        - valid (bool): if player has 7 trumps, two trumps >= 17 and 2 <= colors 
            or 8 trumps
            - https://www.cego-online.de/tl_files/documents/CegoSpielregelndef1301224mit%20Anhang.pdf
    '''

    trumps = [card for card in solo_player_cards if card.suit == 'trump']
    trumps_higher_17 = [card for card in trumps if card.suit == 'trump'
                        and (card.rank == 'gstiess' or int(card.rank) >= 17)]

    colors = set(
        [card.suit for card in solo_player_cards if card.suit != 'trump'])

    if len(trumps) >= 8:
        return True
    elif len(trumps) == 7 and len(trumps_higher_17) >= 2 and len(colors) <= 2:  # fixed heuristic!
        return True

    return False


def valid_solo_light(solo_player_cards):
    ''' This function checks if it would be valid for the 
    for the solo player to play solo.

    Parameters:
        - cego_player_cards (list): the cards of the cego player

    Returns:
        - valid (bool): if player has at least 7 trumps
            - https://www.cego-online.de/tl_files/documents/CegoSpielregelndef1301224mit%20Anhang.pdf
    '''
    trumps = [card for card in solo_player_cards if card.suit == 'trump']
    return len(trumps) >= 7


def valid_bettel(solo_player_cards) -> bool:
    valid_cards = []
    # print(LOW_CARDS)
    for card in solo_player_cards:
        if str(card) in LOW_CARDS:
            valid_cards.append(card)

    # check if all cards are low cards
    if len(valid_cards) != len(solo_player_cards):
        return False

    return True


def valid_piccolo(solo_player_cards):
    valid_cards = []
    for card in solo_player_cards:
        if str(card) in LOW_CARDS:
            valid_cards.append(card)

    # check if all cards but one are low cards
    if len(valid_cards)+1 != len(solo_player_cards):
        return False

    return True
