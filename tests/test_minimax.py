
"""Tests for the Morris AI minimax algorithm."""

import unittest

from game.board import WHITE, BLACK
from game.move_generator import OPENING, MIDGAME
from game.minimax import WIN_SCORE, minimax


class TestMinimax(unittest.TestCase):
    """Tests for minimax search behavior."""

    @staticmethod
    def evaluate_by_piece_position(board):
        """Temporary evaluator that scores a board by a new piece's index."""
        for index, piece in enumerate(board):
            if piece in (WHITE, BLACK):
                # The starting piece is at index zero.
                # Return the index of the other piece.
                if index != 0:
                    return index

        return 0

    def test_white_maximizes_score(self):
        """White should choose the move with the highest score."""
        board = WHITE + ("x" * 22)

        result = minimax(
            board=board,
            depth=1,
            player=WHITE,
            phase=OPENING,
            evaluate=self.evaluate_by_piece_position,
        )

        self.assertEqual(result.best_board[22], WHITE)
        self.assertEqual(result.estimate, 22)
        self.assertEqual(result.positions_evaluated, 22)

    def test_black_minimizes_score(self):
        """Black should choose the move with the lowest score."""
        board = BLACK + ("x" * 22)

        result = minimax(
            board=board,
            depth=1,
            player=BLACK,
            phase=OPENING,
            evaluate=self.evaluate_by_piece_position,
        )

        self.assertEqual(result.best_board[1], BLACK)
        self.assertEqual(result.estimate, 1)
        self.assertEqual(result.positions_evaluated, 22)

    def test_depth_one_evaluates_each_possible_move(self):
        """Depth one should evaluate every legal child position."""
        board = WHITE + ("x" * 22)

        result = minimax(
            board=board,
            depth=1,
            player=WHITE,
            phase=OPENING,
            evaluate=lambda position: 0,
        )

        self.assertEqual(result.positions_evaluated, 22)

    def test_depth_two_evaluates_leaf_positions(self):
        """Depth two should search two moves before evaluation."""
        board = WHITE + ("x" * 22)

        result = minimax(
            board=board,
            depth=2,
            player=WHITE,
            phase=OPENING,
            evaluate=lambda position: 0,
        )

        # White has 22 choices; Black then has 21 choices.
        self.assertEqual(result.positions_evaluated, 22 * 21)

    def test_terminal_position_returns_win_score(self):
        """A position with two Black pieces is a win for White."""
        board = "WWWBB" + ("x" * 18)

        result = minimax(
            board=board,
            depth=1,
            player=WHITE,
            phase=MIDGAME,
            evaluate=lambda position: 0,
        )

        self.assertEqual(result.best_board, board)
        self.assertEqual(result.estimate, WIN_SCORE)
        self.assertEqual(result.positions_evaluated, 0)

    def test_depth_must_be_positive(self):
        """Depth zero is invalid for a root move search."""
        board = "x" * 23

        with self.assertRaises(ValueError):
            minimax(
                board=board,
                depth=0,
                player=WHITE,
                phase=OPENING,
                evaluate=lambda position: 0,
            )

    def test_invalid_phase_is_rejected(self):
        """An unknown phase should raise ValueError."""
        board = "x" * 23

        with self.assertRaises(ValueError):
            minimax(
                board=board,
                depth=1,
                player=WHITE,
                phase="invalid",
                evaluate=lambda position: 0,
            )


if __name__ == "__main__":
    unittest.main()
