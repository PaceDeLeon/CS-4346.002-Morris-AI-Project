import unittest

from game.board import EMPTY, WHITE, BLACK, neighbors
from game.move_generator import (
    OPENING,
    MIDGAME,
    ENDGAME,
    generate_moves,
    generate_moves_opening,
    generate_moves_midgame,
    generate_moves_endgame,
    generate_remove,
)


class TestMoveGenerator(unittest.TestCase):

    def test_opening_generates_all_empty_locations(self):
        board = "x" * 23

        moves = generate_moves(board, WHITE, OPENING)

        self.assertEqual(len(moves), 23)
        self.assertTrue(all(move.count(WHITE) == 1 for move in moves))
        self.assertTrue(all(move.count(BLACK) == 0 for move in moves))

    def test_opening_supports_black(self):
        board = "x" * 23

        moves = generate_moves_opening(board, BLACK)

        self.assertEqual(len(moves), 23)
        self.assertTrue(all(move.count(BLACK) == 1 for move in moves))

    def test_mill_triggers_capture(self):
        board = list("x" * 23)
        board[0] = WHITE
        board[1] = WHITE
        board[3] = BLACK
        board = "".join(board)

        moves = generate_moves_opening(board, WHITE)

        expected = list(board)
        expected[2] = WHITE
        expected[3] = EMPTY
        expected = "".join(expected)

        self.assertIn(expected, moves)

    def test_midgame_moves_only_to_adjacent_empty_locations(self):
        board = list("x" * 23)
        board[0] = WHITE
        board[10] = BLACK
        board = "".join(board)

        moves = generate_moves_midgame(board, WHITE)

        self.assertEqual(len(moves), 3)

        for move in moves:
            self.assertEqual(move.count(WHITE), 1)
            self.assertEqual(move.count(BLACK), 1)

    def test_endgame_can_fly_to_any_empty_location(self):
        board = list("x" * 23)
        board[0] = WHITE
        board[10] = WHITE
        board[20] = WHITE
        board[5] = BLACK
        board[15] = BLACK
        board[22] = BLACK
        board = "".join(board)

        moves = generate_moves_endgame(board, WHITE)

        for move in moves:
            self.assertEqual(move.count(WHITE), 3)

        # White moves from 0 to 2, a non-adjacent empty position.
        expected = list(board)
        expected[0] = EMPTY
        expected[2] = WHITE
        expected = "".join(expected)

        self.assertIn(expected, moves)

    def test_invalid_phase_is_rejected(self):
        with self.assertRaises(ValueError):
            generate_moves("x" * 23, WHITE, "invalid")

    
    def test_cannot_remove_piece_from_mill_if_unprotected_piece_exists(self):
        # Black has a mill at locations 0, 1, and 2.
        # Black also has an unprotected piece at location 3.
        board = list("x" * 23)
        board[0] = BLACK
        board[1] = BLACK
        board[2] = BLACK
        board[3] = BLACK
        board[10] = WHITE
        board = "".join(board)

        moves = generate_remove(board, WHITE)

        # Only the unprotected Black piece at location 3 can be removed.
        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0][3], EMPTY)
        self.assertEqual(moves[0][0], BLACK)
        self.assertEqual(moves[0][1], BLACK)
        self.assertEqual(moves[0][2], BLACK)

    def test_can_remove_piece_from_mill_if_all_opponent_pieces_in_mills(self):
        # Black's three pieces form a mill at locations 0, 1, and 2.
        board = list("x" * 23)
        board[0] = BLACK
        board[1] = BLACK
        board[2] = BLACK
        board[10] = WHITE
        board = "".join(board)

        moves = generate_remove(board, WHITE)

        # Any of the three Black pieces may be removed.
        self.assertEqual(len(moves), 3)
        for move in moves:
            self.assertEqual(move.count(BLACK), 2)
            self.assertEqual(move.count(WHITE), 1)

    def test_player_with_fewer_than_three_pieces_has_no_midgame_moves(self):
        board = list("x" * 23)
        board[0] = WHITE
        board[10] = WHITE
        board[20] = BLACK
        board = "".join(board)

        moves = generate_moves(board, WHITE, MIDGAME)

        self.assertEqual(moves, [])

    
    def test_blocked_player_has_no_midgame_moves(self):
        # Give White four pieces so flying is not allowed.
        white_locations = {0, 4, 10, 15}

        # Find every location that is adjacent to a White piece.
        blocked_locations = set(white_locations)

        for location in white_locations:
            blocked_locations.update(neighbors(location))

        # Choose an empty location that is not adjacent to White.
        empty_location = next(
            location
            for location in range(23)
            if location not in blocked_locations
        )

        # Fill the board with Black pieces.
        board = [BLACK] * 23

        # Place White's four pieces.
        for location in white_locations:
            board[location] = WHITE

        # Leave one empty location that White cannot reach.
        board[empty_location] = EMPTY
        board = "".join(board)

        moves = generate_moves(board, WHITE, MIDGAME)

        self.assertEqual(moves, [])


    def test_every_generated_move_is_a_valid_board_string(self):
        board = list("x" * 23)
        board[0] = WHITE
        board[1] = WHITE
        board[10] = BLACK
        board[15] = BLACK
        board = "".join(board)

        moves = generate_moves(board, WHITE, OPENING)

        self.assertGreater(len(moves), 0)

        for move in moves:
            self.assertEqual(len(move), 23)
            self.assertTrue(set(move).issubset({WHITE, BLACK, EMPTY}))



if __name__ == "__main__":
    unittest.main(verbosity=2)
