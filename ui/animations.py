from kivy.animation import Animation
from kivy.metrics import dp

def animate_piece_placement(widget):
    # scale up slightly then back down
    widget.scale = 0.5
    anim = Animation(scale=1.1, duration=0.1) + Animation(scale=1.0, duration=0.05)
    anim.start(widget)

# Draw win line animation is handled directly in board_view.py since it needs canvas context
