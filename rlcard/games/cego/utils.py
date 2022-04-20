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


def compare_trick_winner(card1, card2):
    black_cards_ranks, red_card_ranks, trump_card_ranks = Card.split_ranks()

    if card1.suit == card2.suit:
        if card1.suit == "trump":
            return trump_card_ranks.index(card1.rank) - trump_card_ranks.index(card2.rank)
        elif card1.suit == "d" or card1.suit == "h":
            return red_card_ranks.index(card1.rank) - red_card_ranks.index(card2.rank)
        else:
            return black_cards_ranks.index(card1.rank) - black_cards_ranks.index(card2.rank)
    elif card2.suit == "trump":
        return -1
    else:
        return 1


def compare_card_rank(card1, card2):
    black_cards_ranks, red_card_ranks, trump_card_ranks = Card.split_ranks()

    if card1.suit == card2.suit:
        if card1.suit == "trump":
            return trump_card_ranks.index(card1.rank) - trump_card_ranks.index(card2.rank)
        elif card1.suit == "d" or card1.suit == "h":
            return red_card_ranks.index(card1.rank) - red_card_ranks.index(card2.rank)
        else:
            return black_cards_ranks.index(card1.rank) - black_cards_ranks.index(card2.rank)
    else:
        return Card.info["ranks"].index(card1.rank) - Card.info["ranks"].index(card2.rank)


def sort_cards_by_rank_ascending(cards):
    # TODO
    pass


def get_cego_player_deck(hand_cards, blind_cards):
    # TODO
    pass
