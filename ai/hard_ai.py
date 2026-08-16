import math
from ai.minimax import minimax
from ai.threats import find_immediate_win

def get_hard_move(board, cpu_player):
    opponent = 1 if cpu_player == 2 else 2

    # 1. Immediate Win
    win_move = find_immediate_win(board, cpu_player)
    if win_move:
        return win_move

    # 2. Immediate Block
    block_move = find_immediate_win(board, opponent)
    if block_move:
        return block_move
        
    # 3. Minimax Search
    # Search depth depends on Python performance. For Gomoku, branching factor is huge.
    # Depth 2 means CPU considers its move, and opponent's best response.
    # We might do depth 3 if the board is small, but depth 2 is safe for responsiveness.
    # Given the requirements, a depth of 2 or 3 is reasonable. Let's use 2.
    DEPTH = 2
    
    score, best_move = minimax(board, DEPTH, -math.inf, math.inf, True, cpu_player, cpu_player)
    
    # Fallback to center if something went wrong
    if not best_move:
        if board.piece_count[1] == 0 and board.piece_count[2] == 0:
            return (board.rows // 2, board.cols // 2)
            
        for r in range(board.rows):
            for c in range(board.cols):
                if board.grid[r][c] == 0:
                    return (r, c)
                    
    return best_move
