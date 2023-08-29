import random

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from .bird import Bird

from .config import DIFFICULTY, SPEED


class Text(Label):
    """Text is defined in the main.kv file."""

    pass


class EnvironmentImage(BoxLayout):
    """Parent class for setting the background and ground images."""

    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)
        self.img1 = Image(source=source, size_hint=(None, None))
        self.img1.size = self.img1.texture.size
        self.size_hint = (None, None)
        self.size = self.img1.size

        self.img2 = Image(source=source, size_hint=(None, None))
        self.img2.size = self.img1.size
        self.img2.pos = (self.width, 0)

        self.add_widget(self.img1)
        self.add_widget(self.img2)

    def update(self):
        self.x -= SPEED
        if self.x <= -self.width:
            self.pos = self.parent.pos


class BackgroundImage(EnvironmentImage):
    def __init__(self, **kwargs):
        super().__init__(source="assets/images/background.png", **kwargs)


class GroundImage(EnvironmentImage):
    def __init__(self, **kwargs):
        super().__init__(source="assets/images/ground.png", **kwargs)


class Pipes(BoxLayout):
    """Define a pair of top and bottom pipes."""

    difficulty = DIFFICULTY
    passed = False

    def update(self):
        self.x -= SPEED
        if self.right < 0:
            self.parent.remove_widget(self)


class PipesQueue(Widget):
    add_interval = 0  # seconds

    def update(self, dt):
        for child in list(self.children):
            child.update()
        self.add_interval -= dt
        if self.add_interval < 0:
            p = Pipes(
                pos=(self.parent.width, 0)
            )  # x is on the right side of the screen
            ratio = (
                random.randrange(2, 8) / 10.0
            )  # region for the pipes to randomly generate
            p.y = self.parent.y - p.height / 2 + ratio * self.parent.height
            self.add_widget(
                p, index=len(self.children)
            )  # add to the end, so that we can correctly decide the current pipe
            self.add_interval = 3

    def reset(self):
        self.add_interval = 0
        for child in list(self.children):
            self.remove_widget(child)


class Environment(BoxLayout):
    def reset(self):
        self.pipes_queue.reset()

    def update(self, dt):
        self.background.update()
        self.ground.update()
        self.pipes_queue.update(dt)

    def collided(self, bird: Bird):
        bird_img = bird.bird_img
        # check grounds
        if bird_img.collide_widget(self.ground.img1) or bird_img.collide_widget(
            self.ground.img2
        ):
            return True
        # check pipes_queue
        for pipes in self.pipes_queue.children:
            if bird_img.collide_widget(pipes.top_img) or bird_img.collide_widget(
                pipes.bottom_img
            ):
                return True
        return False

    def scored(self, bird: Bird):
        bird_img = bird.bird_img

        for pipes in self.pipes_queue.children:
            if not pipes.passed and bird_img.x > pipes.right:
                pipes.passed = True
                return True
        return False
