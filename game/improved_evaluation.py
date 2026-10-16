"""Improved static estimation functions (White's perspective).

The handout versions in game/evaluation.py stay unchanged as the baseline.
See MyStaticEstimation.txt for the rationale behind each feature and weight.
"""

from game.board import (
    WHITE,
    BLACK,
    EMPTY,
    MILLS,
    count_pieces,
    empty_locations,
    mills_at,
    neighbors,
)


WIN = 10000

# Opening weights.
OPENING_PIECE = 100
OPENING_THREAT = 30
OPENING_MOBILITY = 3

# Midgame/endgame weights.
GAME_PIECE = 1000
GAME_THREAT = 50
GAME_BLOCKED = 20
GAME_MILL = 10
GAME_MOBILITY = 5


def improved_estimation_opening(board: str) -> int:
    """Opening estimate: material, mill threats, and room to move later."""
    return (
        OPENING_PIECE * (count_pieces(board, WHITE) - count_pieces(board, BLACK))
        + OPENING_THREAT
        * (_mill_threats(board, WHITE, True) - _mill_threats(board, BLACK, True))
        + OPENING_MOBILITY
        * (_mobility(board, WHITE, False) - _mobility(board, BLACK, False))
    )


def improved_estimation_game(board: str) -> int:
    """Midgame/endgame estimate: wins, material, threats, blocking, mobility."""
    white_pieces = count_pieces(board, WHITE)
    black_pieces = count_pieces(board, BLACK)

    if black_pieces <= 2:
        return WIN
    if white_pieces <= 2:
        return -WIN

    white_moves = _mobility(board, WHITE, True)
    black_moves = _mobility(board, BLACK, True)

    # A player with no legal move loses. The handout version only
    # checks this for Black.
    if black_moves == 0:
        return WIN
    if white_moves == 0:
        return -WIN

    score = (
        GAME_PIECE * (white_pieces - black_pieces)
        + GAME_THREAT
        * (_mill_threats(board, WHITE, False) - _mill_threats(board, BLACK, False))
        + GAME_BLOCKED * (_blocked(board, BLACK) - _blocked(board, WHITE))
        + GAME_MILL * (_mills(board, WHITE) - _mills(board, BLACK))
        + GAME_MOBILITY * (white_moves - black_moves)
    )

    # Keep non-terminal positions strictly inside the win scores.
    return max(-WIN + 1, min(WIN - 1, score))


def _mobility(board: str, player: str, hopping_allowed: bool) -> int:
    """
    Count (piece, destination) moves, ignoring which piece gets captured.

    Hopping does not apply during the opening, so there it only counts
    adjacent empty spots (room to move once the midgame starts).
    """
    if hopping_allowed and count_pieces(board, player) == 3:
        return 3 * len(empty_locations(board))

    return sum(
        1
        for location, piece in enumerate(board)
        if piece == player
        for neighbor in neighbors(location)
        if board[neighbor] == EMPTY
    )


def _mill_threats(board: str, player: str, opening: bool) -> int:
    """
    Count empty spots where player can close a mill on their next move.

    Opening: any empty spot completing two of player's pieces in a line
    (a piece can be placed there). Otherwise, a piece outside that line
    must be able to reach the spot: adjacent, or any piece when hopping.
    """
    flying = count_pieces(board, player) == 3
    threats = 0

    for spot in empty_locations(board):
        for mill in mills_at(spot):
            line = [p for p in mill if p != spot]

            if not all(board[p] == player for p in line):
                continue

            # Hopping with 3 pieces: the third piece can fly to the spot.
            if opening or flying:
                can_reach = True
            else:
                can_reach = any(
                    board[n] == player and n not in line
                    for n in neighbors(spot)
                )

            if can_reach:
                threats += 1
                break

    return threats


def _blocked(board: str, player: str) -> int:
    """Count player's pieces with no empty neighbor (0 while hopping)."""
    if count_pieces(board, player) == 3:
        return 0

    return sum(
        1
        for location, piece in enumerate(board)
        if piece == player
        and all(board[n] != EMPTY for n in neighbors(location))
    )


def _mills(board: str, player: str) -> int:
    """Count completed mills owned by player."""
    return sum(1 for mill in MILLS if all(board[p] == player for p in mill))
