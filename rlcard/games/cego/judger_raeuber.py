from rlcard.games.cego.utils import cards2value
from rlcard.games.cego import Judger


class CegoJudgerRaeuber(Judger):
    '''This is the class for the räuber variant 
    to judge the winner of a round and the points of each player

    inherits from:
        - Judger
    '''

    def __init__(self, np_random):
        self.np_random = np_random

    def update_points(self, points, players, winner_player_id, trick_cards) -> list:

        new_points = cards2value(trick_cards)

        # if player is cego player, only he receives the reward
        points[winner_player_id] += new_points

        return points

    def judge_game_zero_to_one(self, points) -> list:
        max_points = max(points)
        rewards = [1, 1, 1, 1]

        rewards[points.index(max_points)] = 0
        return rewards

    def judge_game_minusone_to_one(self, points) -> list:
        max_points = max(points)
        rewards = [1, 1, 1, 1]
        print(points)
        rewards[points.index(max_points)] = -1
        return rewards