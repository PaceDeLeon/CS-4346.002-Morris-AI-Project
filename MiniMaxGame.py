
"""Find White's best move during the Morris midgame/endgame."""

import argparse
from pathlib import Path

from game.board import WHITE, BLACK, count_pieces, validate_board
from game.move_generator import MIDGAME, ENDGAME
from game.minimax import minimax
from game.evaluation import static_estimation_game


def main() -> None:
    """Read a board, run minimax, and save White's selected move."""
    parser = argparse.ArgumentParser(
        description="Find White's best Morris midgame/endgame move."
    )

    parser.add_argument("input_board_file")
    parser.add_argument("output_board_file")
    parser.add_argument("depth", type=int)

    args = parser.parse_args()

    try:
        board = Path(args.input_board_file).read_text(
            encoding="utf-8"
        ).strip()

        validate_board(board)

        white_pieces = count_pieces(board, WHITE)
        black_pieces = count_pieces(board, BLACK)

        # Select the phase based on the input position.
        phase = (
            ENDGAME
            if white_pieces == 3 or black_pieces == 3
            else MIDGAME
        )

        result = minimax(
            board=board,
            depth=args.depth,
            player=WHITE,
            phase=phase,
            evaluate=static_estimation_game,
        )

        Path(args.output_board_file).write_text(
            result.best_board + "\n",
            encoding="utf-8",
        )

    except (OSError, ValueError) as error:
        parser.error(str(error))

    print(f"Board Position: {result.best_board}")
    print(
        "Positions evaluated by static estimation: "
        f"{result.positions_evaluated}"
    )
    print(f"MINIMAX estimate: {result.estimate}")


if __name__ == "__main__":
    main()
