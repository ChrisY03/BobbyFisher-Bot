"""
team_alpha.py  —  Chess Bot using Minimax + Alpha-Beta Pruning
Heuristic: Material value

Install dependency:  pip install python-chess
"""

import chess

# ── Piece values (centipawns) ─────────────────────────────────────────────────
PIECE_VALUES = {
    chess.PAWN:   10,
    chess.KNIGHT: 30,
    chess.BISHOP: 30,
    chess.ROOK:   50,
    chess.QUEEN:  90,
    chess.KING:   0,
}

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
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    # ── Example Heuristic ─────────────────────────────────────────────────────────
    # The evaluation function counts the number of pieces White has minus the number
    # of pieces Black has, multiplied by a value of 1.

    # In the minimax algorithm, this evaluation is applied at the leaf nodes and
    # reflects the advantage of one player over the other. A positive score means
    # White is in a better position, while a negative score indicates that Black
    # is ahead.

    # The algorithm itself does not need to care about the player's colour,
    # because the evaluation function already represents the position from
    # both players' perspectives.

    score = 0
    for piece_type, value in PIECE_VALUES.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value

    # Your code goes here

     #fucntion to count legal moves for given color
    mobWeight = 2
    if chess.WHITE == board.turn:
        mobilityScore = board.legal_moves.count() * mobWeight
    else:
        mobilityScore = -board.legal_moves.count() * mobWeight

    score += mobilityScore

    return score

def orderMoves(board, moves) -> list:
    scoreMoves=[]
    for move in moves:
        moveScore = 0
        movePieceType = board.piece_type_at(move.from_square)
        capturePieceType = board.is_capture(move)

        #capture oppents most valauable with our weakest
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
        
        #penalise moving pieces to square that is being attacked by oppenents pawn
        board.push(move)
        opponent = board.turn
        destination = move.to_square
        attackers = board.attackers(opponent,destination)

        for square in attackers:
            if board.piece_type_at(square)==chess.PAWN:
                moveScore -= PIECE_VALUES[board.piece_type_at(destination)]
                break
        board.pop()
        
        scoreMoves.append((moveScore,move))
    scoreMoves.sort(key=lambda x: x[0], reverse=True)
    return [move for score, move in scoreMoves]

def SearchAllCaptures(board, alpha, beta) -> float:
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
        for move in orderMoves(board,captureMoves):
            board.push(move)
            best = max(best, SearchAllCaptures(board, alpha, beta))
            board.pop()
            alpha = max(alpha, best)
            if beta <= alpha:
                break       # Beta cutoff — opponent won't allow this path
        return best
    else:
        best = float('inf')
        for move in orderMoves(board,captureMoves):
            board.push(move)
            best = min(best, SearchAllCaptures(board, alpha, beta))
            board.pop()
            beta = min(beta, best)
            if beta <= alpha:
                break       # Alpha cutoff
        return best

# ── Minimax with Alpha-Beta Pruning ───────────────────────────────────────────
def minimax(board: chess.Board, depth: int,
            alpha: float, beta: float,
            maximizing: bool) -> float:
    """
    Standard Minimax search with Alpha-Beta cutoffs.
    maximizing=True means we are searching for the best move for White.
    """
    if depth == 0 or board.is_game_over():
        return SearchAllCaptures(board,alpha,beta)

    if maximizing:
        best = float('-inf')
        for move in orderMoves(board, board.legal_moves):
            board.push(move)
            best = max(best, minimax(board, depth - 1, alpha, beta, False))
            board.pop()
            alpha = max(alpha, best)
            if beta <= alpha:
                break       # Beta cutoff — opponent won't allow this path
        return best
    else:
        best = float('inf')
        for move in orderMoves(board, board.legal_moves):
            board.push(move)
            best = min(best, minimax(board, depth - 1, alpha, beta, True))
            board.pop()
            beta = min(beta, best)
            if beta <= alpha:
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
    for move in orderMoves(board, b.legal_moves):
        b.push(move)
        score = minimax(b, depth - 1,
                        float('-inf'), float('inf'),
                        not maximizing)
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
