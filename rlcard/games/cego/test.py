import unittest

import rlcard
from rlcard.agents import RandomAgent
from rlcard.games.cego.game_cego import CegoGameStandard as Game
from rlcard.games.cego.utils import cards2value, encode_observation_var1


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
                'seed': 12,
                'game_variant': "standard",
                'game_activate_heuristic': True,
                'game_judge_by_points': 0
            }
        )
        env.set_agents([
            RandomAgent(num_actions=env.num_actions) for _ in range(env.num_players)
        ])

        env.game.init_game()

        cego_card_value = cards2value(env.game.players[0].hand)
        expected = 15
        self.assertGreaterEqual(cego_card_value, expected)


if __name__ == '__main__':
    unittest.main()
