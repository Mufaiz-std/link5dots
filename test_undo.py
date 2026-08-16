from main import Link5DotsApp
from game.game_state import GameState
from game.board import Board

def test_undo():
    print("--- Testing Undo/Restart Logic ---")
    app = Link5DotsApp()
    app.build()
    
    # 1. VS CPU, CPU went first
    app.game_state.mode = GameState.MODE_CPU
    app.game_state.who_goes_first_setting = GameState.FIRST_P2
    app.start_new_game() # Triggers CPU move
    app.sm.get_screen('game').on_enter()
    # Need to simulate CPU worker manually since threading is skipped headless
    app._apply_cpu_move((5, 5)) 
    
    assert app.move_history.count() == 1
    assert app.board.piece_count[Board.PLAYER_2] == 1
    
    # Player hits undo
    app.handle_undo()
    assert app.move_history.count() == 0
    assert app.board.piece_count[Board.PLAYER_2] == 0
    print("  OK: VS CPU, CPU-went-first: Undo removes only 1 move")
    
    # 2. VS CPU, normal case (player went first)
    app.game_state.who_goes_first_setting = GameState.FIRST_P1
    app.start_new_game()
    app.handle_player_move(0, 0)
    app._apply_cpu_move((1, 1))
    
    assert app.move_history.count() == 2
    app.handle_undo()
    assert app.move_history.count() == 0
    print("  OK: VS CPU, normal case: Undo removes both player and CPU move")
    
    # 3. Disabled during CPU thinking
    app.start_new_game()
    app.game_state.cpu_thinking = True
    app.handle_player_move(0, 0) # Fake move just to add one
    app.move_history.push(0, 0, 1)
    
    app.handle_undo()
    assert app.move_history.count() == 1 # Was not removed
    print("  OK: Undo is disabled and ignored while CPU is thinking")

if __name__ == '__main__':
    test_undo()
