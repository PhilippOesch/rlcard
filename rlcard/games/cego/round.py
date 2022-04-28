from rlcard.games.cego.card import CegoCard as Card
from rlcard.games.cego.utils import cards2list


""" A Round in Cego equals one trick """


class CegoRound:
    def __init__(self, np_random):
        self.np_random = np_random
        self.num_players = 4  # there are always 4 players in cego# index of current winning player

    def start_new_round(self, starting_player_idx) -> None:
        self.current_player_idx = starting_player_idx
        self.starting_player_idx = starting_player_idx
        self.trick = []
        self.winner_card = None
        self.target = None
        self.is_over = False
        self.winner_idx = None

    def proceed_round(self, players, action) -> None:
        """ keep the round running """

        # print("cards in trick", len(self.trick))

        """ Logs for Testing """
        # print("current player: ", self.current_player_idx)
        # print("Player Cards: ", cards2list(
        #     players[self.current_player_idx].hand))
        # print("Target Card: ", str(self.target))
        # print("Played Card: ", action)

        # get current player
        player = players[self.current_player_idx]

        # get and remove card from player hand
        remove_index = None
        for index, card in enumerate(player.hand):
            if str(card) == action:
                remove_index = index
                break

        card = player.hand.pop(remove_index)

        # if no card has been player, the first card is the target
        if len(self.trick) == 0:
            self.winner_card = card
            self.winner_idx = self.current_player_idx
        else:
            current_winner = Card.compare_trick_winner(self.winner_card, card)
            if current_winner < 0:
                self.winner_card = card
                self.winner_idx = self.current_player_idx

        self.trick.append(card)

        # if the trick is full, this round is over
        if len(self.trick) == self.num_players:
            self.is_over = True

        self.current_player_idx = (
            self.current_player_idx + 1) % self.num_players

    # get legal actions for current player
    def get_legal_actions(self, player) -> list:
        hand = player.hand  # get hand of current player
        legal_actions = []

        # if no card has been player, all cards are legal
        if len(self.trick) == 0:
            legal_actions = cards2list(hand)
            return legal_actions

        self.target = self.trick[0]  # get the first card in trick

        # if the cards fit the suit, they must be played
        for card in hand:
            if card.suit == self.target.suit:
                legal_actions.append(str(card))

        if len(legal_actions) > 0:
            return legal_actions

        # if no card of the same suit is on the hand, a trump card must be played
        for card in hand:
            if card.suit == 'trump':
                legal_actions.append(str(card))

        if len(legal_actions) > 0:
            return legal_actions

        # else, all other cards are legal
        return cards2list(hand)

    def get_state(self, player) -> dict:
        state = {}
        state['hand'] = cards2list(player.hand)
        state['trick'] = cards2list(self.trick)
        state['target'] = str(self.target) if str(
            self.target) is not None else None
        state['winner_card'] = str(self.winner_card) if str(
            self.winner_card) is not None else None
        state['winner'] = self.winner_idx
        state['valued_cards'] = cards2list(
            player.valued_cards) if player.is_cego_player else []
        state['legal_actions'] = self.get_legal_actions(player)
        state['start_player'] = self.starting_player_idx
        return state
