"""Find White's best move during the Morris midgame/endgame using alpha-beta.

ALPHA-BETA search:  game/alphabeta.py
Move generator:     game/move_generator.py
Static estimation:  game/evaluation.py (static_estimation_game)
Input/output:       game/cli.py
"""

from game.alphabeta import alphabeta
from game.board import WHITE
from game.cli import run
from game.evaluation import static_estimation_game
from game.move_generator import MIDGAME


if __name__ == "__main__":
    run(
        search=alphabeta,
        evaluate=static_estimation_game,
        phase=MIDGAME,
        player=WHITE,
        description="Find White's best move during the Morris midgame/endgame using alpha-beta.",
    )
