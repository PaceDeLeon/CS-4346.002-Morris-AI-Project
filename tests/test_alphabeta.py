"""Alpha-beta must match minimax and never evaluate more positions."""

import unittest

from game.alphabeta import alphabeta
from game.board import WHITE, BLACK
from game.evaluation import static_estimation_opening, static_estimation_game
from game.minimax import minimax
from game.move_generator import OPENING, MIDGAME, generate_moves


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


    def test_move_number_matches_fixed_phase_away_from_boundary(self):
        board = "WWxBBBBxxWxxxxxxxxxxxxx"
        evaluate = static_estimation_opening

        self.assertEqual(
            alphabeta(board, 3, WHITE, OPENING, evaluate, move_number=1),
            alphabeta(board, 3, WHITE, OPENING, evaluate),
        )

        board = "xxxxxBxWWWWWBBBBxxxxxxx"
        evaluate = static_estimation_game

        self.assertEqual(
            alphabeta(board, 3, WHITE, MIDGAME, evaluate, move_number=19),
            alphabeta(board, 3, WHITE, MIDGAME, evaluate),
        )

    def test_move_number_switches_to_midgame_after_move_18(self):
        # Black places its ninth piece at move 18; White then moves pieces.
        board = "WBWWxBBxWBBxxWBxxWBWWxx"
        leaves = []

        def record(position):
            leaves.append(position)
            return position.count(WHITE)

        result = alphabeta(board, 2, BLACK, OPENING, record, move_number=18)

        placements = generate_moves(board, BLACK, OPENING)
        white_moves = {
            move
            for child in placements
            for move in generate_moves(child, WHITE, MIDGAME)
        }

        self.assertIn(result.best_board, placements)
        self.assertTrue(leaves)
        for leaf in leaves:
            self.assertIn(leaf, white_moves)


if __name__ == "__main__":
    unittest.main(verbosity=2)
