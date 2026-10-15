"""Static estimation functions from the Morris handout (White's perspective)."""

from game.board import WHITE, BLACK, count_pieces
from game.move_generator import MIDGAME, generate_moves


def static_estimation_opening(board: str) -> int:
    """Return the opening static estimate from the Morris handout."""
    return count_pieces(board, WHITE) - count_pieces(board, BLACK)


def static_estimation_game(board: str) -> int:
    """
    Midgame/endgame static estimate from Morris handout.

    Positive scores favor White; negative scores favor Black.
    """
    white_pieces = count_pieces(board, WHITE)
    black_pieces = count_pieces(board, BLACK)

    black_moves = len(generate_moves(board, BLACK, MIDGAME))

    if black_pieces <= 2:
        return 10000
    if white_pieces <= 2:
        return -10000
    if black_moves == 0:
        return 10000

    return 1000 * (white_pieces - black_pieces) - black_moves
