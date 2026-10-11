
"""Minimax search for the Morris AI project."""

from dataclasses import dataclass
from typing import Callable

from game.board import (
    WHITE,
    BLACK,
    count_pieces,
    validate_board,
    validate_player,
)
from game.move_generator import PHASES, OPENING, generate_moves


WIN_SCORE = 10000

EvaluationFunction = Callable[[str], int | float]


@dataclass
class MinimaxResult:
    """Results returned by a minimax search."""

    best_board: str
    estimate: int | float
    positions_evaluated: int


def minimax(
    board: str,
    depth: int,
    player: str,
    phase: str,
    evaluate: EvaluationFunction,
) -> MinimaxResult:
    """Find the best next board using minimax."""
    validate_board(board)
    validate_player(player)

    if not isinstance(depth, int) or isinstance(depth, bool) or depth < 1:
        raise ValueError("Depth must be a positive integer.")

    if phase not in PHASES:
        raise ValueError(
            "Phase must be 'opening', 'midgame', or 'endgame'."
        )

    if not callable(evaluate):
        raise TypeError("evaluate must be a callable function.")

    # Check whether the game has already been won.
    terminal_score = _piece_terminal_score(board, phase)
    if terminal_score is not None:
        return MinimaxResult(board, terminal_score, 0)

    # Generate all legal moves for the current player.
    moves = generate_moves(board, player, phase)

    # Handle a position where the current player cannot move.
    if not moves:
        if phase == OPENING:
            return MinimaxResult(board, evaluate(board), 1)

        score = -WIN_SCORE if player == WHITE else WIN_SCORE
        return MinimaxResult(board, score, 0)

    # White is MAX; Black is MIN.
    maximizing = player == WHITE
    best_score = float("-inf") if maximizing else float("inf")
    best_board = moves[0]
    positions_evaluated = 0
    next_player = _opponent(player)

    # Explore each possible move from the current position.
    for next_board in moves:
        score, evaluated = _search(
            next_board,
            depth - 1,
            next_player,
            phase,
            evaluate,
        )

        positions_evaluated += evaluated

        if maximizing and score > best_score:
            best_score = score
            best_board = next_board
        elif not maximizing and score < best_score:
            best_score = score
            best_board = next_board

    return MinimaxResult(
        best_board=best_board,
        estimate=best_score,
        positions_evaluated=positions_evaluated,
    )


def _search(
    board: str,
    depth: int,
    player: str,
    phase: str,
    evaluate: EvaluationFunction,
) -> tuple[int | float, int]:
    """Search a subtree and return its score and static-evaluation count."""

    # A win/loss score is not a static evaluation.
    terminal_score = _piece_terminal_score(board, phase)
    if terminal_score is not None:
        return terminal_score, 0

    moves = generate_moves(board, player, phase)

    # A player who cannot move loses outside the opening phase.
    if not moves:
        if phase == OPENING:
            return evaluate(board), 1

        score = -WIN_SCORE if player == WHITE else WIN_SCORE
        return score, 0

    # At depth zero, score this leaf with the supplied evaluation function.
    if depth == 0:
        return evaluate(board), 1

    next_player = _opponent(player)
    maximizing = player == WHITE

    best_score = float("-inf") if maximizing else float("inf")
    positions_evaluated = 0

    for next_board in moves:
        score, evaluated = _search(
            next_board,
            depth - 1,
            next_player,
            phase,
            evaluate,
        )

        positions_evaluated += evaluated

        if maximizing:
            best_score = max(best_score, score)
        else:
            best_score = min(best_score, score)

    return best_score, positions_evaluated


def _piece_terminal_score(board: str, phase: str) -> int | None:
    """Return a terminal score when a player has fewer than three pieces."""

    # Piece-count wins do not apply during the opening phase.
    if phase == OPENING:
        return None

    if count_pieces(board, BLACK) <= 2:
        return WIN_SCORE

    if count_pieces(board, WHITE) <= 2:
        return -WIN_SCORE

    return None


def _opponent(player: str) -> str:
    """Return the opposing player."""

    return BLACK if player == WHITE else WHITE
