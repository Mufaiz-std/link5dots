from game.board import Board

def evaluate_board(board, cpu_player):
    """
    Evaluates the board from the perspective of `cpu_player`.
    Positive score means cpu_player is winning, negative means opponent is winning.
    """
    opponent = Board.PLAYER_1 if cpu_player == Board.PLAYER_2 else Board.PLAYER_2
    
    score = 0
    score += evaluate_lines(board, cpu_player)
    score -= evaluate_lines(board, opponent)
    return score

def evaluate_lines(board, player):
    score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    # Very basic heuristic: count lengths of lines
    # To optimize, in a real gomoku engine you'd evaluate windows of 5.
    
    # We will evaluate all windows of 5 cells.
    for r in range(board.rows):
        for c in range(board.cols):
            for dr, dc in directions:
                # Check if window of 5 fits
                if 0 <= r + 4*dr < board.rows and 0 <= c + 4*dc < board.cols:
                    pieces = 0
                    empty = 0
                    for i in range(5):
                        cell = board.grid[r + i*dr][c + i*dc]
                        if cell == player:
                            pieces += 1
                        elif cell == Board.EMPTY:
                            empty += 1
                    
                    if pieces + empty == 5:
                        # Only our pieces and empty cells in this window
                        if pieces == 5:
                            score += 100000
                        elif pieces == 4:
                            score += 1000
                        elif pieces == 3:
                            score += 100
                        elif pieces == 2:
                            score += 10
                        elif pieces == 1:
                            score += 1
    return score
