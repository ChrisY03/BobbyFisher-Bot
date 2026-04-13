import chess
import importlib

# ── Config ────────────────────────────────────────────────────────────────
CURRENT_BOT = "v7"
BASELINE_BOT = "v6"
DEPTH = 3
MAX_PLIES = 200   # safety stop to avoid endless games

# Use either:
# - "moves": a list of UCI moves from the normal start position
# - "fen": a direct FEN position
TEST_POSITIONS = [
    {"name": "Start Position", "moves": []},

    {"name": "Italian Game",
     "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "f8c5"]},

    {"name": "Queen's Gambit Declined",
     "moves": ["d2d4", "d7d5", "c2c4", "e7e6", "b1c3", "g8f6"]},

    {"name": "Caro-Kann",
     "moves": ["e2e4", "c7c6", "d2d4", "d7d5", "b1c3", "d5e4"]},

    {"name": "King's Indian Setup",
     "moves": ["d2d4", "g8f6", "c2c4", "g7g6", "b1c3", "f8g7", "e2e4", "d7d6"]},

    {"name": "Scotch Setup",
     "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "d2d4", "e5d4", "f3d4"]},

    # Simple endgames
    {"name": "KQ vs K",
     "fen": "8/8/8/3k4/8/3K4/4Q3/8 w - - 0 1"},

    {"name": "KR vs K",
     "fen": "8/8/8/3k4/8/3K4/4R3/8 w - - 0 1"},
]


# ── Helpers ───────────────────────────────────────────────────────────────
def load_bot(module_name):
    return importlib.import_module(module_name)


def make_board(position_spec):
    if "fen" in position_spec:
        return chess.Board(position_spec["fen"])

    board = chess.Board()
    for uci in position_spec["moves"]:
        board.push_uci(uci)
    return board


def play_game(start_board, white_bot, black_bot, depth=3, max_plies=200):
    board = start_board.copy()

    while not board.is_game_over() and len(board.move_stack) < max_plies:
        bot = white_bot if board.turn == chess.WHITE else black_bot
        move = bot.get_next_move(board, board.turn, depth)

        if move is None or move not in board.legal_moves:
            # Illegal or missing move = immediate loss for side to move
            return "0-1" if board.turn == chess.WHITE else "1-0", "illegal move"

        board.push(move)

    if board.is_game_over():
        outcome = board.outcome()
        if outcome is None:
            return board.result(), "game over"
        return outcome.result(), outcome.termination.name

    return "1/2-1/2", "max plies reached"


def score_for_current(result, current_is_white):
    if result == "1/2-1/2":
        return 0.5
    if result == "1-0":
        return 1.0 if current_is_white else 0.0
    if result == "0-1":
        return 0.0 if current_is_white else 1.0
    return 0.5


# ── Main benchmark ────────────────────────────────────────────────────────
def run_benchmark():
    current_bot = load_bot(CURRENT_BOT)
    baseline_bot = load_bot(BASELINE_BOT)

    total_score = 0.0
    total_games = 0

    current_white_score = 0.0
    current_black_score = 0.0
    current_white_games = 0
    current_black_games = 0

    print(f"\nBenchmark: {CURRENT_BOT} vs {BASELINE_BOT}")
    print(f"Depth: {DEPTH}")
    print("-" * 72)

    for pos in TEST_POSITIONS:
        name = pos["name"]

        # Game 1: current bot as White
        board1 = make_board(pos)
        result1, reason1 = play_game(board1, current_bot, baseline_bot, DEPTH, MAX_PLIES)
        score1 = score_for_current(result1, current_is_white=True)

        total_score += score1
        total_games += 1
        current_white_score += score1
        current_white_games += 1

        print(f"{name:<24} | Current = White | Result: {result1:<7} | {reason1}")

        # Game 2: current bot as Black
        board2 = make_board(pos)
        result2, reason2 = play_game(board2, baseline_bot, current_bot, DEPTH, MAX_PLIES)
        score2 = score_for_current(result2, current_is_white=False)

        total_score += score2
        total_games += 1
        current_black_score += score2
        current_black_games += 1

        print(f"{name:<24} | Current = Black | Result: {result2:<7} | {reason2}")
        print("-" * 72)

    overall_pct = 100 * total_score / total_games
    white_pct = 100 * current_white_score / current_white_games if current_white_games else 0
    black_pct = 100 * current_black_score / current_black_games if current_black_games else 0

    print("\nFinal Summary")
    print("=" * 72)
    print(f"Current bot score: {total_score:.1f} / {total_games}")
    print(f"Overall score %   : {overall_pct:.1f}%")
    print(f"As White          : {current_white_score:.1f} / {current_white_games}  ({white_pct:.1f}%)")
    print(f"As Black          : {current_black_score:.1f} / {current_black_games}  ({black_pct:.1f}%)")

    if overall_pct > 55:
        print("Verdict: current bot looks stronger.")
    elif overall_pct < 45:
        print("Verdict: baseline bot looks stronger.")
    else:
        print("Verdict: roughly similar strength.")


if __name__ == "__main__":
    run_benchmark()