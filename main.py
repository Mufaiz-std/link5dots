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

    def start_new_game(self, reroll_random=True):
        self.game_state.setup_new_game(reroll_random)
        self.board = Board(self.game_state.board_rows, self.game_state.board_cols)
        self.move_history.clear()
        self.game_state.deadlock_prompted = False
        
        game_screen = self.sm.get_screen('game')
        if hasattr(game_screen, 'board_view'):
            game_screen.board_view.board = self.board
            game_screen.board_view.game_state = self.game_state
            
        self.sm.transition.direction = 'left'
        self.sm.current = 'game'
        game_screen.update_ui()
        
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

    def _execute_move(self, r, c):
        player = self.game_state.current_player
        if self.board.place_piece(r, c, player):
            self.move_history.push(r, c, player)
            
            # Sound/haptic
            game_screen = self.sm.get_screen('game')
            if hasattr(game_screen, 'board_view'):
                game_screen.board_view.play_sound()
                game_screen.board_view.play_haptic()
            from game.rules import check_win, check_draw
            winner, win_line = check_win(self.board, r, c)
            if winner:
                self.game_state.winner = winner
                self.game_state.win_line = win_line
                if self.game_state.mode == GameState.MODE_PVP:
                    outcome = 'win'
                else:
                    outcome = 'win' if winner == Board.PLAYER_1 else 'lose'
                self.show_result(outcome)
                game_screen.update_ui()
                return
            elif check_draw(self.board):
                self.game_state.is_draw = True
                self.show_result('draw')
                game_screen.update_ui()
                return
                
            from game.rules import is_deadlocked
            if not getattr(self.game_state, 'deadlock_prompted', False) and is_deadlocked(self.board):
                self.game_state.deadlock_prompted = True
                self.prompt_deadlock_draw()
                game_screen.update_ui()
                return
                
            self._finalize_turn()
            
    def _finalize_turn(self):
        self.game_state.switch_turn()
        game_screen = self.sm.get_screen('game')
        game_screen.update_ui()
        if self.game_state.mode == GameState.MODE_CPU and self.game_state.current_player == Board.PLAYER_2:
            self.trigger_cpu_move()

    def prompt_deadlock_draw(self):
        from ui.components import ConfirmDialog
        dialog = ConfirmDialog(
            "Neither of us can win.\nDo you want a draw?",
            on_confirm=self.accept_deadlock_draw,
            on_cancel=self.reject_deadlock_draw,
            confirm_text="YES",
            cancel_text="NO"
        )
        dialog.open()

    def accept_deadlock_draw(self):
        self.game_state.is_draw = True
        self.show_result('draw')
        self.sm.get_screen('game').update_ui()

    def reject_deadlock_draw(self):
        self._finalize_turn()

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
            if self.game_state.is_game_over():
                self.go_home()
            elif self.move_history.count() > 0:
                dialog = ConfirmDialog("Game will be lost.", lambda: self.go_home())
                dialog.open()
            else:
                self.go_home()
        elif self.sm.current == 'settings':
            prev = getattr(self, 'previous_screen', 'home')
            self.sm.transition.direction = 'right'
            self.sm.current = prev
        elif self.sm.current == 'setup':
            self.go_home()

    def prompt_restart(self):
        if self.game_state.is_game_over():
            self.start_new_game(reroll_random=True)
        elif self.move_history.count() > 0:
            dialog = ConfirmDialog("Restart game?", lambda: self.start_new_game(reroll_random=True))
            dialog.open()
        else:
            self.start_new_game(reroll_random=True)

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
