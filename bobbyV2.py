import chess
import random
from math import inf

materialWorth = {chess.KING:0,
                 chess.QUEEN:90, #Queen
                 chess.ROOK:50, #Rook
                 chess.BISHOP:30, #Bishop
                 chess.KNIGHT:30, #Knight
                 chess.PAWN:10}    #Pawn




def evalaute(board):   

    pieceScore = 0
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
    for piece in materialWorth:                     #rewards pieces
        squares = board.pieces(piece,chess.WHITE)
        pieceScore += len(squares) * materialWorth[piece]

    for piece in materialWorth:
        squares = board.pieces(piece,chess.BLACK)
        pieceScore -= len(squares) * materialWorth[piece]

    #fucntion to count legal moves for given color
    def countLegalMoves(board,color):
        temp = board.copy()
        temp.turn = color
        return temp.legal_moves.count()
    
    # white-black for amount of legal moves
    mobilityScore = (countLegalMoves(board,chess.WHITE)-countLegalMoves(board,chess.BLACK)) * mobWeight
    
    score = pieceScore + mobilityScore
    return score #higher + better for white, negative score better for black



def minimax(board,depth,alpha,beta,maximizingPlayer):

    if depth == 0 or board.is_game_over():
        return evalaute(board)
    
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
    moves = list(board.legal_moves)
    bestMove = moves[0]

    if board.is_game_over():
        return None
    
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
    print("v2:", bestMove)        
    return bestMove


