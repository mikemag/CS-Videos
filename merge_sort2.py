from manimlib.imports import *

from csanim.code import CodeBlock
from csanim.stacks import StackFrame, CallStack
from end_scene import EndScene


class S01MergeSort2Intro(Scene):

    def construct(self):
        # mmmfixme: placeholder
        title = TextMobject('Merge Sort: Part 2').scale(1.5).to_edge(UP)
        self.play(ShowCreation(title))
        self.wait(duration=0.5)

        t1 = TextMobject("\\textit{Recursion and such}")
        self.play(ShowCreation(t1))
        self.wait(duration=2)

        self.play(FadeOut(title), FadeOut(t1))
