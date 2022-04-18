from utils import cards2value


class CegoJudger:
    @staticmethod
    def judge_payoffs(players):
        payoffs = []
        for player in players:
            payoffs.append(player.points)

        return payoffs

    @staticmethod
    def receive_payoffs(players, player_id, cards):
        points = cards2value(cards)

        payoffs = []
        # setup payoffs
        for player in players:
            payoffs.append(player.points)

        # if player is cego player, only he receives the reward
        if player[player_id].is_cego_player:
            players[player_id].points += points

        # if player is not cego player, all players but the cego player receive the reward
        else:
            for i in range(len(players)):
                if not players[i].is_cego_player:
                    players[i].points += points

        return payoffs

    @staticmethod
    def get_round_winner(players, start_player_id, trick_cards):
        target = trick_cards[0]

        for i in range(1, len(players)):
            # TODO
            pass
