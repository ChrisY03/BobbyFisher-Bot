import chess

PIECE_VALUES = {
    chess.PAWN:   100,
    chess.KNIGHT: 300,
    chess.BISHOP: 350,
    chess.ROOK:   500,
    chess.QUEEN:  900,
    chess.KING:   0,
}

CHECKMATE_SCORE = 100000

PAWN_TABLE = [
      0,   0,   0,   0,   0,   0,   0,   0,
     40,  40,  40,  40,  40,  40,  40,  40,
      5,   5,  15,  20,  20,  15,   5,   5,
      0,   0,   5,  15,  15,   5,   0,   0,
      0,   0,   0,  10,  10,   0,   0,   0,
      5,  -5,  -5,   0,   0,  -5,  -5,   5,
     10,  10,  10, -10, -10,  10,  10,  10,
      0,   0,   0,   0,   0,   0,   0,   0,
]

KNIGHT_TABLE = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -30,   0,   5,  10,  10,   5,   0, -30,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -30,   0,   5,  10,  10,   5,   0, -30,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -50, -40, -35, -30, -30, -35, -40, -50,
]

BISHOP_TABLE = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,  10,  15,  15,  10,   0, -10,
    -10,   5,  10,  15,  15,  10,   5, -10,
    -10,   0,  10,  15,  15,  10,   0, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,   5,   0,   0,   0,   0,   5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20,
]

ROOK_TABLE = [
      0,   0,   0,   5,   5,   0,   0,   0,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
      5,  10,  10,  10,  10,  10,  10,   5,
      0,   5,   5,   5,   5,   5,   5,   0,
]

QUEEN_TABLE = [
    -20, -10, -10,  -5,  -5, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   3,   3,   3,   3,   0, -10,
     -5,   0,   3,   3,   3,   3,   0,  -5,
      0,   0,   3,   3,   3,   3,   0,  -5,
    -10,   0,   3,   3,   3,   3,   0, -10,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -20, -10, -10,  -5,  -5, -10, -10, -20,
]

KING_TABLE_MID = [
    -40, -50, -50, -60, -60, -50, -50, -40,
    -40, -50, -50, -60, -60, -50, -50, -40,
    -40, -50, -50, -60, -60, -50, -50, -40,
    -40, -50, -50, -60, -60, -50, -50, -40,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -30, -30, -30, -30, -20,
     30,  30,   5,   0,   0,   5,  30,  30,
     30,  40,  20,   0,   0,  20,  40,  30,
]

KING_TABLE_END = [
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10,   0,   0, -10, -20, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -30,   0,   0,   0,   0, -30, -30,
    -50, -30, -30, -30, -30, -30, -30, -50,
]

PIECE_SQUARE_TABLES = {
    chess.PAWN:   PAWN_TABLE,
    chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE,
    chess.ROOK:   ROOK_TABLE,
    chess.QUEEN:  QUEEN_TABLE,
    chess.KING:   KING_TABLE_MID,
}

CENTER_SQUARES = [chess.D4, chess.E4, chess.D5, chess.E5]
EXTENDED_CENTER = [
    chess.C3, chess.D3, chess.E3, chess.F3,
    chess.C4, chess.D4, chess.E4, chess.F4,
    chess.C5, chess.D5, chess.E5, chess.F5,
    chess.C6, chess.D6, chess.E6, chess.F6,
]


def is_endgame(board):
    queens = len(board.pieces(chess.QUEEN, chess.WHITE)) + \
             len(board.pieces(chess.QUEEN, chess.BLACK))
    total = sum(
        len(board.pieces(pt, c))
        for pt in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]
        for c in [chess.WHITE, chess.BLACK]
    )
    return queens == 0 or total <= 6


def get_pst_index(color, square):
    rank = chess.square_rank(square)
    file = chess.square_file(square)
    if color == chess.WHITE:
        return (7 - rank) * 8 + file
    else:
        return rank * 8 + file


def evaluate(board):
    if board.is_checkmate():
        return -CHECKMATE_SCORE if board.turn == chess.WHITE else CHECKMATE_SCORE
    if board.is_stalemate() or board.is_insufficient_material() or \
       board.is_repetition(3) or board.is_fifty_moves():
        return 0

    endgame = is_endgame(board)
    score = 0

    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece is None:
            continue
        value = PIECE_VALUES[piece.piece_type]
        if piece.piece_type == chess.KING:
            table = KING_TABLE_END if endgame else KING_TABLE_MID
        else:
            table = PIECE_SQUARE_TABLES[piece.piece_type]
        pos = table[get_pst_index(piece.color, sq)]
        if piece.color == chess.WHITE:
            score += value + pos
        else:
            score -= value + pos

    # Mobility
    current_mobility = board.legal_moves.count()
    board.push(chess.Move.null())
    opponent_mobility = board.legal_moves.count()
    board.pop()
    if board.turn == chess.WHITE:
        score += 0.1 * (current_mobility - opponent_mobility)
    else:
        score += 0.1 * (opponent_mobility - current_mobility)

    # King safety (middlegame only)
    if not endgame:
        for color in [chess.WHITE, chess.BLACK]:
            sign = 1 if color == chess.WHITE else -1
            king_sq = board.king(color)
            king_file = chess.square_file(king_sq)
            king_rank = chess.square_rank(king_sq)
            pawn_shield = 0
            for df in [-1, 0, 1]:
                f = king_file + df
                if not (0 <= f <= 7):
                    continue
                for dr in [1, 2]:
                    r = king_rank + dr if color == chess.WHITE else king_rank - dr
                    if not (0 <= r <= 7):
                        continue
                    p = board.piece_at(chess.square(f, r))
                    if p and p.piece_type == chess.PAWN and p.color == color:
                        pawn_shield += 1
            castling_bonus = 10 if board.has_castling_rights(color) else 0
            score += sign * (pawn_shield * 15 + castling_bonus)

    # Pawn structure
    for color in [chess.WHITE, chess.BLACK]:
        sign = 1 if color == chess.WHITE else -1
        files = [chess.square_file(sq) for sq in board.pieces(chess.PAWN, color)]
        for f in range(8):
            count = files.count(f)
            if count > 1:
                score -= sign * (count - 1) * 20
            if count > 0:
                has_neighbour = (
                    (f > 0 and files.count(f - 1) > 0) or
                    (f < 7 and files.count(f + 1) > 0)
                )
                if not has_neighbour:
                    score -= sign * 15

    return score


def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    if maximizing:
        best = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            best = max(best, minimax(board, depth - 1, alpha, beta, False))
            board.pop()
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = float('inf')
        for move in board.legal_moves:
            board.push(move)
            best = min(best, minimax(board, depth - 1, alpha, beta, True))
            board.pop()
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best


def get_next_move(board, color, depth=3):
    best_move = None
    maximizing = (color == chess.WHITE)
    best_score = float('-inf') if maximizing else float('inf')
    b = board.copy()
    for move in b.legal_moves:
        b.push(move)
        score = minimax(b, depth - 1, float('-inf'), float('inf'), not maximizing)
        b.pop()
        if maximizing and score > best_score:
            best_score, best_move = score, move
        elif not maximizing and score < best_score:
            best_score, best_move = score, move
    return best_move


if __name__ == '__main__':
    b = chess.Board()
    move = get_next_move(b, chess.WHITE, depth=3)
    print(f"[team_solid] Opening move: {b.san(move)}")
