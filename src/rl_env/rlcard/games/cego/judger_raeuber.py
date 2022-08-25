from rlcard.games.cego.utility.game import cards2value
from rlcard.games.cego import Judger


class CegoJudgerRaeuber(Judger):
    ''' The standard class to judge the winner of a round and the points of each player

    inherits from:
        - Judger
    '''

    def __init__(self, np_random):
        self.np_random = np_random

    def update_points(self, points, players, winner_player_id, trick_cards) -> list:
        new_points = cards2value(trick_cards)
        points[winner_player_id] += new_points

        return points

    def judge_game_zero_to_one(self, points) -> list:
        payoff = [1, 1, 1, 1]
        # returns idx with most points
        index_max = max(range(len(points)), key=points.__getitem__)

        payoff[index_max] = 0
        return payoff

    def judge_game_minusone_to_one(self, points) -> list:
        payoff = [1, 1, 1, 1]
        # returns idx with most points
        index_max = max(range(len(points)), key=points.__getitem__)

        payoff[index_max] = -1
        return payoff
