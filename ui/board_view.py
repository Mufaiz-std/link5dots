from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse
from kivy.metrics import dp
from kivy.core.audio import SoundLoader
import math

from game.board import Board
from settings.settings_store import settings
from ui.components import PALETTE

class BoardView(Scatter):
    def __init__(self, game_state, board, on_move_callback, **kwargs):
        kwargs.setdefault('do_rotation', False)
        kwargs.setdefault('scale_min', 0.5)
        kwargs.setdefault('scale_max', 3.0)
        super().__init__(**kwargs)
        self.game_state = game_state
        self.board = board
        self.on_move_callback = on_move_callback
        
        self.sound_tak = SoundLoader.load('assets/sounds/tak.wav')
        
        from kivy.graphics.instructions import InstructionGroup
        self.board_ig = InstructionGroup()
        self.canvas.add(self.board_ig)
        
        # We will draw directly on this scatter's canvas
        self.bind(size=self.draw_board, pos=self.draw_board)
        
        # Track last touch down to distinguish tap vs pan
        self.last_touch_down = None
        self.tap_threshold = dp(10)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.last_touch_down = touch.pos
        return super().on_touch_down(touch)
        
    def on_touch_up(self, touch):
        if self.last_touch_down:
            dx = touch.pos[0] - self.last_touch_down[0]
            dy = touch.pos[1] - self.last_touch_down[1]
            if math.hypot(dx, dy) < self.tap_threshold:
                # It's a tap
                self.handle_tap(touch)
            self.last_touch_down = None
        return super().on_touch_up(touch)
        
    def handle_tap(self, touch):
        if self.game_state.is_game_over() or self.game_state.cpu_thinking:
            return
            
        # Convert window touch to local coordinates
        local_x, local_y = self.to_local(*touch.pos)
        
        # Calculate which cell was tapped
        cell_size = min(self.width / max(1, self.board.cols), self.height / max(1, self.board.rows))
        # Calculate grid metrics to determine offsets
        grid_w = cell_size * self.board.cols
        grid_h = cell_size * self.board.rows
        offset_x = (self.width - grid_w) / 2
        offset_y = (self.height - grid_h) / 2
        
        # Check if tap was outside the board
        if local_x < offset_x or local_x > offset_x + grid_w or local_y < offset_y or local_y > offset_y + grid_h:
            return
            
        col = int((local_x - offset_x) / cell_size)
        row = int((local_y - offset_y) / cell_size)
        
        if 0 <= row < self.board.rows and 0 <= col < self.board.cols:
            self.on_move_callback(row, col)

    def play_sound(self):
        if settings.get('sound') and self.sound_tak:
            self.sound_tak.play()
            
    def play_haptic(self):
        if settings.get('haptics'):
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Context = autoclass('android.content.Context')
                Vibrator = autoclass('android.os.Vibrator')
                vibrator = PythonActivity.mActivity.getSystemService(Context.VIBRATOR_SERVICE)
                if vibrator and vibrator.hasVibrator():
                    vibrator.vibrate(20) # 20ms
            except Exception:
                pass

    def draw_board(self, *args):
        self.board_ig.clear()
        
        cell_size = min(self.width / max(1, self.board.cols), self.height / max(1, self.board.rows))
        
        # Center the grid inside the scatter
        grid_w = cell_size * self.board.cols
        grid_h = cell_size * self.board.rows
        offset_x = (self.width - grid_w) / 2
        offset_y = (self.height - grid_h) / 2
        
        # Draw Grid Lines
        self.board_ig.add(Color(*PALETTE['grid_line']))
        # Vertical lines
        for c in range(self.board.cols):
            x = offset_x + c * cell_size + cell_size / 2
            self.board_ig.add(Line(points=[x, offset_y, x, offset_y + grid_h], width=1.5))
        # Horizontal lines
        for r in range(self.board.rows):
            y = offset_y + r * cell_size + cell_size / 2
            self.board_ig.add(Line(points=[offset_x, y, offset_x + grid_w, y], width=1.5))
            
        # Draw Pieces
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                val = self.board.grid[r][c]
                if val != Board.EMPTY:
                    px = offset_x + c * cell_size + cell_size / 2
                    py = offset_y + r * cell_size + cell_size / 2
                    psize = cell_size * 0.85
                    
                    is_hollow = (val == Board.PLAYER_1)
                    
                    self.board_ig.add(Color(*PALETTE['text_primary']))
                    if is_hollow:
                        self.board_ig.add(Line(circle=(px, py, psize/2), width=2))
                    else:
                        self.board_ig.add(Ellipse(pos=(px - psize/2, py - psize/2), size=(psize, psize)))
                        
            # Highlight Last Move
            if settings.get('show_last_move') and getattr(self, 'last_move', None) and self.last_move[0] is not None:
                r, c = self.last_move
                self.board_ig.add(Color(*PALETTE['accent_fill']))
                cx = offset_x + c * cell_size + cell_size / 2
                cy = offset_y + r * cell_size + cell_size / 2
                hl_size = cell_size * 0.8
                self.board_ig.add(Line(rectangle=(cx - hl_size/2, cy - hl_size/2, hl_size, hl_size), dash_length=5, dash_offset=5, width=1.5))

            if self.game_state.win_line:
                self.board_ig.add(Color(*PALETTE['accent_fill']))
                r1, c1 = self.game_state.win_line[0]
                r2, c2 = self.game_state.win_line[-1]
                
                cx1 = offset_x + c1 * cell_size + cell_size / 2
                cy1 = offset_y + r1 * cell_size + cell_size / 2
                cx2 = offset_x + c2 * cell_size + cell_size / 2
                cy2 = offset_y + r2 * cell_size + cell_size / 2
                
                self.board_ig.add(Line(points=[cx1, cy1, cx2, cy2], width=4))

    def set_last_move(self, r, c):
        self.last_move = (r, c)
        self.draw_board()

