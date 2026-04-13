import chess
from v5 import get_next_move as v5
from v6 import get_next_move as cur



def play_match(bot_white, bot_black, depth, start_fen=None, max_plies=300):
    board = chess.Board(start_fen) if start_fen else chess.Board()

    while not board.is_game_over(claim_draw=True) and board.ply() < max_plies:
        current_bot = bot_white if board.turn == chess.WHITE else bot_black
        move = current_bot(board, board.turn, depth)

        if move not in board.legal_moves:
            return {
                "Illegal move by White" if board.turn == chess.WHITE else "Illegal move by Black",
            }

        board.push(move)
    print("result:\n", board,
    "reason: ", board.outcome(claim_draw=True))
    return board.result(claim_draw=True)
    


v5 = v5
v6 = cur

print("new model as white\n")
print(play_match(cur,v5,3))

print("new model as black\n")
print(play_match(v5,cur,3))
