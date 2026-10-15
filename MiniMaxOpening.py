
"""Compute White's best move during the Morris opening phase."""

import argparse
from pathlib import Path

from game.board import WHITE, validate_board
from game.move_generator import OPENING
from game.minimax import minimax
from game.evaluation import static_estimation_opening


def main() -> None:
    """Read the input board, run minimax, and save the selected board."""
    parser = argparse.ArgumentParser(
        description="Find White's best move during the Morris opening phase."
    )

    parser.add_argument("input_board_file", help="File containing the input board")
    parser.add_argument("output_board_file", help="File to save the selected board")
    parser.add_argument("depth", type=int, help="Minimax search depth")

    args = parser.parse_args()

    try:
        # Read the 23-character board from the input file.
        board = Path(args.input_board_file).read_text(
            encoding="utf-8"
        ).strip()

        validate_board(board)

        # Search for White's best opening move.
        result = minimax(
            board=board,
            depth=args.depth,
            player=WHITE,
            phase=OPENING,
            evaluate=static_estimation_opening,
        )

        # Save only the selected board position to the output file.
        Path(args.output_board_file).write_text(
            result.best_board + "\n",
            encoding="utf-8",
        )

    except (OSError, ValueError) as error:
        parser.error(str(error))

    # Print the output in the format requested by the project.
    print(f"Board Position: {result.best_board}")
    print(
        "Positions evaluated by static estimation: "
        f"{result.positions_evaluated}"
    )
    print(f"MINIMAX estimate: {result.estimate}")


if __name__ == "__main__":
    main()
