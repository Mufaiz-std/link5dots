from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle
from kivy.graphics.instructions import InstructionGroup
from kivy.utils import get_color_from_hex
from kivy.properties import BooleanProperty, StringProperty, ListProperty
from kivy.animation import Animation
from kivy.metrics import dp

class ThemePalette(dict):
    def apply_theme(self, theme_name):
        if theme_name == 'dark':
            self.update({
                'screen_bg': get_color_from_hex('#1E241E'),
                'grid_line': get_color_from_hex('#3A453A'),
                'text_primary': get_color_from_hex('#E7EEE2'),
                'text_mid': get_color_from_hex('#7E8F76'),
                'accent_fill': get_color_from_hex('#7FA372'),
                'accent_text': get_color_from_hex('#14180F'),
                'dark_fill': get_color_from_hex('#E7EEE2'),
                'muted_stroke': get_color_from_hex('#5C6B57'),
                'muted_line': get_color_from_hex('#4A5A44'),
            })
        else:
            self.update({
                'screen_bg': get_color_from_hex('#DCE5D6'),
                'grid_line': get_color_from_hex('#A9B8A2'),
                'text_primary': get_color_from_hex('#3A4A3A'),
                'text_mid': get_color_from_hex('#5C6B57'),
                'accent_fill': get_color_from_hex('#6B8064'),
                'accent_text': get_color_from_hex('#F2F5EF'),
                'dark_fill': get_color_from_hex('#3A4A3A'),
                'muted_stroke': get_color_from_hex('#8A968A'),
                'muted_line': get_color_from_hex('#8FA37E'),
            })

PALETTE = ThemePalette()

FONT_REGULAR = 'assets/fonts/RobotoMono-Regular.ttf'
FONT_BOLD = 'assets/fonts/RobotoMono-Bold.ttf'

class CustomLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault('font_name', FONT_REGULAR)
        kwargs.setdefault('color', PALETTE['text_primary'])
        super().__init__(**kwargs)

class AccentButton(Button):
    def __init__(self, **kwargs):
        kwargs.setdefault('background_normal', '')
        kwargs.setdefault('background_down', '')
        kwargs.setdefault('background_color', (0,0,0,0))
        kwargs.setdefault('font_name', FONT_BOLD)
        kwargs.setdefault('color', PALETTE['accent_text'])
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(48))
        self.bg_color = kwargs.pop('bg_color', PALETTE['accent_fill'])
        super().__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas, state=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            color = self.bg_color
            if self.state == 'down':
                # slightly darker on press
                color = [c * 0.9 for c in color[:3]] + [1]
            Color(*color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(4)])

class DarkButton(AccentButton):
    def __init__(self, **kwargs):
        kwargs['bg_color'] = PALETTE['dark_fill']
        super().__init__(**kwargs)

class OutlineButton(Button):
    def __init__(self, **kwargs):
        kwargs.setdefault('background_normal', '')
        kwargs.setdefault('background_down', '')
        kwargs.setdefault('background_color', (0,0,0,0))
        kwargs.setdefault('font_name', FONT_BOLD)
        kwargs.setdefault('color', PALETTE['text_mid'])
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(48))
        super().__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas, state=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.state == 'down':
                Color(*PALETTE['grid_line'])
                RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(4)])
            Color(*PALETTE['grid_line'])
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(4)), width=1.5)

class PillButton(Button):
    selected = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        kwargs.setdefault('background_normal', '')
        kwargs.setdefault('background_down', '')
        kwargs.setdefault('background_color', (0,0,0,0))
        kwargs.setdefault('font_name', FONT_REGULAR)
        super().__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas, selected=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.before.clear()
        if self.selected:
            self.color = PALETTE['accent_text']
            with self.canvas.before:
                Color(*PALETTE['accent_fill'])
                RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(4)])
        else:
            self.color = PALETTE['text_mid']
            with self.canvas.before:
                Color(*PALETTE['grid_line'])
                Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(4)), width=1.2)

class CustomToggle(Widget):
    active = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(50), dp(30))
        self.ig = InstructionGroup()
        self.canvas.add(self.ig)
        self.bind(pos=self.update_canvas, size=self.update_canvas, active=self.update_canvas)
        self.update_canvas()
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.active = not self.active
            return True
        return super().on_touch_down(touch)

    def update_canvas(self, *args):
        self.ig.clear()
        # track
        self.ig.add(Color(*PALETTE['accent_fill'] if self.active else PALETTE['grid_line']))
        self.ig.add(RoundedRectangle(pos=self.pos, size=self.size, radius=[self.height/2]))
        
        # knob
        self.ig.add(Color(*PALETTE['accent_text']))
        knob_size = self.height - dp(4)
        knob_x = self.x + self.width - knob_size - dp(2) if self.active else self.x + dp(2)
        knob_y = self.y + dp(2)
        self.ig.add(RoundedRectangle(pos=(knob_x, knob_y), size=(knob_size, knob_size), radius=[knob_size/2]))

class ConfirmDialog(ModalView):
    def __init__(self, title_text, on_confirm, on_cancel=None, confirm_text="RESTART", cancel_text="CANCEL", **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.8, None)
        self.height = dp(180)  # Slightly taller to fit multi-line text
        self.background_color = (0,0,0,0.5)
        self.auto_dismiss = False
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        with layout.canvas.before:
            Color(*PALETTE['screen_bg'])
            self.rect = RoundedRectangle(radius=[dp(6)])
            
        def update_rect(instance, value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size
        layout.bind(pos=update_rect, size=update_rect)
        
        lbl = CustomLabel(text=title_text, font_name=FONT_BOLD, size_hint_y=0.5)
        layout.add_widget(lbl)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=0.5)
        
        btn_cancel = OutlineButton(text=cancel_text)
        def do_cancel(instance):
            self.dismiss()
            if on_cancel:
                on_cancel()
        btn_cancel.bind(on_release=do_cancel)
        
        btn_restart = DarkButton(text=confirm_text)
        def do_confirm(instance):
            self.dismiss()
            on_confirm()
        btn_restart.bind(on_release=do_confirm)
        
        btn_layout.add_widget(btn_cancel)
        btn_layout.add_widget(btn_restart)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
