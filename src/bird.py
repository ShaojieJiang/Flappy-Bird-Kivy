from kivy.core.audio import SoundLoader
from kivy.uix.widget import Widget

from .config import GRAVITY, JUMP_FORCE


class Bird(Widget):
    velocity_y: 0
    flap_sound = SoundLoader.load("assets/audios/flap.wav")

    def update(self):
        self.velocity_y += GRAVITY
        self.velocity_y = max(self.velocity_y, -10)
        self.bird_img.y += self.velocity_y
        if self.velocity_y < -5:
            self.bird_img.source = "atlas://assets/images/bird_anim/wing-up"
        elif self.velocity_y < 0:
            self.bird_img.source = "atlas://assets/images/bird_anim/wing-mid"

    def jump(self):
        self.velocity_y = JUMP_FORCE
        self.bird_img.source = "atlas://assets/images/bird_anim/wing-down"
        self.flap_sound.play()

    def reset(self):
        self.bird_img.y = self.height / 2
        self.velocity_y = 0
