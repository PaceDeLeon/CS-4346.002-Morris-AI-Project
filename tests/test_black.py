"""Black's move via the handout's color swap must be a legal Black move."""

import unittest

from game.board import WHITE, BLACK, swap_colors
from game.evaluation import static_estimation_opening, static_estimation_game
from game.minimax import minimax
from game.move_generator import OPENING, MIDGAME, generate_moves


CASES = [
    ("WWxBBBBxxWxxxxxxxxxxxxx", OPENING, static_estimation_opening),
    ("xxxxxBxWWWWWBBBBxxxxxxx", MIDGAME, static_estimation_game),
    ("WxWWxWWWWWBBBBBBBBxxxxx", MIDGAME, static_estimation_game),
]


class TestBlackColorSwap(unittest.TestCase):

    def test_swap_search_returns_legal_black_move(self):
        for board, phase, evaluate in CASES:
            with self.subTest(board=board):
                result = minimax(swap_colors(board), 2, WHITE, phase, evaluate)
                black_move = swap_colors(result.best_board)

                self.assertIn(black_move, generate_moves(board, BLACK, phase))


if __name__ == "__main__":
    unittest.main(verbosity=2)
