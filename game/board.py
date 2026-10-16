
"""Board representation and helper functions for the Morris game."""

BOARD_SIZE = 23

WHITE = "W"
BLACK = "B"
EMPTY = "x"

PLAYERS = (WHITE, BLACK)

# Each index represents a board location.
# The values are the locations directly connected to it.
NEIGHBORS = (
    (1, 3, 8),
    (0, 2, 4),
    (1, 5, 13),
    (0, 4, 6, 9),
    (1, 3, 5),
    (2, 4, 7, 12),
    (3, 7, 10),
    (5, 6, 11),
    (0, 9, 20),
    (3, 8, 10, 17),
    (6, 9, 14),
    (7, 12, 16),
    (5, 11, 13, 19),
    (2, 12, 22),
    (10, 15, 17),
    (14, 16, 18),
    (11, 15, 19),
    (9, 14, 18, 20),
    (15, 17, 19, 21),
    (12, 16, 18, 22),
    (8, 17, 21),
    (18, 20, 22),
    (13, 19, 21),
)

# Each group of three locations represents a mill.
MILLS = (
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
)


def validate_board(board: str) -> None:
    """Check that a board is a valid 23-character string."""
    if not isinstance(board, str) or len(board) != BOARD_SIZE:
        raise ValueError(
            f"Board must be a {BOARD_SIZE}-character string."
        )

    if any(piece not in (WHITE, BLACK, EMPTY) for piece in board):
        raise ValueError("Board may contain only 'W', 'B', and 'x'.")


def validate_player(player: str) -> None:
    """Check that the player is White or Black."""
    if player not in PLAYERS:
        raise ValueError("Player must be 'W' or 'B'.")


def neighbors(location: int) -> tuple[int, ...]:
    """Return the locations directly connected to a location."""
    if not isinstance(location, int) or not 0 <= location < BOARD_SIZE:
        raise ValueError(
            f"Location must be between 0 and {BOARD_SIZE - 1}."
        )

    return NEIGHBORS[location]


def mills_at(location: int) -> tuple[tuple[int, int, int], ...]:
    """Return all mill combinations that include a location."""
    if not isinstance(location, int) or not 0 <= location < BOARD_SIZE:
        raise ValueError(
            f"Location must be between 0 and {BOARD_SIZE - 1}."
        )

    return tuple(
        mill for mill in MILLS if location in mill
    )


def close_mill(location: int, board: str) -> bool:
    """Return True if the piece at a location belongs to a completed mill."""
    validate_board(board)

    if not isinstance(location, int) or not 0 <= location < BOARD_SIZE:
        raise ValueError(
            f"Location must be between 0 and {BOARD_SIZE - 1}."
        )

    piece = board[location]

    # An empty location cannot be part of a completed mill.
    if piece == EMPTY:
        return False

    return any(
        all(board[position] == piece for position in mill)
        for mill in mills_at(location)
    )


def count_pieces(board: str, player: str) -> int:
    """Count how many pieces a player has on the board."""
    validate_board(board)
    validate_player(player)

    return board.count(player)


def empty_locations(board: str) -> list[int]:
    """Return the indices of all empty board locations."""
    validate_board(board)

    return [
        location
        for location, piece in enumerate(board)
        if piece == EMPTY
    ]


def swap_colors(board: str) -> str:
    """Swap every W and B on the board (handout's Black-move method)."""
    validate_board(board)

    return board.translate(str.maketrans({WHITE: BLACK, BLACK: WHITE}))
