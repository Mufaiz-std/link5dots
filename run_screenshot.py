
import os
os.environ['KIVY_WINDOW'] = 'sdl2'
from main import Link5DotsApp
from kivy.clock import Clock
from kivy.core.window import Window

class TestApp(Link5DotsApp):
    def build(self):
        root = super().build()
        Clock.schedule_once(lambda dt: Window.screenshot('test_main_screenshot.png'), 2)
        Clock.schedule_once(lambda dt: self.stop(), 3)
        return root

TestApp().run()

