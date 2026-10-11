
"""Generate legal board states for Morris."""

from game.board import (
    BOARD_SIZE,
    WHITE,
    BLACK,
    EMPTY,
    PLAYERS,
    validate_board,
    validate_player,
    neighbors,
    close_mill,
    count_pieces,
    empty_locations,
)


OPENING = "opening"
MIDGAME = "midgame"
ENDGAME = "endgame"

PHASES = (OPENING, MIDGAME, ENDGAME)



def generate_moves(board: str, player: str, phase: str) -> list[str]:
    """
    Generate all legal next board states for a player.

    board: A 23-character board string.
    player: WHITE ("W") or BLACK ("B").
    phase: OPENING, MIDGAME, or ENDGAME.

    Returns a list of new board strings.
    """
    validate_board(board)
    validate_player(player)

    if phase not in PHASES:
        raise ValueError(
            "Phase must be 'opening', 'midgame', or 'endgame'."
        )

    if phase == OPENING:
        return generate_moves_opening(board, player)

    if phase == MIDGAME:
        # A player with fewer than three pieces cannot continue.
        if count_pieces(board, player) < 3:
            return []

        return generate_moves_midgame(board, player)

    
    # In the endgame, a player with exactly three pieces may fly.
    # A player with more than three pieces must move to an adjacent
    # empty location. A player with fewer than three cannot continue.
    if count_pieces(board, player) < 3:
        return []

    if count_pieces(board, player) == 3:
        return generate_moves_endgame(board, player)

    return generate_moves_midgame(board, player)




def generate_moves_opening(board: str, player: str) -> list[str]:
    """Generate moves that place a piece on an empty location."""
    validate_board(board)
    validate_player(player)

    moves = []

    for location in empty_locations(board):
        new_board = list(board)
        new_board[location] = player
        new_board = "".join(new_board)

        if close_mill(location, new_board):
            moves.extend(generate_remove(new_board, player))
        else:
            moves.append(new_board)

    return moves


def generate_moves_midgame(board: str, player: str) -> list[str]:
    """Move a piece to an adjacent empty location."""
    validate_board(board)
    validate_player(player)

    # Flying is only allowed with exactly three pieces.
    if count_pieces(board, player) == 3:
        return generate_moves_endgame(board, player)

    moves = []

    for source in range(BOARD_SIZE):
        if board[source] != player:
            continue

        for destination in neighbors(source):
            if board[destination] != EMPTY:
                continue

            new_board = list(board)
            new_board[source] = EMPTY
            new_board[destination] = player
            new_board = "".join(new_board)

            if close_mill(destination, new_board):
                moves.extend(generate_remove(new_board, player))
            else:
                moves.append(new_board)

    return moves


def generate_moves_endgame(board: str, player: str) -> list[str]:
    """Move a piece to any empty location when flying is allowed."""
    validate_board(board)
    validate_player(player)

    moves = []

    for source in range(BOARD_SIZE):
        if board[source] != player:
            continue

        for destination in empty_locations(board):
            new_board = list(board)
            new_board[source] = EMPTY
            new_board[destination] = player
            new_board = "".join(new_board)

            if close_mill(destination, new_board):
                moves.extend(generate_remove(new_board, player))
            else:
                moves.append(new_board)

    return moves


def generate_remove(board: str, player: str) -> list[str]:
    """
    Generate board states after capturing an opponent's piece.

    Prefer opponent pieces that are not in mills. If all opponent
    pieces are in mills, any opponent piece may be captured.
    """
    validate_board(board)
    validate_player(player)

    opponent = BLACK if player == WHITE else WHITE

    opponent_locations = [
        location
        for location, piece in enumerate(board)
        if piece == opponent
    ]

    # There is nothing to capture.
    if not opponent_locations:
        return [board]

    # First, find opponent pieces that are not protected by a mill.
    removable = [
        location
        for location in opponent_locations
        if not close_mill(location, board)
    ]

    # If all opponent pieces are in mills, allow any capture.
    if not removable:
        removable = opponent_locations

    moves = []

    for location in removable:
        new_board = list(board)
        new_board[location] = EMPTY
        moves.append("".join(new_board))

    return moves
