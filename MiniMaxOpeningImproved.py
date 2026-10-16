"""Compute White's best move during the Morris opening phase with the improved static estimation.

MINIMAX search:     game/minimax.py
Move generator:     game/move_generator.py
Static estimation:  game/improved_evaluation.py (improved_estimation_opening)
                    rationale in MyStaticEstimation.txt
Input/output:       game/cli.py
"""

from game.board import WHITE
from game.cli import run
from game.improved_evaluation import improved_estimation_opening
from game.minimax import minimax
from game.move_generator import OPENING


if __name__ == "__main__":
    run(
        search=minimax,
        evaluate=improved_estimation_opening,
        phase=OPENING,
        player=WHITE,
        description="Compute White's best move during the Morris opening phase with the improved static estimation.",
    )
