import random
from game.board import Board
from ai.threats import find_immediate_win, find_open_threats

def get_easy_move(board, cpu_player):
    opponent = Board.PLAYER_1 if cpu_player == Board.PLAYER_2 else Board.PLAYER_2

    # 1. Can we win immediately?
    win_move = find_immediate_win(board, cpu_player)
    if win_move:
        return win_move

    # 2. Must we block opponent from winning immediately?
    block_move = find_immediate_win(board, opponent)
    if block_move:
        return block_move

    # 3. Can we create/block an open-ended threat of 4 or 3?
    # Block opponent's 4
    threats_4 = find_open_threats(board, opponent, length=4)
    if threats_4:
        return random.choice(threats_4)
        
    # Block opponent's 3
    threats_3 = find_open_threats(board, opponent, length=3)
    if threats_3:
        return random.choice(threats_3)
        
    # Make our own 3
    my_3 = find_open_threats(board, cpu_player, length=3)
    if my_3:
        return random.choice(my_3)

    # 4. Fallback: play near existing pieces, or center if empty
    candidates = []
    if board.piece_count[Board.PLAYER_1] == 0 and board.piece_count[Board.PLAYER_2] == 0:
        return (board.rows // 2, board.cols // 2)
        
    for r in range(board.rows):
        for c in range(board.cols):
            if board.grid[r][c] == Board.EMPTY:
                # Check adjacent cells for any pieces
                has_neighbor = False
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0: continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < board.rows and 0 <= nc < board.cols:
                            if board.grid[nr][nc] != Board.EMPTY:
                                has_neighbor = True
                                break
                    if has_neighbor: break
                if has_neighbor:
                    candidates.append((r, c))

    if candidates:
        return random.choice(candidates)
        
    # Utter fallback (should rarely happen unless weird board shapes)
    for r in range(board.rows):
        for c in range(board.cols):
            if board.grid[r][c] == Board.EMPTY:
                return (r, c)
    return None
