"""
team_alpha.py  —  Chess Bot using Minimax + Alpha-Beta Pruning
Heuristic: Material value , 
    Piece mobility, 
    King Safety, 
    Move ordering

Install dependency:  pip install python-chess
"""

import chess

PAWN_TABLE = [
      0,   0,   0,   0,   0,   0,   0,   0,
     50,  50,  50,  50,  50,  50,  50,  50,
     10,  10,  20,  30,  30,  20,  10,  10,
      5,   5,  10,  25,  25,  10,   5,   5,
      0,   0,   0,  20,  20,   0,   0,   0,
      5,  -5, -10,   0,   0, -10,  -5,   5,
      5,  10,  10, -20, -20,  10,  10,   5,
      0,   0,   0,   0,   0,   0,   0,   0,
]

KNIGHT_TABLE = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -30,   5,  10,  15,  15,  10,   5, -30,
    -30,   0,  15,  20,  20,  15,   0, -30,
    -30,   5,  15,  20,  20,  15,   5, -30,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50,
]

BISHOP_TABLE = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   5,   0,   0,   0,   0,   5, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,   0,  10,  10,  10,  10,   0, -10,
    -10,   5,   5,  10,  10,   5,   5, -10,
    -10,   0,   5,  10,  10,   5,   0, -10,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20,
]

ROOK_TABLE = [
      0,   0,   5,  10,  10,   5,   0,   0,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
      5,  10,  10,  10,  10,  10,  10,   5,
      0,   0,   0,   0,   0,   0,   0,   0,
]

QUEEN_TABLE = [
    -20, -10, -10,  -5,  -5, -10, -10, -20,
    -10,   0,   0,   0,   0,   5,   0, -10,
    -10,   0,   5,   5,   5,   5,   5, -10,
     -5,   0,   5,   5,   5,   5,   0,  -5,
      0,   0,   5,   5,   5,   5,   0,  -5,
    -10,   5,   5,   5,   5,   5,   0, -10,
    -10,   0,   5,   0,   0,   0,   0, -10,
    -20, -10, -10,  -5,  -5, -10, -10, -20,
]

KING_TABLE_MID = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
     20,  20,   0,   0,   0,   0,  20,  20,
     20,  30,  10,   0,   0,  10,  30,  20,
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

# ── Piece values (centipawns) ─────────────────────────────────────────────────
PIECE_VALUES = {
    chess.PAWN:   100,
    chess.KNIGHT: 300,
    chess.BISHOP: 300,
    chess.ROOK:   500,
    chess.QUEEN:  900,
    chess.KING:   0,
}

endgame_material_start = PIECE_VALUES[chess.ROOK] * 2 + PIECE_VALUES[chess.BISHOP] + PIECE_VALUES[chess.KNIGHT] 

MAX_PLY = 64
Killer_Moves  = [[None,None] for _ in range(MAX_PLY)]


PAWN_CASTLE_POSITION = {
    chess.G1 : [chess.F2,chess.G2,chess.H2], #white kingside
    chess.G8 : [chess.F7,chess.G7,chess.H7], #black kingside
    chess.C1 : [chess.A2,chess.B2,chess.C2],    #White queenside
    chess.C8 : [chess.A7,chess.B7,chess.C7] #black queenside
}
KING_CASTLE_POSITION = [chess.G1,chess.G8,chess.C1,chess.C8]

ROOK_CASTLE_POSITION = { 
    chess.G1 : chess.F1, #white kingside
    chess.G8 : chess.F8, #black kingside
    chess.C1 : chess.D1, #White queenside
    chess.C8 : chess.D8 #black queenside
    }

KING_CENTER_POSITION = {chess.WHITE : [chess.D1,chess.E1,chess.D2,chess.E2],
                        chess.BLACK : [chess.D7,chess.E7,chess.D8,chess.E8]}

def KingSafety(board, color) -> float:
    score = 0
    king_sq = board.king(color)
    if board.has_castling_rights(color):
        score += 5
    if king_sq in KING_CASTLE_POSITION:
        score += 30
        if board.piece_type_at(ROOK_CASTLE_POSITION[king_sq]):
            score += 10
        for pawn_sq in PAWN_CASTLE_POSITION[king_sq]:
            if board.piece_type_at(pawn_sq) == chess.PAWN and board.color_at(pawn_sq) == color:
                score += 5
    if king_sq in KING_CENTER_POSITION[color]:
        score -= 30 
    return score

def endgame_phase_weight(material_count_withut_pawns) -> float:
    multiplier = 1 / endgame_material_start
    return 1 - min(1, material_count_withut_pawns * multiplier)

def get_pst_index(table, color, square) -> int:
    if color == chess.WHITE:
        rank = chess.square_rank(square)
        file = chess.square_file(square)
        rank = 7 - rank
        square = rank * 8 + file
    return table[square]    
    
def evaluatePST(table, pieceList, color) -> int:
    value = 0
    for i in pieceList:
        value += get_pst_index(table, color, pieceList[i])
    return value

def evaluatePSTs(board, color, endgamePhaseWeight) -> int:
    value = 0
    value += evaluatePST(PAWN_TABLE, board.pieces(chess.PAWN, color), color)
    value += evaluatePST(ROOK_TABLE, board.pieces(chess.ROOK, color), color)
    value += evaluatePST(KNIGHT_TABLE, board.pieces(chess.KNIGHT, color), color)
    value += evaluatePST(BISHOP_TABLE, board.pieces(chess.BISHOP, color),color)
    value += evaluatePST(QUEEN_TABLE, board.pieces(chess.QUEEN, color),color)


# ── Heuristic ─────────────────────────────────────────────────────────────────
def evaluate(board: chess.Board) -> float:
    """

    Material:  Sum of piece values for White minus Black.

    Score > 0  =>  White is better.
    Score < 0  =>  Black is better.
    """




    if board.is_checkmate():
        # The side to move is in checkmate — they lose
        return -99999 if board.turn == chess.WHITE else 99999
    if board.is_stalemate() or board.is_insufficient_material() or board.is_repetition(3):
        return 0

    whiteScore = 0
    blackScore = 0

    whiteMaterial, blackMaterial = 0
    for piece_type, value in PIECE_VALUES.items():
        whiteMaterial += len(board.pieces(piece_type, chess.WHITE)) * value
        blackMaterial -= len(board.pieces(piece_type, chess.BLACK)) * value

    whiteMaterialWithoutPawns = whiteMaterial - len(board.pieces(piece_type, chess.WHITE)) * PIECE_VALUES[chess.PAWN]
    blackMaterialWithoutPawns = blackMaterial - len(board.pieces(piece_type, chess.BLACK)) * PIECE_VALUES[chess.PAWN]
    whiteEndgamePhaseWeight = endgame_phase_weight(whiteMaterialWithoutPawns)
    blackEndgamePhaseWeight = endgame_phase_weight(blackMaterialWithoutPawns)
    
    # Your code goes here

     #fucntion to count legal moves for given color
    if chess.WHITE == board.turn:
        score += board.legal_moves.count() 
    else:
        score -= board.legal_moves.count()
    
    score += KingSafety(board, chess.WHITE) - KingSafety(board, chess.BLACK)

    return score

def orderMoves(board, moves, ply) -> list:
    scoreMoves=[]
    for move in moves:
        moveScore = 0
        movePieceType = board.piece_type_at(move.from_square)

        #capture oppents most valuable with our weakest
        if board.is_capture(move):
            if board.is_en_passant(move):
                capturePieceType = chess.PAWN
            else:
                capturePieceType = board.piece_type_at(move.to_square)

            moveScore = 10 * PIECE_VALUES[capturePieceType] - PIECE_VALUES[movePieceType]

        #promoting pawn is good
        if move.promotion != None:
            moveScore += PIECE_VALUES[move.promotion] 
        
        if board.gives_check(move):
            moveScore += 50

        if move in Killer_Moves[ply] and not board.is_capture(move):
            moveScore += 200
        
        #penalise moving pieces to square that is being attacked by oppenents pawn
        """""
        board.push(move)
        opponent = board.turn
        destination = move.to_square
        attackers = board.attackers(opponent,destination)

        for square in attackers:
            if board.piece_type_at(square)==chess.PAWN:
                moveScore -= PIECE_VALUES[board.piece_type_at(destination)]
                break
        board.pop()
        """
        
        scoreMoves.append((moveScore,move))
    scoreMoves.sort(key=lambda x: x[0], reverse=True)
    return [move for score, move in scoreMoves]

def SearchAllCaptures(board, alpha, beta,ply) -> float:
    best = evaluate(board)
    captureMoves = []

    if board.turn == chess.WHITE:
        if(best >= beta):
            return beta
        alpha = max(alpha, best)
    else:
        if(best <= alpha):
            return alpha
        beta = min(beta, best)
  
    for move in board.legal_moves:
        if(board.is_capture(move)):
            captureMoves.append(move)

    if not captureMoves:
        return best

    if board.turn == chess.WHITE:
        best = float('-inf')
        for move in orderMoves(board,captureMoves,ply):
            board.push(move)
            best = max(best, SearchAllCaptures(board, alpha, beta,ply))
            board.pop()
            alpha = max(alpha, best)
            if beta <= alpha:
                break       # Beta cutoff — opponent won't allow this path
        return best
    else:
        best = float('inf')
        for move in orderMoves(board,captureMoves,ply):
            board.push(move)
            best = min(best, SearchAllCaptures(board, alpha, beta,ply))
            board.pop()
            beta = min(beta, best)
            if beta <= alpha:
                break       # Alpha cutoff
        return best

# ── Minimax with Alpha-Beta Pruning ───────────────────────────────────────────
def minimax(board: chess.Board, depth: int,
            alpha: float, beta: float,
            maximizing: bool, ply: int) -> float:
    """
    Standard Minimax search with Alpha-Beta cutoffs.
    maximizing=True means we are searching for the best move for White.
    """
    if depth == 0 or board.is_game_over():
        return SearchAllCaptures(board,alpha,beta,ply)
    

    if maximizing:
        best = float('-inf')
        for move in orderMoves(board, board.legal_moves, ply):
            board.push(move)
            best = max(best, minimax(board, depth - 1, alpha, beta, False, ply + 1))
            board.pop()
            alpha = max(alpha, best)
            if beta <= alpha:
                if not board.is_capture(move) and move not in Killer_Moves[ply][0]:
                    if Killer_Moves[ply][0]:
                        Killer_Moves[ply][1] = Killer_Moves[ply][0]
                    Killer_Moves[ply][0] = move
                break       # Beta cutoff — opponent won't allow this path
        return best
    else:
        best = float('inf')
        for move in orderMoves(board, board.legal_moves, ply):
            board.push(move)
            best = min(best, minimax(board, depth - 1, alpha, beta, True, ply + 1))
            board.pop()
            beta = min(beta, best)
            if beta <= alpha:
                if not board.is_capture(move) and move not in Killer_Moves[ply][0]:
                    if Killer_Moves[ply][0]:
                        Killer_Moves[ply][1] = Killer_Moves[ply][0]
                    Killer_Moves[ply][0] = move
                break       # Alpha cutoff
        return best


# ── Entry point called by the tournament harness ──────────────────────────────
def get_next_move(board: chess.Board,
                  color: chess.Color,
                  depth: int = 3) -> chess.Move:
    """
    Return the best move for `color` from the current `board` position.
    DO NOT rename or change this signature — the harness calls it directly.
    """
    best_move  = None
    maximizing = (color == chess.WHITE)
    best_score = float('-inf') if maximizing else float('inf')

    b = board.copy()   # never modify the board passed in
    for move in orderMoves(board, b.legal_moves,0):
        b.push(move)
        score = minimax(b, depth - 1,
                        float('-inf'), float('inf'),
                        not maximizing, 0)
        b.pop()

        if maximizing and score > best_score:
            best_score, best_move = score, move
        elif not maximizing and score < best_score:
            best_score, best_move = score, move
    
    return best_move


# ── Quick self-test ───────────────────────────────────────────────────────────
if __name__ == '__main__':
    b = chess.Board()
    move = get_next_move(b, chess.WHITE, depth=3)
    print(f"[team_alpha] Opening move: {b.san(move)}")
