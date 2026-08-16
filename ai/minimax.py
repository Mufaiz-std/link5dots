import math
from game.board import Board
from ai.evaluation import evaluate_board
from game.rules import check_win

def get_candidate_moves(board):
    """
    Returns a list of interesting moves to consider.
    We only consider cells that are adjacent (within distance 2) to existing pieces.
    """
    if board.piece_count[Board.PLAYER_1] == 0 and board.piece_count[Board.PLAYER_2] == 0:
        return [(board.rows // 2, board.cols // 2)]
        
    candidates = set()
    for r in range(board.rows):
        for c in range(board.cols):
            if board.grid[r][c] != Board.EMPTY:
                for dr in range(-2, 3):
                    for dc in range(-2, 3):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < board.rows and 0 <= nc < board.cols:
                            if board.grid[nr][nc] == Board.EMPTY:
                                candidates.add((nr, nc))
    return list(candidates)

def minimax(board, depth, alpha, beta, maximizing_player, current_player, cpu_player):
    opponent = Board.PLAYER_1 if current_player == Board.PLAYER_2 else Board.PLAYER_2
    
    # Check for terminal states (win/draw) before generating moves
    # Actually checking win for the whole board on every node is slow, 
    # but we can rely on depth and evaluation.
    
    if depth == 0 or board.is_full():
        return evaluate_board(board, cpu_player), None

    candidates = get_candidate_moves(board)
    if not candidates:
        return evaluate_board(board, cpu_player), None
        
    best_move = None
    
    if maximizing_player:
        max_eval = -math.inf
        for r, c in candidates:
            board.grid[r][c] = current_player
            winner, _ = check_win(board, r, c)
            if winner == current_player:
                eval_score = 1000000 + depth # Prefer faster wins
            else:
                eval_score, _ = minimax(board, depth - 1, alpha, beta, False, opponent, cpu_player)
                
            board.grid[r][c] = Board.EMPTY
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (r, c)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for r, c in candidates:
            board.grid[r][c] = current_player
            winner, _ = check_win(board, r, c)
            if winner == current_player:
                eval_score = -1000000 - depth # Opponent wins
            else:
                eval_score, _ = minimax(board, depth - 1, alpha, beta, True, opponent, cpu_player)
                
            board.grid[r][c] = Board.EMPTY
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (r, c)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move
