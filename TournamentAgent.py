"""Tournament agent: alpha-beta with iterative deepening for either color.

Usage:
  python TournamentAgent.py <board file or 23-char board> <output file>
                            <W|B> <move number> [--time SECONDS]

The move number is the number of the move this agent is about to make
(White's first move is 1). Moves 1-18 are the opening; it cannot be
inferred from the board because captures change the piece count.

ALPHA-BETA search:  game/alphabeta.py (move_number switches phase per ply)
Move generator:     game/move_generator.py
Static estimation:  game/improved_evaluation.py
"""

import argparse
import time
from pathlib import Path

from game.alphabeta import alphabeta, phase_for_move
from game.board import WHITE, BLACK, PLAYERS, swap_colors, validate_board
from game.improved_evaluation import (
    WIN,
    improved_estimation_game,
    improved_estimation_opening,
)


DEFAULT_SECONDS = 180  # 4-minute limit per move; leaves time to post.
MAX_DEPTH = 50


class _OutOfTime(Exception):
    """Raised inside the search when the time budget is used up."""


def choose_move(board: str, player: str, move_number: int, seconds: float):
    """
    Return (board, estimate, depth) for player's move, searching deeper
    until the time budget runs out. Black uses the handout color swap.
    """
    deadline = time.monotonic() + seconds

    if player == BLACK:
        board = swap_colors(board)

    best = None

    for depth in range(1, MAX_DEPTH + 1):
        # Every leaf of a depth-d search is at move move_number + d, so
        # one evaluation function fits all leaves of this iteration.
        if phase_for_move(move_number + depth) == phase_for_move(1):
            estimate = improved_estimation_opening
        else:
            estimate = improved_estimation_game

        # Depth 1 always finishes, so there is always a move to return.
        def timed_estimate(position, estimate=estimate, depth=depth):
            if depth > 1 and time.monotonic() > deadline:
                raise _OutOfTime
            return estimate(position)

        try:
            result = alphabeta(
                board=board,
                depth=depth,
                player=WHITE,
                phase=phase_for_move(move_number),
                evaluate=timed_estimate,
                move_number=move_number,
            )
        except _OutOfTime:
            break

        best = (result.best_board, result.estimate, depth)

        # A forced win or loss will not change with a deeper search.
        if abs(result.estimate) >= WIN:
            break

    best_board, estimate, depth = best

    if player == BLACK:
        best_board = swap_colors(best_board)

    return best_board, estimate, depth


def main() -> None:
    """Read the position, choose a move, save it, and print it to post."""
    parser = argparse.ArgumentParser(
        description="Morris tournament agent (alpha-beta, iterative deepening)."
    )

    parser.add_argument("board", help="Board file, or the 23-character board itself")
    parser.add_argument("output_board_file", help="File to save the selected board")
    parser.add_argument("color", type=str.upper, choices=PLAYERS, help="W or B")
    parser.add_argument("move_number", type=int, help="Number of the move to make (1-based)")
    parser.add_argument(
        "--time",
        type=float,
        default=DEFAULT_SECONDS,
        help=f"Search time budget in seconds (default {DEFAULT_SECONDS})",
    )

    args = parser.parse_args()

    try:
        board = args.board.strip()
        if len(board) != 23 or Path(board).is_file():
            board = Path(args.board).read_text(encoding="utf-8").strip()

        validate_board(board)

        if args.move_number < 1:
            raise ValueError("Move number must be a positive integer.")

        started = time.monotonic()
        best_board, estimate, depth = choose_move(
            board, args.color, args.move_number, args.time
        )
        elapsed = time.monotonic() - started

        Path(args.output_board_file).write_text(best_board + "\n", encoding="utf-8")

    except (OSError, ValueError) as error:
        parser.error(str(error))

    side = "White" if args.color == WHITE else "Black"

    if best_board == board:
        print(f"{side} has no legal move: the game is lost.")
        return

    # Estimate is from the moving side's point of view (positive = good).
    print(f"Depth searched: {depth}   Estimate: {estimate}   Time: {elapsed:.1f}s")
    print()
    print(f"Move {args.move_number} - {side}")
    print(best_board)


if __name__ == "__main__":
    main()
