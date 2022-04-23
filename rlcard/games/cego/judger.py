from rlcard.games.cego.utils import cards2value


class CegoJudger:
    def __init__(self, np_random):
        self.np_random = np_random

    def receive_payoffs(self, payoffs, players, player_id, cards) -> list:
        points = cards2value(cards)

        payoffs = payoffs[:]

        # if player is cego player, only he receives the reward
        if players[player_id].is_cego_player:
            payoffs[player_id] += points

        # if player is not cego player, all players but the cego player receive the reward
        else:
            for i in range(len(players)):
                if not payoffs[i].is_cego_player:
                    payoffs[i] += points

        return payoffs
