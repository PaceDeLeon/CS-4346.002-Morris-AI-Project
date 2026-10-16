"""Checks for the improved static estimation."""

import unittest

from game.evaluation import static_estimation_game
from game.improved_evaluation import (
    WIN,
    improved_estimation_game,
    improved_estimation_opening,
)


class TestImprovedEvaluation(unittest.TestCase):

    def test_two_black_pieces_is_white_win(self):
        self.assertEqual(improved_estimation_game("WWWBBxxxxxxxxxxxxxxxxxx"), WIN)

    def test_white_with_no_moves_is_loss(self):
        # White a0, d0, g0, b1 (4 pieces, so no hopping) are boxed in by
        # Black on d1, f1, c2, a3, b3, g3.
        board = "WWWWBBBxBBxxxB" + "x" * 9

        self.assertEqual(improved_estimation_game(board), -WIN)
        # The handout version does not detect this.
        self.assertNotEqual(static_estimation_game(board), -WIN)

    def test_opening_counts_mill_threats(self):
        # Same material, but White has two pieces in line with the third empty.
        # White a0, d0 (threat on g0) vs. a0, c4 (no shared line).
        # Black b3, g6 in both, with no shared line either.
        def board(*white):
            cells = ["x"] * 23
            for i in white:
                cells[i] = "W"
            cells[9] = cells[22] = "B"
            return "".join(cells)

        threat = board(0, 1)
        scattered = board(0, 14)

        self.assertGreater(
            improved_estimation_opening(threat),
            improved_estimation_opening(scattered),
        )

    def test_non_terminal_stays_inside_win_scores(self):
        board = "WWWWWWWWWBBBxxxxxxxxxxx"
        score = improved_estimation_game(board)

        self.assertLess(abs(score), WIN)


if __name__ == "__main__":
    unittest.main(verbosity=2)
