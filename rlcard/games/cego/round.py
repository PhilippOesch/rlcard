from utils import cards2list


class CegoRound:
    def __init__(self, dealer, np_random):
        self.np_random = np_random
        self.dealer = dealer
        self.current_player = 0
        self.num_players = 4  # there are always 4 players in cego
        self.trick = []
        self.played_tricks = [],
        self.is_over = False
        self.winner = None
        self.trick_round = 0
        self.game_round = 0

    def proceed_round(self, players, action):
        # if action
        # TODO: implement this function
        pass

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
