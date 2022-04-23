from card import CegoCard as Card
from utils import cards2list


""" A Round in Cego equals one trick """


class CegoRound:
    def __init__(self, dealer, np_random, starting_player=0):
        self.np_random = np_random
        self.dealer = dealer
        self.starting_player = starting_player
        self.current_player = self.starting_player
        self.num_players = 4  # there are always 4 players in cego
        self.trick = []
        self.target = None
        self.is_over = False
        self.winner_idx = None  # index of current winning player

    def proceed_round(self, players, action):
        """ keep the round running """

        # get current player
        player = players[self.current_player]

        # get and remove card from player hand
        remove_index = None
        for index, card in enumerate(player.hand):
            if card.str == action:
                remove_index = index
                break

        card = player.hand.pop(remove_index)

        # if no card has been player, the first card is the target
        if len(self.trick) == 0:
            self.target = card
            self.winner_idx = self.current_player
        else:
            current_winner = Card.compare_trick_winner(self.target, card)
            if current_winner < 0:
                self.target = card
                self.winner_idx = self.current_player

        self.trick.append(card)

        # if the trick is full, this round is over
        if len(self.trick) == self.num_players:
            self.is_over = True

        self.current_player = (self.current_player + 1) % self.num_players

    # get legal actions for current player
    def get_legal_actions(self, players, player_id):
        hand = players[player_id].hand  # get hand of current player
        legal_actions = []

        # if no card has been player, all cards are legal
        if len(self.trick) == 0:
            legal_actions = cards2list(hand)
            return legal_actions

        target = self.trick[0]  # get the first card in trick

        # if the cards fit the suit, they must be played
        for card in hand:
            if card.suit == target.suit:
                legal_actions.append(card.str)

        if len(legal_actions) == 0:
            return legal_actions

        # if no card of the same suit is on the hand, a trump card must be played
        for card in hand:
            if card.type == 'trump':
                legal_actions.append(card.str)

        if len(legal_actions) == 0:
            return legal_actions

        # else, all cards are legal
        return cards2list(hand)

    def get_state(self, players, player_id):
        state = {}
        player = players[player_id]
        state['hand'] = cards2list(player.hand)
        state['current_trick'] = cards2list(self.trick)
        state['played_tricks'] = self.played_tricks
        state['legal_actions'] = self.get_legal_actions(players, player_id)
        return state
