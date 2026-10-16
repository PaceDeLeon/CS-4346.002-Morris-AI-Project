"""Alpha-beta search for the Morris AI project.

Same signature, move order, and tie-breaking as game.minimax, so for the
same position and depth it returns the same move and estimate. Only the
number of positions evaluated differs.
"""

from game.board import WHITE, BLACK, validate_board, validate_player
from game.minimax import EvaluationFunction, MinimaxResult
from game.move_generator import PHASES, generate_moves


def alphabeta(
    board: str,
    depth: int,
    player: str,
    phase: str,
    evaluate: EvaluationFunction,
) -> MinimaxResult:
    """Find the best next board using minimax with alpha-beta pruning."""
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
    alpha = float("-inf")
    beta = float("inf")

    for next_board in moves:
        score, evaluated = _search(
            next_board,
            depth - 1,
            next_player,
            phase,
            evaluate,
            alpha,
            beta,
        )

        positions_evaluated += evaluated

        # Strict comparison keeps the first best move, as in minimax.
        # A pruned child returns a value no better than best_score,
        # so it can never replace the current best move.
        if maximizing and score > best_score:
            best_score = score
            best_board = next_board
        elif not maximizing and score < best_score:
            best_score = score
            best_board = next_board

        if maximizing:
            alpha = max(alpha, best_score)
        else:
            beta = min(beta, best_score)

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
    alpha: float,
    beta: float,
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
            alpha,
            beta,
        )

        positions_evaluated += evaluated

        if maximizing:
            best_score = max(best_score, score)

            # MIN above already has a move worth beta or less.
            if best_score >= beta:
                break

            alpha = max(alpha, best_score)
        else:
            best_score = min(best_score, score)

            # MAX above already has a move worth alpha or more.
            if best_score <= alpha:
                break

            beta = min(beta, best_score)

    return best_score, positions_evaluated


def _opponent(player: str) -> str:
    """Return the opposing player."""

    return BLACK if player == WHITE else WHITE
