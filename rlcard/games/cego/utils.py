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

def get_other_cards(hand, valued_cards, tricks_played, current_trick) -> list:
    ''' get all cards that are still playable by the other players '''
    
    known_cards = []
    if hand is not None:
        known_cards.extend(hand)
    if valued_cards is not None:
        known_cards.extend(valued_cards)
    if tricks_played is not None:
        known_cards.extend([card for trick in tricks_played for card in trick])
    if current_trick is not None:
        known_cards.extend(current_trick)
    card_idxs= [ACTION_SPACE[card] for card in known_cards]
    state = np.ones((54), dtype=int)
    state[card_idxs] = 0
    return state


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
