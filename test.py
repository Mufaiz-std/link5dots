from kivy.app import App
from ui.screens import HomeScreen
from kivy.core.window import Window

class TestApp(App):
    def build(self):
        Window.clearcolor = (1, 0, 0, 1) # Red bg to contrast
        print('Building app')
        h = HomeScreen(name='home')
        print('HomeScreen children:', h.children)
        if h.children:
            print('Layout children:', h.children[0].children)
        return h

TestApp().run()
