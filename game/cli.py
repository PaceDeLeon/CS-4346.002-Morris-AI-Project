"""Shared command-line runner for the Morris search scripts."""

import argparse
from pathlib import Path

from game.board import WHITE, BLACK, swap_colors, validate_board


def run(search, evaluate, phase: str, player: str, description: str) -> None:
    """
    Read a board file, search for player's best move, and report it.

    Usage: script input_board_file output_board_file depth

    Black is handled with the handout's color swap: swap the board,
    search for White, then swap the chosen board back.
    """
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("input_board_file", help="File containing the input board")
    parser.add_argument("output_board_file", help="File to save the selected board")
    parser.add_argument("depth", type=int, help="Search depth")

    args = parser.parse_args()

    try:
        # Read the 23-character board from the input file.
        board = Path(args.input_board_file).read_text(
            encoding="utf-8"
        ).strip()

        validate_board(board)

        if player == BLACK:
            board = swap_colors(board)

        result = search(
            board=board,
            depth=args.depth,
            player=WHITE,
            phase=phase,
            evaluate=evaluate,
        )

        best_board = result.best_board
        if player == BLACK:
            best_board = swap_colors(best_board)

        # Save only the selected board position to the output file.
        Path(args.output_board_file).write_text(
            best_board + "\n",
            encoding="utf-8",
        )

    except (OSError, ValueError) as error:
        parser.error(str(error))

    # Print the output in the format requested by the project.
    print(f"Board Position: {best_board}")
    print(
        "Positions evaluated by static estimation: "
        f"{result.positions_evaluated}"
    )
    print(f"MINIMAX estimate: {result.estimate}")
