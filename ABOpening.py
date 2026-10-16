"""Compute White's best move during the Morris opening phase using alpha-beta.

ALPHA-BETA search:  game/alphabeta.py
Move generator:     game/move_generator.py
Static estimation:  game/evaluation.py (static_estimation_opening)
Input/output:       game/cli.py
"""

from game.alphabeta import alphabeta
from game.board import WHITE
from game.cli import run
from game.evaluation import static_estimation_opening
from game.move_generator import OPENING


if __name__ == "__main__":
    run(
        search=alphabeta,
        evaluate=static_estimation_opening,
        phase=OPENING,
        player=WHITE,
        description="Compute White's best move during the Morris opening phase using alpha-beta.",
    )
