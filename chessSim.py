import chess
from bobbyV1 import get_random_move as vR, get_next_move as v1
from bobbyV2 import get_next_move as v2
from bobbyV3 import get_next_move as v3
from bobbyV4 import get_next_move as v4
from team_alphaV4 import get_next_move as Ba



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
    

bobbyV1 = v1
bobbyV2 = v2
bobbyV3 = v3
bobbyV4 = v4
team_alphaV4 = Ba

bobbyVR = vR

print("new model as white\n")
print(play_match(v4,Ba,3))

print("new model as black\n")
print(play_match(Ba,v4,3))
