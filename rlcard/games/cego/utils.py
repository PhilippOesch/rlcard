from card import CegoCard as Card

import json

jsondata_path = 'rlcard/games/cego/jsondata/action_space.json'


def init_deck():
    deck = []
    card_info = Card.info

    for card in card_info["cards"]:
        rank, suit = card.split('-')
        deck.append(Card(suit, rank))

    return deck


def cards2list(cards):
    cards_list = []
    for card in cards:
        cards_list.append(str(card))
    return cards_list


def cards2value(cards):
    value = 0
    for card in cards:
        value += card.get_value()

    return value


""" this function is a helper function for selecting 
    the cards from the blind deck for the cego player"""


# def get_cego_player_deck(hand_cards, blind_cards):
#     """ the selection process is rule based:

#         1. sort the blind and hand cards by rank descending
#         2. throw away worst ranked card from blind
#         3. take best 2 cards from hand
#         """

#     sorted_blinds = sorted(blind_cards, reverse=True)
#     sorted_hand = sorted(hand_cards, reverse=True)

#     new_hand = sorted_blinds[:-1] + sorted_hand[0:2]

#     throw_away = sorted_hand[1:]
#     throw_away.append(sorted_blinds[-1])

#     return new_hand, throw_away

def set_cego_player_deck(player, blind_cards):
    """ the selection process is rule based:

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
