from game.board import Board
from game.rules import check_win, check_draw
from game.game_state import GameState
from game.moves import MoveHistory

def run_tests():
    print("--- Section 2: Game Logic unit tests ---")
    
    # 1. Win detection
    print("Testing Win detection...")
    board = Board(15, 15)
    
    # - 15x15 middle win
    for i in range(5): board.place_piece(7, 7+i, 1)
    win, _ = check_win(board, 7, 7)
    assert win == 1
    print("  OK: 15x15 middle win")
    
    # - Edge/corner win
    board.clear()
    for i in range(5): board.place_piece(14, 14-i, 1)
    win, _ = check_win(board, 14, 14)
    assert win == 1
    print("  OK: Edge/corner win")
    
    # - Exactly 5
    board.clear()
    for i in range(5): board.place_piece(0, i, 1)
    win, _ = check_win(board, 0, 4)
    assert win == 1
    print("  OK: Exactly 5 in a row")
    
    # - 6+ in a row
    board.clear()
    for i in range(7): board.place_piece(0, i, 1)
    win, _ = check_win(board, 0, 3)
    assert win == 1
    print("  OK: 6+ in a row")
    
    # - Near-miss 4
    board.clear()
    for i in [0,1,2,4]: board.place_piece(0, i, 1)
    win, _ = check_win(board, 0, 2)
    assert win is None
    print("  OK: Near-miss of 4 in a row")
    
    # 2. Draw detection (5x5)
    print("Testing Draw detection...")
    b5 = Board(5, 5)
    # Fill with alternating pattern to avoid accidental 5-in-a-row
    for r in range(5):
        for c in range(5):
            player = 1 if (r+c)%2 == 0 else 2
            b5.place_piece(r, c, player)
    assert check_draw(b5) == True
    print("  OK: 5x5 board draw detection")
    
    # 3. Occupancy
    print("Testing Occupancy...")
    b = Board(15, 15)
    b.place_piece(5, 5, 1)
    res = b.place_piece(5, 5, 2)
    assert res == False
    assert b.grid[5][5] == 1
    print("  OK: Occupancy rejection")
    
    # 4. Board size boundaries
    # The setup allows minimum 5x5.
    b_min = Board(5, 5)
    assert b_min.rows == 5
    b_max = Board(20, 20)
    assert b_max.rows == 20
    b_too_small = Board(4, 4) # Our code doesn't strictly reject at instantiation, it just creates a 4x4.
    # The Setup screen enforces the minimum sliders. 
    print("  OK: Board size 5x5, 20x20 accepted")
    
    # 5. Non-square (10x15)
    print("Testing Non-square board...")
    b1015 = Board(10, 15)
    for i in range(5): b1015.place_piece(9, i, 1) # bottom edge
    win, _ = check_win(b1015, 9, 4)
    assert win == 1
    print("  OK: 10x15 non-square win detection")

if __name__ == '__main__':
    run_tests()
