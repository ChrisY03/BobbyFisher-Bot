import chess
import random
from math import inf

materialWorth = {chess.KING:900,
                 chess.QUEEN:90, #Queen
                 chess.ROOK:50, #Rook
                 chess.BISHOP:30, #Bishop
                 chess.KNIGHT:30, #Knight
                 chess.PAWN:10}    #Pawn


#This version only accpunts for the potential material loss when evaulting its next move, so it seeks to retain as many pieces a possible

def evalaute(board):   
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -900
        else:
            return 900
        
    if board.is_stalemate():
        return 0
    
    score = 0
    for piece in materialWorth:
        squares = board.pieces(piece,chess.WHITE)
        score += len(squares) * materialWorth[piece]

    for piece in materialWorth:
        squares = board.pieces(piece,chess.BLACK)
        score -= len(squares) * materialWorth[piece]
    
    return score

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
    if board.is_game_over():
        return None
    
    if color == chess.WHITE:
        bestScore = -inf
        for move in moves:
            board.push(move)
            currentScore = minimax(board,depth-1,+inf,-inf,False)
            if currentScore > bestScore:
                bestScore = currentScore
                bestMove = move
            board.pop()
    else:
        bestScore = +inf
        for move in moves:
            board.push(move)
            currentScore = minimax(board,depth-1,-inf,+inf,True)
            if currentScore < bestScore:
                bestScore = currentScore
                bestMove = move
            board.pop()
            
    return bestMove

def get_random_move(board,depth,color):
    moves = list(board.legal_moves)
    moveAmount = board.legal_moves.count()
    randomMove =  moves[int(random.random()*moveAmount)]
    return randomMove


