
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

    moves = generate_moves(board, player, phase)

    # No legal move: none to choose, return static estimate
    if not moves:
        return MinimaxResult(board, evaluate(board), 1)

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

    # At depth zero, score this leaf with the static estimate.
    if depth == 0:
        return evaluate(board), 1

    moves = generate_moves(board, player, phase)

    # No moves available; treat as leaf & use static estimate
    if not moves:
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

def _opponent(player: str) -> str:
    """Return the opposing player."""

    return BLACK if player == WHITE else WHITE
