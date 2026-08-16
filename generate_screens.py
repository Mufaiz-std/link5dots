import os

content = """from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.clock import Clock

from ui.components import CustomLabel, AccentButton, OutlineButton, PillButton, CustomToggle, ConfirmDialog, PALETTE, FONT_BOLD, FONT_REGULAR, DarkButton
from ui.board_view import BoardView
from settings.settings_store import settings
from game.game_state import GameState
from game.board import Board

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*PALETTE['screen_bg'])
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def header(self, title, on_back):
        box = BoxLayout(size_hint_y=None, height=dp(50))
        back_btn = OutlineButton(text="<", size_hint_x=None, width=dp(50))
        back_btn.bind(on_release=on_back)
        lbl = CustomLabel(text=title, font_name=FONT_BOLD)
        box.add_widget(back_btn)
        box.add_widget(lbl)
        return box

class HomeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(24), spacing=dp(16))
        
        title_box = BoxLayout(orientation='vertical', size_hint_y=0.4, padding=[0, dp(40), 0, 0])
        lbl_title = CustomLabel(text="LINK 5", font_name=FONT_BOLD, font_size=dp(36), size_hint_y=0.6)
        lbl_sub = CustomLabel(text="D  O  T  S", font_name=FONT_REGULAR, font_size=dp(18), size_hint_y=0.4, color=PALETTE['text_mid'])
        title_box.add_widget(lbl_title)
        title_box.add_widget(lbl_sub)
        layout.add_widget(title_box)
        
        graphic = Widget(size_hint_y=0.4)
        def draw_graphic(*a):
            graphic.canvas.clear()
            with graphic.canvas:
                Color(*PALETTE['grid_line'])
                cx, cy = graphic.center_x, graphic.center_y
                step = dp(25)
                for i in range(-2, 3):
                    Line(points=[cx + i*step, cy - 2*step, cx + i*step, cy + 2*step], width=1.5)
                    Line(points=[cx - 2*step, cy + i*step, cx + 2*step, cy + i*step], width=1.5)
                Color(*PALETTE['text_dark'])
                Line(circle=(cx, cy, step*0.35), width=2)
                Line(circle=(cx - step, cy - step, step*0.35), width=2)
                Ellipse(pos=(cx - step - step*0.35, cy + step - step*0.35), size=(step*0.7, step*0.7))
                Ellipse(pos=(cx + step - step*0.35, cy - step - step*0.35), size=(step*0.7, step*0.7))
        graphic.bind(pos=draw_graphic, size=draw_graphic)
        layout.add_widget(graphic)
        
        btn_box = BoxLayout(orientation='vertical', size_hint_y=0.2, spacing=dp(16))
        btn_play = AccentButton(text="PLAY")
        btn_play.bind(on_release=lambda x: self.parent.transition_to('setup'))
        btn_settings = OutlineButton(text="SETTINGS")
        btn_settings.bind(on_release=lambda x: self.parent.transition_to('settings'))
        btn_box.add_widget(btn_play)
        btn_box.add_widget(btn_settings)
        layout.add_widget(btn_box)
        self.add_widget(layout)

class SetupScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(24), spacing=dp(16))
        self.layout.add_widget(self.header("NEW GAME", lambda x: self.parent.transition_to('home')))
        
        self.layout.add_widget(CustomLabel(text="GAME MODE", size_hint_y=None, height=dp(20), halign='left', text_size=(None, None)))
        mode_box = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(10))
        self.btn_cpu = PillButton(text="VS CPU", selected=True)
        self.btn_pvp = PillButton(text="VS PLAYER")
        self.btn_cpu.bind(on_release=lambda x: self.set_mode(GameState.MODE_CPU))
        self.btn_pvp.bind(on_release=lambda x: self.set_mode(GameState.MODE_PVP))
        mode_box.add_widget(self.btn_cpu)
        mode_box.add_widget(self.btn_pvp)
        self.layout.add_widget(mode_box)
        
        self.layout.add_widget(CustomLabel(text="BOARD SIZE", size_hint_y=None, height=dp(20), halign='left'))
        size_box = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(10))
        self.btn_10 = PillButton(text="10x10")
        self.btn_15 = PillButton(text="15x15", selected=True)
        self.btn_20 = PillButton(text="20x20")
        self.btn_custom = PillButton(text="CUSTOM")
        for b, s in [(self.btn_10, 10), (self.btn_15, 15), (self.btn_20, 20), (self.btn_custom, 'custom')]:
            b.bind(on_release=lambda instance, size=s: self.set_size(size))
            size_box.add_widget(b)
        self.layout.add_widget(size_box)
        
        self.custom_size_box = BoxLayout(orientation='vertical', size_hint_y=None, height=0, opacity=0)
        self.layout.add_widget(self.custom_size_box)
        
        self.diff_lbl = CustomLabel(text="DIFFICULTY", size_hint_y=None, height=dp(20), halign='left')
        self.layout.add_widget(self.diff_lbl)
        self.diff_box = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(10))
        self.btn_easy = PillButton(text="EASY", selected=True)
        self.btn_hard = PillButton(text="HARD")
        self.btn_easy.bind(on_release=lambda x: self.set_diff(GameState.DIFF_EASY))
        self.btn_hard.bind(on_release=lambda x: self.set_diff(GameState.DIFF_HARD))
        self.diff_box.add_widget(self.btn_easy)
        self.diff_box.add_widget(self.btn_hard)
        self.layout.add_widget(self.diff_box)
        
        self.layout.add_widget(CustomLabel(text="WHO GOES FIRST", size_hint_y=None, height=dp(20), halign='left'))
        self.first_box = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(10))
        self.btn_f1 = PillButton(text="YOU FIRST", selected=True)
        self.btn_f2 = PillButton(text="CPU FIRST")
        self.btn_fr = PillButton(text="RANDOM")
        self.btn_f1.bind(on_release=lambda x: self.set_first(GameState.FIRST_P1))
        self.btn_f2.bind(on_release=lambda x: self.set_first(GameState.FIRST_P2))
        self.btn_fr.bind(on_release=lambda x: self.set_first(GameState.FIRST_RANDOM))
        self.first_box.add_widget(self.btn_f1)
        self.first_box.add_widget(self.btn_f2)
        self.first_box.add_widget(self.btn_fr)
        self.layout.add_widget(self.first_box)
        
        self.layout.add_widget(Widget()) 
        btn_start = DarkButton(text="START GAME")
        btn_start.bind(on_release=self.start_game)
        self.layout.add_widget(btn_start)
        self.add_widget(self.layout)
        
        self.mode = GameState.MODE_CPU
        self.board_size = 15
        self.difficulty = GameState.DIFF_EASY
        self.first = GameState.FIRST_P1

        self.custom_r = Slider(min=5, max=20, value=15, step=1)
        self.custom_c = Slider(min=5, max=20, value=15, step=1)
        lbl_r = CustomLabel(text="ROWS: 15")
        lbl_c = CustomLabel(text="COLS: 15")
        self.custom_r.bind(value=lambda i, v: setattr(lbl_r, 'text', f"ROWS: {int(v)}"))
        self.custom_c.bind(value=lambda i, v: setattr(lbl_c, 'text', f"COLS: {int(v)}"))
        box_r = BoxLayout()
        box_r.add_widget(lbl_r)
        box_r.add_widget(self.custom_r)
        box_c = BoxLayout()
        box_c.add_widget(lbl_c)
        box_c.add_widget(self.custom_c)
        self.custom_size_box.add_widget(box_r)
        self.custom_size_box.add_widget(box_c)
        
    def set_mode(self, mode):
        self.mode = mode
        self.btn_cpu.selected = mode == GameState.MODE_CPU
        self.btn_pvp.selected = mode == GameState.MODE_PVP
        if mode == GameState.MODE_PVP:
            self.diff_lbl.opacity = 0
            self.diff_lbl.height = 0
            self.diff_box.opacity = 0
            self.diff_box.height = 0
            self.btn_f1.text = "PLAYER 1"
            self.btn_f2.text = "PLAYER 2"
        else:
            self.diff_lbl.opacity = 1
            self.diff_lbl.height = dp(20)
            self.diff_box.opacity = 1
            self.diff_box.height = dp(48)
            self.btn_f1.text = "YOU FIRST"
            self.btn_f2.text = "CPU FIRST"
            
    def set_size(self, size):
        self.board_size = size
        self.btn_10.selected = size == 10
        self.btn_15.selected = size == 15
        self.btn_20.selected = size == 20
        self.btn_custom.selected = size == 'custom'
        if size == 'custom':
            self.custom_size_box.opacity = 1
            self.custom_size_box.height = dp(80)
        else:
            self.custom_size_box.opacity = 0
            self.custom_size_box.height = 0
            
    def set_diff(self, diff):
        self.difficulty = diff
        self.btn_easy.selected = diff == GameState.DIFF_EASY
        self.btn_hard.selected = diff == GameState.DIFF_HARD
        
    def set_first(self, first):
        self.first = first
        self.btn_f1.selected = first == GameState.FIRST_P1
        self.btn_f2.selected = first == GameState.FIRST_P2
        self.btn_fr.selected = first == GameState.FIRST_RANDOM
        
    def start_game(self, *args):
        app = self.parent.app
        app.game_state.mode = self.mode
        app.game_state.difficulty = self.difficulty
        app.game_state.who_goes_first_setting = self.first
        if self.board_size == 'custom':
            app.game_state.board_rows = int(self.custom_r.value)
            app.game_state.board_cols = int(self.custom_c.value)
        else:
            app.game_state.board_rows = self.board_size
            app.game_state.board_cols = self.board_size
        app.start_new_game()

class GameScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        
        # Header
        self.header_box = BoxLayout(size_hint_y=None, height=dp(50), padding=[dp(10), 0])
        self.btn_back = OutlineButton(text="<", size_hint_x=None, width=dp(50))
        self.btn_back.bind(on_release=self.go_back)
        self.lbl_turn = CustomLabel(text="", font_name=FONT_BOLD)
        self.btn_set = OutlineButton(text="*", size_hint_x=None, width=dp(50))
        self.btn_set.bind(on_release=lambda x: self.parent.transition_to('settings'))
        
        self.header_box.add_widget(self.btn_back)
        self.header_box.add_widget(self.lbl_turn)
        self.header_box.add_widget(self.btn_set)
        self.layout.add_widget(self.header_box)
        
        # Board
        self.board_container = FloatLayout()
        self.layout.add_widget(self.board_container)
        
        # Footer
        self.footer_box = BoxLayout(size_hint_y=None, height=dp(60), padding=dp(10))
        self.lbl_p1 = CustomLabel(text="o WHITE 0", size_hint_x=0.4, halign='left')
        self.btn_undo = OutlineButton(text="UNDO", size_hint_x=0.2)
        self.btn_undo.bind(on_release=self.do_undo)
        self.lbl_p2 = CustomLabel(text="• BLACK 0", size_hint_x=0.4, halign='right')
        
        self.footer_box.add_widget(self.lbl_p1)
        self.footer_box.add_widget(self.btn_undo)
        self.footer_box.add_widget(self.lbl_p2)
        self.layout.add_widget(self.footer_box)
        self.add_widget(self.layout)

    def on_enter(self, *args):
        app = self.parent.app
        self.board_container.clear_widgets()
        self.board_view = BoardView(app.game_state, app.board, app.handle_player_move)
        self.board_container.add_widget(self.board_view)
        self.update_ui()
        
    def do_undo(self, *args):
        app = self.parent.app
        if not app.game_state.cpu_thinking:
            app.handle_undo()
            
    def go_back(self, *args):
        app = self.parent.app
        if not app.game_state.cpu_thinking:
            app.handle_back()
            
    def update_ui(self, *args):
        app = self.parent.app
        if not app: return
        gs = app.game_state
        
        if gs.cpu_thinking:
            self.lbl_turn.text = "CPU IS THINKING..."
        else:
            if gs.mode == GameState.MODE_CPU:
                self.lbl_turn.text = "YOUR TURN" if gs.current_player == gs._actual_first_player else "CPU'S TURN"
            else:
                self.lbl_turn.text = "PLAYER 1'S TURN" if gs.current_player == gs._actual_first_player else "PLAYER 2'S TURN"
                
        p1_pieces = app.board.piece_count[Board.PLAYER_1]
        p2_pieces = app.board.piece_count[Board.PLAYER_2]
        self.lbl_p1.text = f"o WHITE {p1_pieces}"
        self.lbl_p2.text = f"• BLACK {p2_pieces}"
        
        if hasattr(self, 'board_view'):
            last = app.move_history.get_last_move()
            if last:
                self.board_view.set_last_move(last[0], last[1])
            else:
                self.board_view.set_last_move(None, None)
            self.board_view.draw_board()

class SettingsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(24), spacing=dp(16))
        self.layout.add_widget(self.header("SETTINGS", lambda x: self.parent.transition_to('home', pop=True)))
        
        def add_setting(label, key):
            box = BoxLayout(size_hint_y=None, height=dp(50))
            lbl = CustomLabel(text=label, halign='left', text_size=(None, None))
            tog = CustomToggle(active=settings.get(key))
            tog.bind(active=lambda instance, val: settings.set(key, val))
            box.add_widget(lbl)
            box.add_widget(tog)
            
            line = Widget(size_hint_y=None, height=dp(1))
            with line.canvas:
                Color(*PALETTE['grid_line'])
                Rectangle(pos=line.pos, size=line.size)
            def update_rect(instance, value):
                instance.canvas.clear()
                with instance.canvas:
                    Color(*PALETTE['grid_line'])
                    Rectangle(pos=instance.pos, size=instance.size)
            line.bind(pos=update_rect, size=update_rect)
            
            self.layout.add_widget(box)
            self.layout.add_widget(line)

        add_setting("SOUND", 'sound')
        add_setting("HAPTICS", 'haptics')
        add_setting("SHOW LAST MOVE", 'show_last_move')
        
        self.layout.add_widget(Widget())
        self.layout.add_widget(CustomLabel(text="LINK 5 DOTS • V1.0", size_hint_y=None, height=dp(20), color=PALETTE['text_mid']))
        self.add_widget(self.layout)

class ResultScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(24), spacing=dp(16))
        
        self.graphic_box = AnchorLayout(size_hint_y=0.4)
        self.layout.add_widget(self.graphic_box)
        
        self.lbl_title = CustomLabel(font_name=FONT_BOLD, font_size=dp(32), size_hint_y=None, height=dp(40))
        self.lbl_sub = CustomLabel(color=PALETTE['text_mid'], size_hint_y=None, height=dp(20))
        self.layout.add_widget(self.lbl_title)
        self.layout.add_widget(self.lbl_sub)
        self.layout.add_widget(Widget(size_hint_y=0.1))
        
        self.btn_primary = DarkButton(text="PLAY AGAIN")
        self.btn_primary.bind(on_release=lambda x: self.parent.app.start_new_game(reroll_random=True))
        self.btn_menu = OutlineButton(text="MAIN MENU")
        self.btn_menu.bind(on_release=lambda x: self.parent.transition_to('home'))
        
        self.layout.add_widget(self.btn_primary)
        self.layout.add_widget(self.btn_menu)
        self.add_widget(self.layout)
        
    def setup_result(self, outcome, gs):
        self.graphic_box.clear_widgets()
        graphic = Widget()
        self.graphic_box.add_widget(graphic)
        
        is_win = outcome == 'win'
        is_lose = outcome == 'lose'
        
        if is_win:
            self.lbl_title.text = "YOU WIN" if gs.mode == GameState.MODE_CPU else ("PLAYER 1 WINS" if gs.winner == gs._actual_first_player else "PLAYER 2 WINS")
            self.lbl_sub.text = "FIVE IN A ROW"
            self.btn_primary.text = "PLAY AGAIN"
            self.lbl_title.color = PALETTE['text_dark']
            
            def draw_win(*a):
                graphic.canvas.clear()
                with graphic.canvas:
                    Color(*PALETTE['text_dark'])
                    cx, cy = graphic.center_x, graphic.center_y
                    for i in range(-2, 3):
                        Ellipse(pos=(cx + i*15 - 5, cy - i*15 - 5), size=(10, 10))
                    Color(*PALETTE['accent_fill'])
                    Line(points=[cx - 30, cy + 30, cx + 30, cy - 30], width=3)
            graphic.bind(pos=draw_win, size=draw_win)
            
        elif is_lose:
            self.lbl_title.text = "YOU LOSE"
            self.lbl_sub.text = "CPU CONNECTED FIVE"
            self.btn_primary.text = "TRY AGAIN"
            self.lbl_title.color = PALETTE['text_mid']
            
            def draw_lose(*a):
                graphic.canvas.clear()
                with graphic.canvas:
                    Color(*PALETTE['muted_stroke'])
                    cx, cy = graphic.center_x, graphic.center_y
                    for i in range(-2, 3):
                        Line(circle=(cx + i*15, cy - i*15, 5), width=1.5)
                    Color(*PALETTE['muted_line'])
                    Line(points=[cx - 30, cy + 30, cx + 30, cy - 30], width=3)
            graphic.bind(pos=draw_lose, size=draw_lose)
            
        else: # Draw
            self.lbl_title.text = "DRAW"
            self.lbl_sub.text = "BOARD IS FULL"
            self.btn_primary.text = "PLAY AGAIN"
            self.lbl_title.color = PALETTE['text_dark']
            
            def draw_draw(*a):
                graphic.canvas.clear()
                with graphic.canvas:
                    cx, cy = graphic.center_x, graphic.center_y
                    Color(*PALETTE['text_dark'])
                    Ellipse(pos=(cx-15, cy+5), size=(10,10))
                    Line(circle=(cx+5, cy+10, 5), width=1.5)
                    Ellipse(pos=(cx+15, cy+5), size=(10,10))
                    Line(circle=(cx-15, cy-15, 5), width=1.5)
                    Ellipse(pos=(cx-5, cy-15), size=(10,10))
                    Line(circle=(cx+15, cy-15, 5), width=1.5)
            graphic.bind(pos=draw_draw, size=draw_draw)
"""
with open("ui/screens.py", "w", encoding="utf-8") as f:
    f.write(content)
