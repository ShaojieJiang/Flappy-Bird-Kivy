from threading import Thread

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.widget import Widget

from .bird import Bird
from .config import DATA_COLLECTION_RATE, FPS, SPEED
from .environment import Environment, Text


class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # define states
        self.game_over = True
        self.score = 0

        # define and add widgets
        self.env = Environment()
        self.size = self.env.size
        self.bird = Bird(size=self.size)
        self.start_text = Text(
            text="Tap to start",
            center_x=self.center_x,
            center_y=self.center_y + 0.1 * self.height,
        )
        self.score_text = Text(
            text="0",
            center_x=self.center_x,
            center_y=0.9 * self.height,
            disabled=True,
        )

        self.add_widget(self.env)
        self.add_widget(self.bird)
        self.add_widget(self.start_text)
        self.add_widget(self.score_text)

        # add sound
        self.score_sound = SoundLoader.load("assets/audios/score.wav")
        self.hit_sound = SoundLoader.load("assets/audios/hit.wav")

        # add keyboard input
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, "text")
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        # schedules
        Clock.schedule_interval(self.update, 1.0 / FPS)

    def update(self, dt):
        if self.game_over:
            return

        self.env.update(dt)
        self.bird.update()

        # Detect if collision has happend
        if self.env.collided(self.bird):
            self.game_over = True
            self.hit_sound.play()
            self.start_text.disabled = False

        # Detect if scoring has happend
        if self.env.scored(self.bird):
            self.score += 1
            self.score_text.text = str(self.score)
            self.score_sound.play()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        if keycode[1] == "spacebar":
            self._act()
            return True
        return False

    def on_touch_down(self, *ignore):
        self._act()

    def _act(self):
        if self.game_over:
            self._start_game()
        else:
            self.bird.jump()

    def _start_game(self):
        self.start_text.disabled = True
        self.score_text.disabled = False
        self.game_over = False
        self.bird.reset()
        self.env.reset()
