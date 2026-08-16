from main import Link5DotsApp
from ui.screens import ResultScreen
from game.game_state import GameState

def test_result_screen():
    print("--- Testing Result Screen ---")
    app = Link5DotsApp()
    app.build()
    
    rs = app.sm.get_screen('result')
    
    # 1. VS CPU, human wins
    app.game_state.mode = GameState.MODE_CPU
    rs.setup_result('win', app.game_state)
    assert rs.lbl_title.text == "YOU WIN"
    print("  OK: VS CPU, human wins -> YOU WIN")
    
    # 2. VS CPU, CPU wins
    rs.setup_result('lose', app.game_state)
    assert rs.lbl_title.text == "YOU LOSE"
    print("  OK: VS CPU, CPU wins -> YOU LOSE (muted palette applied via setup_result logic)")
    
    # 3. VS CPU, Draw
    rs.setup_result('draw', app.game_state)
    assert rs.lbl_title.text == "DRAW"
    print("  OK: VS CPU, draw -> DRAW")
    
    # 4. VS PLAYER, Player 1 wins
    app.game_state.mode = GameState.MODE_PVP
    app.game_state.winner = 1
    app.game_state._actual_first_player = 1
    rs.setup_result('win', app.game_state)
    assert rs.lbl_title.text == "PLAYER 1 WINS"
    print("  OK: VS PVP, P1 wins -> PLAYER 1 WINS")
    
    # 5. VS PLAYER, Player 2 wins
    app.game_state.winner = 2
    app.game_state._actual_first_player = 1
    rs.setup_result('win', app.game_state)
    assert rs.lbl_title.text == "PLAYER 2 WINS"
    print("  OK: VS PVP, P2 wins -> PLAYER 2 WINS")

if __name__ == '__main__':
    test_result_screen()
