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

def is_deadlocked(board):
    """
    Checks if a win is impossible for both players because every possible
    line of 5 contains at least one piece of each color.
    """
    for r in range(board.rows):
        for c in range(board.cols):
            # check horizontal (right)
            if c + 4 < board.cols:
                if not _is_blocked(board, [(r, c+i) for i in range(5)]):
                    return False
            # check vertical (down)
            if r + 4 < board.rows:
                if not _is_blocked(board, [(r+i, c) for i in range(5)]):
                    return False
            # check diagonal (down-right)
            if r + 4 < board.rows and c + 4 < board.cols:
                if not _is_blocked(board, [(r+i, c+i) for i in range(5)]):
                    return False
            # check diagonal (down-left)
            if r + 4 < board.rows and c - 4 >= 0:
                if not _is_blocked(board, [(r+i, c-i) for i in range(5)]):
                    return False
    return True

def _is_blocked(board, line_coords):
    has_p1 = False
    has_p2 = False
    for r, c in line_coords:
        p = board.get_cell(r, c)
        if p == Board.PLAYER_1:
            has_p1 = True
        elif p == Board.PLAYER_2:
            has_p2 = True
    return has_p1 and has_p2

