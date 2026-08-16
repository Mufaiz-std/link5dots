import time
import random
from game.board import Board
from game.rules import check_win, check_draw
from ai.easy_ai import get_easy_move
from ai.hard_ai import get_hard_move

def test_easy_ai():
    print("--- Testing Easy AI (20 games) ---")
    crashes = 0
    illegal = 0
    wins = 0
    draws = 0
    
    for game in range(20):
        b = Board(15, 15)
        current = 1
        while True:
            move = get_easy_move(b, current)
            if not move:
                break
            
            # check illegal
            if not b.is_valid_move(move[0], move[1]):
                illegal += 1
                break
                
            b.place_piece(move[0], move[1], current)
            winner, _ = check_win(b, move[0], move[1])
            if winner:
                wins += 1
                break
            if check_draw(b):
                draws += 1
                break
            
            current = 2 if current == 1 else 1
            
    print(f"Results: {wins} wins, {draws} draws, {crashes} crashes, {illegal} illegal moves.")
    assert crashes == 0 and illegal == 0, "Easy AI failed reliability test."
    
def test_hard_ai():
    print("--- Testing Hard AI ---")
    b = Board(20, 20)
    
    # Check block 4
    for i in range(4):
        b.place_piece(10, i, 1)
    
    start_t = time.time()
    move = get_hard_move(b, 2)
    end_t = time.time()
    
    assert move == (10, 4), f"Hard AI failed to block open 4. Made move {move}"
    print(f"  OK: Hard AI blocked 4 correctly.")
    print(f"  OK: Hard AI took {end_t - start_t:.4f} seconds on 20x20.")
    assert end_t - start_t < 5.0, "Hard AI is too slow."

if __name__ == "__main__":
    test_easy_ai()
    test_hard_ai()
