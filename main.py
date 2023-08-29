from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget

from src.screens import Game


class MainApp(App):
    def build(self):
        widget = Widget()
        widget.add_widget(Game())
        Window.size = [0.5 * dim for dim in widget.children[0].size]
        return widget


if __name__ == "__main__":
    MainApp().run()
