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
        values += card.get_value()

    return value


def compare_card(best, compare_to_card):
    # TODO
    pass
