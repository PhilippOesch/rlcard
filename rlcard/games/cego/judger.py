from rlcard.games.cego.utils import cards2value


class CegoJudger:
    def __init__(self, np_random):
        self.np_random = np_random

    def receive_points(self, points, players, player_id, cards) -> list:
        new_points = cards2value(cards)

        # payoffs = payoffs.copy()

        # if player is cego player, only he receives the reward
        if players[player_id].is_cego_player:
            points[player_id] += new_points

        # if player is not cego player, all players but the cego player receive the reward
        else:
            for i in range(len(players)):
                if not players[i].is_cego_player:
                    points[i] += new_points

        return points

    def judge_game(self, points) -> list:
        if points[0] > points[1]:
            return [points[0], 0, 0, 0]
        else:
            return [0, points[1], points[1], points[1]]
