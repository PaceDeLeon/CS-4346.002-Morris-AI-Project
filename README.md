# Morris Game, Variant — AI Agent

CS 4346 (Intro to Artificial Intelligence) team project. An adversarial
search agent for the *Morris Game, Variant*, a version of Nine Men's Morris,
built with MINIMAX and ALPHA-BETA search.

## The game

- **Board:** 23 points, written as a 23-character string of `W` (White),
  `B` (Black), and `x` (empty). The characters go bottom-left to top-right:

  ```
  index:  0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22
  point:  a0 d0 g0 b1 d1 f1 c2 e2 a3 b3 c3 e3 f3 g3 c4 d4 e4 b5 d5 f5 a6 d6 g6
  ```

  Example: `xxxxxBxWWWWWBBBBxxxxxxx`

- **Phases:**
  - **Opening:** moves 1–18. Each player places 9 pieces on empty points.
  - **Midgame:** move a piece to an adjacent empty point.
  - **Endgame:** a player with exactly 3 pieces may hop to any empty point.
- **Mills:** three of your pieces on one line. Closing a mill removes one
  opponent piece that is not itself in a mill. If every opponent piece is in
  a mill, nothing is removed.
- **Win:** the opponent is reduced to 2 pieces, or has no legal move.

## How the AI works

The agent has three parts: a **move generator**, a **static evaluation**, and
a **search**.

### Move generator (`game/move_generator.py`)

This follows the handout's pseudocode:

- `generate_moves_opening` (GenerateAdd): place a piece on each empty point.
- `generate_moves_midgame` (GenerateMove): move each piece to each adjacent
  empty point.
- `generate_moves_endgame` (GenerateHopping): move each piece to any empty
  point.
- `generate_remove` (GenerateRemove): after a mill, one board for each
  removable opponent piece. If every opponent piece is in a mill, the board
  is returned unchanged.

`generate_moves(board, player, phase)` picks the right generator. Hopping is
chosen for each player separately, as soon as that player has exactly 3
pieces, so the midgame and endgame phases behave the same way. Black's moves
use the same generator with `player="B"`.

Board geometry (`NEIGHBORS`, `MILLS`) is in `game/board.py` and is checked
against the handout diagram by the tests.

### Static evaluation

Every evaluation scores a board from **White's point of view**: positive is
good for White, negative is good for Black. Scores stay within ±10000.

- **Handout baseline** (`game/evaluation.py`, used in Parts I–III):
  - Opening: `pieces(W) - pieces(B)`
  - Midgame/endgame: ±10000 if a side has 2 or fewer pieces, or if Black has
    no moves. Otherwise `1000 * (pieces(W) - pieces(B)) - moves(B)`.
- **Improved** (`game/improved_evaluation.py`, used in Part IV and the
  tournament): adds mill threats, mobility for both sides, blocked pieces,
  and completed mills. It also scores a blocked White as a loss. See
  `MyStaticEstimation.txt` for the features, weights, and reasoning.

### Search

- **MINIMAX** (`game/minimax.py`): White is MAX and Black is MIN. A node is
  scored with the static evaluation when the depth reaches 0 or the player to
  move has no legal moves. Each of those counts as one "position evaluated."
  At the root, the **first** move with the best score is kept (strict `>` or
  `<`).
- **ALPHA-BETA** (`game/alphabeta.py`): the same search, with the same move
  order and tie-break, plus pruning. A MAX node stops when its value reaches
  `beta`, and a MIN node stops when its value drops to `alpha`. A pruned
  branch can never beat the current best, so alpha-beta returns the **same
  move and estimate** as minimax while evaluating fewer positions. See
  `Examples.txt` for measured cases (3–36× fewer positions).

### Playing Black

This uses the handout's color swap: swap every `W` and `B`, find White's best
move on the swapped board, then swap the chosen board back. The printed
estimate for Black is from **Black's** point of view (positive is good for
Black).

### Tournament agent (`TournamentAgent.py`)

- **Search:** alpha-beta with the improved evaluation and **iterative
  deepening**. It searches depth 1, 2, 3, and so on until the time budget
  (180 s by default, of the 4-minute limit) runs out, then returns the move
  from the deepest search that finished.
- **Phase changes during the search:** the agent is given the move number.
  Each level of the search tree uses opening rules through move 18 and
  movement rules after that, so a search near the end of the opening
  correctly looks ahead into the midgame. The phase can't be worked out from
  the board alone, because captures change the piece count.
- **Black:** uses the same color swap as the Black scripts.

## Project structure

```
MiniMaxOpening.py           Part I    White, opening, minimax
MiniMaxGame.py              Part I    White, midgame/endgame, minimax
ABOpening.py                Part II   White, opening, alpha-beta
ABGame.py                   Part II   White, midgame/endgame, alpha-beta
MiniMaxOpeningBlack.py      Part III  Black, opening, minimax
MiniMaxGameBlack.py         Part III  Black, midgame/endgame, minimax
MiniMaxOpeningImproved.py   Part IV   White, opening, improved evaluation
MiniMaxGameImproved.py      Part IV   White, midgame/endgame, improved evaluation
TournamentAgent.py          Part V    either color, any phase, timed
Examples.txt                MINIMAX vs. ALPHA-BETA comparisons
MyStaticEstimation.txt      improved evaluation write-up

game/
  board.py                  board layout, neighbors, mills, helpers, color swap
  move_generator.py         legal moves for all phases, capture rules
  minimax.py                MINIMAX search
  alphabeta.py              ALPHA-BETA search (+ optional move-number phases)
  evaluation.py             handout static estimations (frozen baseline)
  improved_evaluation.py    improved static estimations
  cli.py                    shared input/output for the required scripts

tests/                      unittest suite
```

### Why it is structured this way

The nine required programs differ in only four choices:

- which search (minimax or alpha-beta)
- which evaluation (handout or improved)
- which phase (opening or midgame/endgame)
- which color (White or Black)

Each choice is one interchangeable module in `game/`. Each script is a few
lines that name its combination and pass it to `game/cli.py`, which handles
the file input and output and the required printed lines.

- **One source of truth.** A rule lives in one place. Fixing the move
  generator fixes every program.
- **Fair comparisons.** Minimax vs. alpha-beta, and handout vs. improved,
  differ in exactly one module. Any change in the results comes only from
  that module.
- **Frozen baseline.** The handout evaluations are never edited, so Parts
  I–III always use the required functions.
- **Testable.** The move generator, searches, and evaluations are each
  tested on their own.

Each script's docstring says which `game/` modules it uses.

## How to run

Requires **Python 3.10+**. There are no third-party packages. Run commands
from the project folder, the one that contains `game/`.

### Required programs (Parts I–IV)

```
python <Program>.py <input board file> <output board file> <depth>
```

Example, with `input.txt` containing `xxxxxBxWWWWWBBBBxxxxxxx`:

```
python MiniMaxGame.py input.txt output.txt 3
```

Output (also writes the chosen board to `output.txt`):

```
Board Position: WxxxxBxWxWWWBBBBxxxxxxx
Positions evaluated by static estimation: 677
MINIMAX estimate: 991
```

Use the `Opening` programs for positions during the opening and the `Game`
programs after all 18 pieces have been placed.

### Tournament agent

```
python TournamentAgent.py <board or board file> <output file> <W|B> <move number> [--time SECONDS]
```

- `board`: a file containing the board, or the 23-character board itself.
- `W|B`: the color this agent is playing.
- `move number`: the number of the move **this agent is about to make**.
  White's first move is 1, Black's reply is 2, and so on. Moves 1–18 are
  the opening.
- `--time`: the search budget in seconds (default 180). Use about 150 if you
  need more time to post.

Example: Black replying to move 7:

```
python TournamentAgent.py xxxWxxxxBxxWWxxxxBxxxxx out.txt B 8 --time 150
```

Output:

```
Depth searched: 6   Estimate: ...   Time: 150.0s

Move 8 - Black
<23-character board>
```

The last two lines are in the format to post in the Teams chat.

### Tests

```
python -m unittest tests.test_board tests.test_move tests.test_minimax tests.test_alphabeta tests.test_black tests.test_improved_evaluation
```

The tests cover the board geometry, move generation and capture rules,
minimax counts, alpha-beta matching minimax (5 boards, both colors, depths
1–3), Black's color swap, the improved evaluation, and phase changes during
the search at move 18. The full suite takes about 25 seconds.
