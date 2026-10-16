"""Find White's best move during the Morris midgame/endgame with the improved static estimation.

MINIMAX search:     game/minimax.py
Move generator:     game/move_generator.py
Static estimation:  game/improved_evaluation.py (improved_estimation_game)
                    rationale in MyStaticEstimation.txt
Input/output:       game/cli.py
"""

from game.board import WHITE
from game.cli import run
from game.improved_evaluation import improved_estimation_game
from game.minimax import minimax
from game.move_generator import MIDGAME


if __name__ == "__main__":
    run(
        search=minimax,
        evaluate=improved_estimation_game,
        phase=MIDGAME,
        player=WHITE,
        description="Find White's best move during the Morris midgame/endgame with the improved static estimation.",
    )
