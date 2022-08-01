import unittest

import rlcard
from rlcard.agents import RandomAgent
from rlcard.games.cego.game_cego import CegoGameStandard as Game
from rlcard.games.cego.utility.game import cards2value, cards2list, LOW_CARDS, HIGH_CARDS


def check_if_all_cards_are_unique(players: list) -> bool:
    ''' Check if all players have unique cards

    Parameters:
        - players (list): list of players
    '''

    all_cards_set = set()
    count = 0

    count += len(players[0].valued_cards)
    for card in players[0].valued_cards:
        all_cards_set.add(str(card))

    for player in players:
        count += len(player.hand)
        for card in player.hand:
            all_cards_set.add(str(card))

    if len(all_cards_set) == count:
        return True
    else:
        return False


class TestCardUniqueness(unittest.TestCase):
    def test_card_uniqueness(self):
        game = Game()
        game.init_game()

        self.assertTrue(check_if_all_cards_are_unique(game.players))


class TestStartPayoffs(unittest.TestCase):
    def test_start_payoffs(self):
        game = Game()
        game.init_game()

        expected_payoffs = [
            cards2value(game.players[0].valued_cards), 0, 0, 0
        ]

        self.assertEqual(game.points, expected_payoffs)


class TestRewardRange(unittest.TestCase):
    def test_obs_space(self):
        env = rlcard.make(
            "cego",
            config={
                'seed': 12,
                'game_variant': "standard",
                'game_activate_heuristic': True,
                'game_judge_by_points': 0
            }
        )

        env.set_agents([
            RandomAgent(num_actions=env.num_actions) for _ in range(env.num_players)
        ])

        _, payoffs = env.run(is_training=False)

        break_even_point0 = payoffs[0] + payoffs[1]
        break_even_point1 = payoffs[0] + payoffs[2]
        break_even_point2 = payoffs[0] + payoffs[3]

        self.assertEqual(79, break_even_point0)
        self.assertEqual(79, break_even_point1)
        self.assertEqual(79, break_even_point2)


class TestObsSpace(unittest.TestCase):
    def test_reward_range(self):
        env = rlcard.make(
            "cego",
            config={
                'seed': 12,
                'game_variant': "standard",
                'game_activate_heuristic': True,
                'game_judge_by_points': 0
            }
        )
        expected = [[336], [336], [336], [336]]

        self.assertEqual(env.state_shape, expected)


class TestNumSteps(unittest.TestCase):
    def test_reward_range(self):
        env = rlcard.make(
            "cego",
            config={
                'seed': 12,
                'game_variant': "standard",
                'game_activate_heuristic': True,
                'game_judge_by_points': 0
            }
        )
        env.set_agents([
            RandomAgent(num_actions=env.num_actions) for _ in range(env.num_players)
        ])

        trajectory, _ = env.run(is_training=False)
        num_actions = len(trajectory[0][0]['action_record'])

        self.assertEqual(44, num_actions)


class TestObsStateStartCards(unittest.TestCase):
    def test_obs_state_start_cards(self):
        env = rlcard.make(
            "cego",
            config={
                'seed': 12,
                'game_variant': "standard",
                'game_activate_heuristic': True,
                'game_judge_by_points': 0
            }
        )
        env.set_agents([
            RandomAgent(num_actions=env.num_actions) for _ in range(env.num_players)
        ])

        trajectory, _ = env.run(is_training=False)
        expected = 11  # num cards per player
        end_cards_0 = sum(trajectory[0][0]['obs'][:54])
        start_cards_1 = sum(trajectory[1][0]['obs'][:54])
        start_cards_2 = sum(trajectory[2][0]['obs'][:54])
        start_cards_3 = sum(trajectory[3][0]['obs'][:54])

        self.assertEqual(expected, end_cards_0)
        self.assertEqual(expected, start_cards_1)
        self.assertEqual(expected, start_cards_2)
        self.assertEqual(expected, start_cards_3)


class TestObsStateEndCards(unittest.TestCase):
    def test_obs_state_start_cards(self):
        env = rlcard.make(
            "cego",
            config={
                'seed': 12,
                'game_variant': "standard",
                'game_activate_heuristic': True,
                'game_judge_by_points': 0
            }
        )
        env.set_agents([
            RandomAgent(num_actions=env.num_actions) for _ in range(env.num_players)
        ])

        trajectory, _ = env.run(is_training=False)
        expected = 0  # num cards per player
        end_cards_0 = sum(trajectory[0][-1]['obs'][:54])
        end_cards_1 = sum(trajectory[1][-1]['obs'][:54])
        end_cards_2 = sum(trajectory[2][-1]['obs'][:54])
        end_cards_3 = sum(trajectory[3][-1]['obs'][:54])

        # print(trajectory[0][-1]['obs'][:54])

        self.assertEqual(expected, end_cards_0)
        self.assertEqual(expected, end_cards_1)
        self.assertEqual(expected, end_cards_2)
        self.assertEqual(expected, end_cards_3)


class TestObsStateCegoKnowledgeStart(unittest.TestCase):
    def test_obs_state_cego_knowledge_start(self):
        env = rlcard.make(
            "cego",
            config={
                'seed': 12,
                'game_variant': "standard",
                'game_activate_heuristic': True,
                'game_judge_by_points': 0
            }
        )
        env.set_agents([
            RandomAgent(num_actions=env.num_actions) for _ in range(env.num_players)
        ])

        trajectory, _ = env.run(is_training=False)
        # cards the cego players knows can be played (54-21)
        expected_cego_0 = 33
        # cards the other players know can be played (54-11)
        expected_other_1 = 42
        expected_other_2 = 41
        expected_other_3 = 40

        cards_0 = sum(trajectory[0][0]['obs'][54:108])
        cards_1 = sum(trajectory[1][0]['obs'][54:108])
        cards_2 = sum(trajectory[2][0]['obs'][54:108])
        cards_3 = sum(trajectory[3][0]['obs'][54:108])

        self.assertEqual(expected_cego_0, cards_0)
        self.assertEqual(expected_other_1, cards_1)
        self.assertEqual(expected_other_2, cards_2)
        self.assertEqual(expected_other_3, cards_3)


class TestObsStateCegoKnowledgeEnd(unittest.TestCase):
    def test_obs_state_cego_knowledge_end(self):
        env = rlcard.make(
            "cego",
            config={
                'seed': 15,
                'game_variant': "standard",
                'game_activate_heuristic': True,
                'game_judge_by_points': 0
            }
        )
        env.set_agents([
            RandomAgent(num_actions=env.num_actions) for _ in range(env.num_players)
        ])

        trajectory, _ = env.run(is_training=False)
        expected_cego = 0  # cards the cego player knows (54-21)
        expected_other = 10  # cards the other players know (54-11)

        cards_0 = sum(trajectory[0][-1]['obs'][54:108])
        cards_1 = sum(trajectory[1][-1]['obs'][54:108])
        cards_2 = sum(trajectory[2][-1]['obs'][54:108])
        cards_3 = sum(trajectory[3][-1]['obs'][54:108])

        self.assertEqual(expected_cego, cards_0)
        self.assertEqual(expected_other, cards_1)
        self.assertEqual(expected_other, cards_2)
        self.assertEqual(expected_other, cards_3)


class TestObsStateCegoHeuristic(unittest.TestCase):
    def test_obs_state_cego_knowledge_end(self):
        env = rlcard.make(
            "cego",
            config={
                'game_variant': "standard",
                'game_activate_heuristic': True,
                'game_judge_by_points': 0
            }
        )
        env.set_agents([
            RandomAgent(num_actions=env.num_actions) for _ in range(env.num_players)
        ])

        env.game.init_game()

        cego_card_value = cards2value(env.game.players[0].og_hand_cards)
        expected = 15
        self.assertGreaterEqual(cego_card_value, expected)


class TestValidSoloInfoState(unittest.TestCase):
    def test_valid_solo_infostate(self):
        env = rlcard.make(
            "cego",
            config={
                'seed': 12,
                'game_variant': "solo",
                'game_activate_heuristic': True,
                'game_judge_by_points': 0
            }
        )
        env.set_agents([
            RandomAgent(num_actions=env.num_actions) for _ in range(env.num_players)
        ])

        trajectory, _ = env.run(is_training=False)
        # cards the cego players knows can be played (54-21)
        expected_cego_0 = 43
        # cards the other players know can be played (54-11)
        expected_other_1 = 42
        expected_other_2 = 41
        expected_other_3 = 40

        cards_0 = sum(trajectory[0][0]['obs'][54:108])
        cards_1 = sum(trajectory[1][0]['obs'][54:108])
        cards_2 = sum(trajectory[2][0]['obs'][54:108])
        cards_3 = sum(trajectory[3][0]['obs'][54:108])

        self.assertEqual(expected_cego_0, cards_0)
        self.assertEqual(expected_other_1, cards_1)
        self.assertEqual(expected_other_2, cards_2)
        self.assertEqual(expected_other_3, cards_3)


class TestUltimoPlayerHasGeiss(unittest.TestCase):
    def test_ultimo_logic(self):
        env = rlcard.make(
            "cego",
            config={
                'game_variant': "ultimo",
                'game_activate_heuristic': False,
                'game_judge_by_points': 0
            }
        )

        env.game.init_game()
        player_0_cards = cards2list(env.game.players[0].hand)
        contains_geiss = "1-trump" in player_0_cards
        self.assertEqual(True, contains_geiss)


class TestRaeuberPoints(unittest.TestCase):
    def test_raueber_points(self):
        env = rlcard.make(
            "cego",
            config={
                'game_variant': "raeuber",
                'game_activate_heuristic': False,
                'game_judge_by_points': 0
            }
        )
        env.set_agents([
            RandomAgent(num_actions=env.num_actions) for _ in range(env.num_players)
        ])

        trajectory, _ = env.run(is_training=False)
        full_points = sum(env.game.points) + cards2value(env.game.blind_cards)

        self.assertEqual(79, full_points)


class TestRaeuberTeamState(unittest.TestCase):
    def test_raueber_team_state(self):
        env = rlcard.make(
            "cego",
            config={
                'game_variant': "raeuber",
                'game_activate_heuristic': False,
                'game_judge_by_points': 0
            }
        )
        env.set_agents([
            RandomAgent(num_actions=env.num_actions) for _ in range(env.num_players)
        ])

        trajectory, _ = env.run(is_training=False)
        team_info_0 = list(trajectory[0][0]['obs'][324:328])
        team_info_1 = list(trajectory[1][0]['obs'][324:328])
        team_info_2 = list(trajectory[2][0]['obs'][324:328])
        team_info_3 = list(trajectory[3][0]['obs'][324:328])

        self.assertEqual([1, 0, 0, 0], team_info_0)
        self.assertEqual([0, 1, 0, 0], team_info_1)
        self.assertEqual([0, 0, 1, 0], team_info_2)
        self.assertEqual([0, 0, 0, 1], team_info_3)


class TestUltimoHeuristicStrict(unittest.TestCase):
    def test_ultimo_heuristic_strict(self):
        env = rlcard.make(
            "cego",
            config={
                'game_variant': "ultimo",
                'game_activate_heuristic': True,
                'game_judge_by_points': 0
            }
        )

        env.game.init_game()
        player_0_cards = cards2list(env.game.players[0].hand)
        contains_geiss = "1-trump" in player_0_cards
        trumps = [card for card in player_0_cards if card.split('-')[
            1] == 'trump']
        high_trumps = [card for card in trumps if card.split('-')[1] == 'trump'
                       and (card.split('-')[0] == 'gstiess' or int(card.split('-')[0]) >= 17)]

        self.assertTrue(contains_geiss)
        self.assertGreaterEqual(len(trumps), 8)
        self.assertGreaterEqual(len(high_trumps), 2)


class TestPiccoloPoints(unittest.TestCase):
    def test_piccolo_points(self):
        env = rlcard.make(
            "cego",
            config={
                'game_variant': "piccolo",
                'game_activate_heuristic': True,
                'game_judge_by_points': 0,
                'game_analysis_mode': True
            }
        )
        env.set_agents([
            RandomAgent(num_actions=env.num_actions) for _ in range(env.num_players)
        ])

        _, payoffs, state = env.run(is_training=False)
        winning_players = state['winning_player_history']
        player_0_wins = [id for id in winning_players if id == 0]
        count_player_wins = len(player_0_wins)

        if count_player_wins == 1:
            self.assertEqual(1, payoffs[0])
        else:
            self.assertNotEqual(1, payoffs[0])


class TestBettelPoints(unittest.TestCase):
    def test_piccolo_points(self):
        env = rlcard.make(
            "cego",
            config={
                'game_variant': "bettel",
                'game_activate_heuristic': True,
                'game_judge_by_points': 0,
                'game_analysis_mode': True
            }
        )
        env.set_agents([
            RandomAgent(num_actions=env.num_actions) for _ in range(env.num_players)
        ])

        _, payoffs, state = env.run(is_training=False)
        winning_players = state['winning_player_history']
        player_0_wins = [id for id in winning_players if id == 0]
        count_player_wins = len(player_0_wins)

        if count_player_wins == 0:
            self.assertEqual(1, payoffs[0])
        else:
            self.assertNotEqual(1, payoffs[0])


class TestBettelHeursitic(unittest.TestCase):
    def test_bettel_heuristic(self):
        env = rlcard.make(
            "cego",
            config={
                'game_variant': "bettel",
                'game_activate_heuristic': True,
                'game_judge_by_points': 0,
                'game_analysis_mode': True
            }
        )
        env.game.init_game()
        player_0_cards = env.game.players[0].hand

        valid_cards = []
        for card in player_0_cards:
            if str(card) in LOW_CARDS:
                valid_cards.append(card)

        self.assertEqual(len(valid_cards), 11)


class TestPiccoloHeursitic(unittest.TestCase):
    def test_piccolo_heuristic(self):
        env = rlcard.make(
            "cego",
            config={
                'game_variant': "piccolo",
                'game_activate_heuristic': True,
                'game_judge_by_points': 0,
                'game_analysis_mode': True
            }
        )
        env.game.init_game()
        player_0_cards = env.game.players[0].hand

        valid_cards = []
        high_cards = []
        for card in player_0_cards:
            if str(card) in LOW_CARDS:
                valid_cards.append(card)
            else:
                high_cards.append(card)

        self.assertEqual(len(high_cards), 1)
        self.assertTrue(str(high_cards[0]) in HIGH_CARDS)
        self.assertEqual(len(valid_cards), 10)


if __name__ == '__main__':
    unittest.main()
