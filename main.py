import os
# Prevent Kivy from parsing command line args when running script
os.environ["KIVY_NO_ARGS"] = "1"

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.clock import Clock
from kivy.metrics import dp

from ui.screens import HomeScreen, SetupScreen, GameScreen, SettingsScreen, ResultScreen
from ui.components import PALETTE, ConfirmDialog
from game.board import Board
from game.game_state import GameState
from game.moves import MoveHistory
from game.rules import check_win, check_draw

import threading

class Link5DotsApp(App):
    def build(self):
        Window.clearcolor = PALETTE['screen_bg']
        Window.bind(on_keyboard=self.on_keyboard)
        
        self.game_state = GameState()
        self.board = Board()
        self.move_history = MoveHistory()
        
        self.sm = ScreenManager(transition=SlideTransition())
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(SetupScreen(name='setup'))
        self.sm.add_widget(GameScreen(name='game'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.add_widget(ResultScreen(name='result'))
        
        self.sm.app = self
        
        return self.sm

    def start_new_game(self, reroll_random=False):
        self.game_state.setup_new_game(reroll_random)
        self.board = Board(self.game_state.board_rows, self.game_state.board_cols)
        self.move_history.clear()
        
        game_screen = self.sm.get_screen('game')
        if hasattr(game_screen, 'board_view'):
            game_screen.board_view.board = self.board
            game_screen.board_view.game_state = self.game_state
            
        self.sm.transition.direction = 'left'
        self.sm.current = 'game'
        
        # If CPU goes first
        if self.game_state.mode == GameState.MODE_CPU and self.game_state.current_player == Board.PLAYER_2:
            self.trigger_cpu_move()

    def handle_player_move(self, r, c):
        if self.game_state.is_game_over() or self.game_state.cpu_thinking:
            return
            
        # In CPU mode, only player 1 can move manually
        if self.game_state.mode == GameState.MODE_CPU and self.game_state.current_player == Board.PLAYER_2:
            return

        self._execute_move(r, c)
        
        if not self.game_state.is_game_over():
            if self.game_state.mode == GameState.MODE_CPU and self.game_state.current_player == Board.PLAYER_2:
                self.trigger_cpu_move()

    def _execute_move(self, r, c):
        player = self.game_state.current_player
        if self.board.place_piece(r, c, player):
            self.move_history.push(r, c, player)
            
            # Sound/haptic
            game_screen = self.sm.get_screen('game')
            game_screen.board_view.play_sound()
            game_screen.board_view.play_haptic()
            
            # Check win
            winner, win_line = check_win(self.board, r, c)
            if winner:
                self.game_state.winner = winner
                self.game_state.win_line = win_line
                self.show_result('win' if winner == self.game_state._actual_first_player or self.game_state.mode == GameState.MODE_PVP else 'lose')
            elif check_draw(self.board):
                self.game_state.is_draw = True
                self.show_result('draw')
            else:
                self.game_state.switch_turn()
            
            game_screen.update_ui()

    def trigger_cpu_move(self):
        self.game_state.cpu_thinking = True
        self.sm.get_screen('game').update_ui()
        
        # Run AI on background thread
        threading.Thread(target=self._cpu_worker, daemon=True).start()

    def _cpu_worker(self):
        from ai.easy_ai import get_easy_move
        from ai.hard_ai import get_hard_move
        
        if self.game_state.difficulty == GameState.DIFF_EASY:
            move = get_easy_move(self.board, Board.PLAYER_2)
        else:
            move = get_hard_move(self.board, Board.PLAYER_2)
            
        Clock.schedule_once(lambda dt: self._apply_cpu_move(move))

    def _apply_cpu_move(self, move):
        self.game_state.cpu_thinking = False
        if move:
            r, c = move
            self._execute_move(r, c)
        else:
            # Fallback if AI fails to find move
            pass
        self.sm.get_screen('game').update_ui()

    def handle_undo(self):
        if self.game_state.cpu_thinking or self.game_state.is_game_over() or self.move_history.count() == 0:
            return
            
        if self.game_state.mode == GameState.MODE_PVP:
            # Pop 1
            last = self.move_history.pop()
            if last:
                self.board.remove_piece(last[0], last[1])
                self.game_state.switch_turn()
        else:
            # Pop 2 (player + CPU), unless only 1 move exists (CPU went first)
            if self.move_history.count() == 1:
                last = self.move_history.pop()
                self.board.remove_piece(last[0], last[1])
                self.game_state.switch_turn()
            else:
                last1 = self.move_history.pop()
                if last1:
                    self.board.remove_piece(last1[0], last1[1])
                last2 = self.move_history.pop()
                if last2:
                    self.board.remove_piece(last2[0], last2[1])
                # Turn shouldn't switch since we popped both CPU and Player

        self.game_state.winner = None
        self.game_state.win_line = None
        self.game_state.is_draw = False
        self.sm.get_screen('game').update_ui()

    def handle_back(self):
        # Triggered by on-screen back button or Android back button
        if self.sm.current == 'game':
            if self.move_history.count() > 0:
                dialog = ConfirmDialog("Game will be lost.", lambda: self.go_home())
                dialog.open()
            else:
                self.go_home()
        elif self.sm.current in ['setup', 'settings']:
            self.go_home()

    def prompt_restart(self):
        if self.move_history.count() > 0:
            dialog = ConfirmDialog("Restart game?", lambda: self.start_new_game())
            dialog.open()
        else:
            self.start_new_game()

    def go_home(self):
        self.sm.transition.direction = 'right'
        self.sm.current = 'home'

    def show_result(self, outcome):
        def transition_to_result(dt):
            result_screen = self.sm.get_screen('result')
            result_screen.setup_result(outcome, self.game_state)
            self.sm.transition.direction = 'left'
            self.sm.current = 'result'
        # Delay slightly so user sees the winning piece/line before transition
        Clock.schedule_once(transition_to_result, 1.5)

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if key == 27: # ESC or Android Back button
            self.handle_back()
            return True # Consume event
        return False

if __name__ == '__main__':
    Link5DotsApp().run()
