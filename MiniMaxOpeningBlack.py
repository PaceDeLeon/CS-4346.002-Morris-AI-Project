"""Compute Black's best move during the Morris opening phase.

Uses the handout's color swap: swap W and B, find White's best move
with MINIMAX, then swap the chosen board back (see game/cli.py).

MINIMAX search:     game/minimax.py
Move generator:     game/move_generator.py
Static estimation:  game/evaluation.py (static_estimation_opening)
Input/output:       game/cli.py
"""

from game.board import BLACK
from game.cli import run
from game.evaluation import static_estimation_opening
from game.minimax import minimax
from game.move_generator import OPENING


if __name__ == "__main__":
    run(
        search=minimax,
        evaluate=static_estimation_opening,
        phase=OPENING,
        player=BLACK,
        description="Compute Black's best move during the Morris opening phase.",
    )
