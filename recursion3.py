from manimlib.imports import *

from cs_education.csanim.code import CodeBlock
from cs_education.csanim.stacks import StackFrame, CallStack


class Recursion3Intro(Scene):

    def construct(self):
        title = TextMobject('Recursion: Part 3').scale(1.5).to_edge(UP)
        self.play(ShowCreation(title))
        self.wait(duration=0.5)


class Fibonacci(Scene):

    def construct(self):
        # Now do Fibonacci.
        # Two calls instead of one.
        # Refresher on what the equation is and why it's useful.
        # Trace a short call, and track the history of the calls to the side.
        #   - Then run thru a longer one, tracking the history and showing a bushy tree.
        #   - Simplify the call stack as it runs and focus on the growing call history tree.
        #   - Afterwords, explain how most recursive algorithms are shown like this in books and elsewhere, and
        #     encourage them to study the picture and see how it relates to the code.
        #   - Leave this as the final image of the video.
        pass
