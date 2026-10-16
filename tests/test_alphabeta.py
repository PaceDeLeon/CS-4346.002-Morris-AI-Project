"""Alpha-beta must match minimax and never evaluate more positions."""

import unittest

from game.alphabeta import alphabeta
from game.board import WHITE, BLACK
from game.evaluation import static_estimation_opening, static_estimation_game
from game.minimax import minimax
from game.move_generator import OPENING, MIDGAME


CASES = [
    # (board, phase, evaluate)
    ("xxxxxxxxxxxxxxxxxxxxxxx", OPENING, static_estimation_opening),
    ("WWxBBBBxxWxxxxxxxxxxxxx", OPENING, static_estimation_opening),
    ("xxxxxBxWWWWWBBBBxxxxxxx", MIDGAME, static_estimation_game),
    ("WxWWxWWWWWBBBBBBBBxxxxx", MIDGAME, static_estimation_game),
    ("WxxWxxxBxxBxxxBxxxxxWxW", MIDGAME, static_estimation_game),
]


class TestAlphaBeta(unittest.TestCase):

    def test_matches_minimax(self):
        for board, phase, evaluate in CASES:
            for player in (WHITE, BLACK):
                for depth in (1, 2, 3):
                    with self.subTest(board=board, player=player, depth=depth):
                        mm = minimax(board, depth, player, phase, evaluate)
                        ab = alphabeta(board, depth, player, phase, evaluate)

                        self.assertEqual(ab.best_board, mm.best_board)
                        self.assertEqual(ab.estimate, mm.estimate)
                        self.assertLessEqual(
                            ab.positions_evaluated, mm.positions_evaluated
                        )

    def test_prunes_on_known_boards(self):
        for board, phase, evaluate in CASES[1:3]:
            with self.subTest(board=board):
                mm = minimax(board, 3, WHITE, phase, evaluate)
                ab = alphabeta(board, 3, WHITE, phase, evaluate)

                self.assertLess(ab.positions_evaluated, mm.positions_evaluated)


if __name__ == "__main__":
    unittest.main(verbosity=2)
