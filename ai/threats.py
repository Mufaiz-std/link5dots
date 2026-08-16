from game.board import Board

def find_immediate_win(board, player):
    # Returns (r, c) if there's a move that wins immediately for `player`
    from game.rules import check_win
    for r in range(board.rows):
        for c in range(board.cols):
            if board.grid[r][c] == Board.EMPTY:
                board.grid[r][c] = player
                winner, _ = check_win(board, r, c)
                board.grid[r][c] = Board.EMPTY
                if winner == player:
                    return (r, c)
    return None

def find_open_threats(board, player, length=4):
    # A simplified threat finder: looks for an open-ended line of `length` 
    # without blocked ends. Very basic implementation for Easy AI.
    # Hard AI will use evaluation instead.
    
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    threats = []
    
    for r in range(board.rows):
        for c in range(board.cols):
            if board.grid[r][c] == Board.EMPTY:
                # check if placing a piece here completes a threat of `length`
                for dr, dc in directions:
                    count = 1
                    open_ends = 0
                    
                    # Forward
                    r_curr, c_curr = r + dr, c + dc
                    while 0 <= r_curr < board.rows and 0 <= c_curr < board.cols and board.grid[r_curr][c_curr] == player:
                        count += 1
                        r_curr += dr
                        c_curr += dc
                    if 0 <= r_curr < board.rows and 0 <= c_curr < board.cols and board.grid[r_curr][c_curr] == Board.EMPTY:
                        open_ends += 1

                    # Backward
                    r_curr, c_curr = r - dr, c - dc
                    while 0 <= r_curr < board.rows and 0 <= c_curr < board.cols and board.grid[r_curr][c_curr] == player:
                        count += 1
                        r_curr -= dr
                        c_curr -= dc
                    if 0 <= r_curr < board.rows and 0 <= c_curr < board.cols and board.grid[r_curr][c_curr] == Board.EMPTY:
                        open_ends += 1
                        
                    if count >= length and open_ends > 0:
                        threats.append((r, c))
                        break # No need to check other directions for this cell to be considered a threat block/make
    return threats

