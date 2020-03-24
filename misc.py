from manimlib.imports import *


# A single frame of all of the default colors, for reference.
class Colors(Scene):
    def construct(self):
        g = VGroup(*[TextMobject(n.replace('_', ' ')).set_color(v).scale(0.8)
                     for n, v in COLOR_MAP.items()])
        g.arrange_in_grid(9, 7)
        self.add(g)
        self.wait()


