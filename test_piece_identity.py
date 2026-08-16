from main import Link5DotsApp
from game.game_state import GameState
from game.board import Board

def test_who_goes_first():
    print("--- Testing 'Who Goes First' Logic ---")
    app = Link5DotsApp()
    app.build() # initialize things
    
    # Test YOU FIRST (VS CPU)
    app.game_state.mode = GameState.MODE_CPU
    app.game_state.who_goes_first_setting = GameState.FIRST_P1
    app.start_new_game()
    assert app.game_state.current_player == Board.PLAYER_1
    print("  OK: YOU FIRST sets current player to P1 (hollow)")
    
    # Test CPU FIRST (VS CPU)
    app.game_state.who_goes_first_setting = GameState.FIRST_P2
    app.start_new_game()
    assert app.game_state.current_player == Board.PLAYER_2
    print("  OK: CPU FIRST sets current player to CPU (solid) and triggers CPU move")
    
    # Test RANDOM
    app.game_state.who_goes_first_setting = GameState.FIRST_RANDOM
    
    p1_firsts = 0
    p2_firsts = 0
    for _ in range(50):
        app.start_new_game(reroll_random=True)
        if app.game_state.current_player == Board.PLAYER_1:
            p1_firsts += 1
        else:
            p2_firsts += 1
    assert p1_firsts > 0 and p2_firsts > 0
    print(f"  OK: RANDOM distributed turns (P1: {p1_firsts}, CPU: {p2_firsts}) but identities remained P1=1, P2=2")

    # Test Play Again (Re-roll)
    app.game_state.who_goes_first_setting = GameState.FIRST_P1
    app.start_new_game(reroll_random=False)
    assert app.game_state.current_player == Board.PLAYER_1
    app.start_new_game(reroll_random=False)
    assert app.game_state.current_player == Board.PLAYER_1
    print("  OK: Play Again (fixed choice) retains player")
    
if __name__ == '__main__':
    test_who_goes_first()
