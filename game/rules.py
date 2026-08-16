from game.board import Board

def check_win(board, r, c):
    """
    Checks if the piece placed at (r, c) results in a win (5 in a row).
    Returns a tuple (winning_player, list_of_winning_cells) if win, else (None, None).
    """
    player = board.get_cell(r, c)
    if player == Board.EMPTY or player is None:
        return None, None

    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal \
        (1, -1)   # Diagonal /
    ]

    for dr, dc in directions:
        line = [(r, c)]
        
        # Check forward direction
        r_curr, c_curr = r + dr, c + dc
        while 0 <= r_curr < board.rows and 0 <= c_curr < board.cols and board.get_cell(r_curr, c_curr) == player:
            line.append((r_curr, c_curr))
            r_curr += dr
            c_curr += dc
            
        # Check backward direction
        r_curr, c_curr = r - dr, c - dc
        while 0 <= r_curr < board.rows and 0 <= c_curr < board.cols and board.get_cell(r_curr, c_curr) == player:
            line.append((r_curr, c_curr))
            r_curr -= dr
            c_curr -= dc
            
        if len(line) >= 5:
            # Sort the line visually from top-left to bottom-right (or bottom-left) to draw nicely
            line.sort(key=lambda x: (x[0], x[1]))
            return player, line

    return None, None

def check_draw(board):
    return board.is_full()
