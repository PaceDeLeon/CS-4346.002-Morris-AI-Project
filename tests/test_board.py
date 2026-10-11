import unittest

from game.board import (
    BOARD_SIZE,
    WHITE,
    BLACK,
    EMPTY,
    NEIGHBORS,
    MILLS,
    validate_board,
    validate_player,
    neighbors,
    mills_at,
    close_mill,
    count_pieces,
    empty_locations,
)


class TestBoard(unittest.TestCase):

    def test_board_size_and_symbols(self):
        board = "x" * 23
        validate_board(board)

        self.assertEqual(BOARD_SIZE, 23)
        self.assertEqual(WHITE, "W")
        self.assertEqual(BLACK, "B")
        self.assertEqual(EMPTY, "x")

    def test_invalid_boards_are_rejected(self):
        with self.assertRaises(ValueError):
            validate_board("x" * 22)

        with self.assertRaises(ValueError):
            validate_board("x" * 22 + "?")

    def test_neighbors_match_pdf(self):
        self.assertEqual(neighbors(0), (1, 3, 8))
        self.assertEqual(neighbors(1), (0, 2, 4))
        self.assertEqual(neighbors(2), (1, 5, 13))

    def test_neighbors_are_symmetric(self):
        for location, connected in enumerate(NEIGHBORS):
            for other in connected:
                self.assertIn(location, NEIGHBORS[other])

    def test_mills_match_pdf(self):
        self.assertIn((0, 1, 2), MILLS)
        self.assertIn((0, 3, 6), MILLS)
        self.assertIn((0, 8, 20), MILLS)

    def test_completed_mill(self):
        board = list("x" * 23)
        board[0] = "W"
        board[1] = "W"
        board[2] = "W"
        board = "".join(board)

        self.assertTrue(close_mill(0, board))
        self.assertTrue(close_mill(1, board))
        self.assertTrue(close_mill(2, board))

    def test_incomplete_mill(self):
        board = list("x" * 23)
        board[0] = "W"
        board[1] = "W"
        board = "".join(board)

        self.assertFalse(close_mill(0, board))
        self.assertFalse(close_mill(1, board))

    def test_empty_location_is_not_a_mill(self):
        board = "x" * 23
        self.assertFalse(close_mill(0, board))

    def test_piece_counts(self):
        board = "WBW" + "x" * 20

        self.assertEqual(count_pieces(board, WHITE), 2)
        self.assertEqual(count_pieces(board, BLACK), 1)

    def test_empty_locations(self):
        board = "WBW" + "x" * 20

        self.assertEqual(empty_locations(board), list(range(3, 23)))

    def test_invalid_player_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_player("R")

    
    def test_all_neighbors_match_expected_board(self):
        """Check every neighbor list against the expected board layout."""

        expected_neighbors = (
            (1, 3, 8),          # 0: a0
            (0, 2, 4),          # 1: d0
            (1, 5, 13),         # 2: g0
            (0, 4, 6, 9),       # 3: b1
            (1, 3, 5),          # 4: d1
            (2, 4, 7, 12),      # 5: f1
            (3, 7, 10),         # 6: c2
            (5, 6, 11),         # 7: e2
            (0, 9, 20),         # 8: a3
            (3, 8, 10, 17),     # 9: b3
            (6, 9, 14),         # 10: c3
            (7, 12, 16),        # 11: e3
            (5, 11, 13, 19),    # 12: f3
            (2, 12, 22),        # 13: g3
            (10, 15, 17),       # 14: c4
            (14, 16, 18),       # 15: d4
            (11, 15, 19),       # 16: e4
            (9, 14, 18, 20),    # 17: b5
            (15, 17, 19, 21),   # 18: d5
            (12, 16, 18, 22),   # 19: f5
            (8, 17, 21),        # 20: a6
            (18, 20, 22),       # 21: d6
            (13, 19, 21),       # 22: g6
        )

        self.assertEqual(len(NEIGHBORS), BOARD_SIZE)

        for location in range(BOARD_SIZE):
            with self.subTest(location=location):
                self.assertEqual(
                    neighbors(location),
                    expected_neighbors[location],
                    f"Incorrect neighbors for location {location}",
                )

    def test_all_mills_match_expected_board(self):
        """Check every mill combination against the expected board layout."""

        expected_mills = {
            (0, 1, 2),
            (3, 4, 5),
            (8, 9, 10),
            (11, 12, 13),
            (14, 15, 16),
            (17, 18, 19),
            (20, 21, 22),
            (0, 8, 20),
            (3, 9, 17),
            (6, 10, 14),
            (7, 11, 16),
            (5, 12, 19),
            (2, 13, 22),
            (15, 18, 21),
            (0, 3, 6),
            (2, 5, 7),
            (14, 17, 20),
            (16, 19, 22),
        }

        # Compare sets so the order of the mill definitions doesn't matter.
        actual_mills = {tuple(sorted(mill)) for mill in MILLS}

        self.assertEqual(len(MILLS), 18, "Expected exactly 18 mills")
        self.assertEqual(
            actual_mills,
            expected_mills,
            "The mill combinations do not match the expected board layout",
        )
        


if __name__ == "__main__":
    unittest.main(verbosity=2)
