import chess
import random
from math import inf

materialWorth = {chess.KING:0,
                 chess.QUEEN:90, #Queen
                 chess.ROOK:50, #Rook
                 chess.BISHOP:30, #Bishop
                 chess.KNIGHT:30, #Knight
                 chess.PAWN:10}    #Pawn


def countMaterial(board, color):
    pieceScore = 0
    for piece in materialWorth:
        pieceScore += len(board.pieces(piece, color)) * materialWorth[piece]
    return pieceScore

def evaluate(board):   

    mobilityScore = 0
    mobWeight = 3

    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -inf
        else:
            return inf
        
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    
    #responsible for counting up white and black material and returning white-black
    whiteMaterial = countMaterial(board, chess.WHITE)
    blackMaterial = countMaterial(board, chess.BLACK)
    pieceScore = whiteMaterial - blackMaterial


    #fucntion to count legal moves for given color
    def countLegalMoves(board,color):
        temp = board.copy()
        temp.turn = color
        return temp.legal_moves.count()
    
    # white-black for amount of legal moves
    mobilityScore = (countLegalMoves(board,chess.WHITE)-countLegalMoves(board,chess.BLACK)) * mobWeight
    
    score = pieceScore + mobilityScore
    return score #higher + better for white, negative score better for black

def orderMoves(board, moves):
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

            moveScore = 10 * materialWorth[capturePieceType] - materialWorth[movePieceType]

        #promoting pawn is good
        if move.promotion != None:
            moveScore += materialWorth[move.promotion] 
        
        if board.gives_check(move):
            moveScore += 50
        
        #penalise moving pieces to square that is being attacked by oppenents pawn
        board.push(move)
        opponent = board.turn
        destination = move.to_square
        attackers = board.attackers(opponent,destination)

        for square in attackers:
            if board.piece_type_at(square)==chess.PAWN:
                moveScore -= materialWorth[board.piece_type_at(destination)]
                break
        board.pop()
        
        scoreMoves.append((moveScore,move))
    scoreMoves.sort(key=lambda x: x[0], reverse=True)
    return [move for score, move in scoreMoves]
            



def minimax(board,depth,alpha,beta,maximizingPlayer):

    if depth == 0:
        return evaluate(board)
    
    if maximizingPlayer:
        maxEval = -inf
        
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board,depth-1,alpha,beta,False)
            maxEval = max(maxEval,eval)
            alpha = max(alpha,eval)
            board.pop()
            if beta<=alpha:
                break
            
        return maxEval
    else:
        minEval = +inf
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board,depth-1,alpha,beta,True)
            minEval = min(minEval,eval)
            beta = min(beta,eval)
            board.pop()
            if beta<=alpha:
                break
        return minEval
    
def get_next_move(board,color,depth):
    moves = list(orderMoves(board, board.legal_moves))
    bestMove = moves[0]

    maximizing = (color == chess.WHITE)
    if maximizing:
        bestScore = -inf
    else:
        bestScore = inf

    for move in moves:
        board.push(move)
        score = minimax(board,depth-1,-inf,+inf,not maximizing)
        board.pop()

        if (maximizing and score > bestScore) or ((not maximizing) and score < bestScore): 
            bestScore = score
            bestMove = move
    print("v3:", bestMove)       
    return bestMove



