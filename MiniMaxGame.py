"""Find White's best move during the Morris midgame/endgame.

MINIMAX search:     game/minimax.py
Move generator:     game/move_generator.py
Static estimation:  game/evaluation.py (static_estimation_game)
Input/output:       game/cli.py
"""

from game.board import WHITE
from game.cli import run
from game.evaluation import static_estimation_game
from game.minimax import minimax
from game.move_generator import MIDGAME


if __name__ == "__main__":
    # MIDGAME covers the endgame too: the move generator switches a
    # player to hopping when they have exactly three pieces.
    run(
        search=minimax,
        evaluate=static_estimation_game,
        phase=MIDGAME,
        player=WHITE,
        description="Find White's best Morris midgame/endgame move.",
    )
