"""Compute White's best move during the Morris opening phase."""

from game.board import WHITE
from game.cli import run
from game.evaluation import static_estimation_opening
from game.minimax import minimax
from game.move_generator import OPENING


if __name__ == "__main__":
    run(
        search=minimax,
        evaluate=static_estimation_opening,
        phase=OPENING,
        player=WHITE,
        description="Find White's best move during the Morris opening phase.",
    )
