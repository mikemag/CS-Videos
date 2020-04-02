from manimlib.imports import *


class Recursion1Intro(Scene):
    def construct(self):
        title = TextMobject('Recursion').scale(1.5).to_edge(TOP)
        subtitle = TextMobject('\\textit{An introduction}').next_to(title, DOWN)
        self.play(ShowCreation(title))
        self.play(FadeInFromDown(subtitle))
        self.wait()
