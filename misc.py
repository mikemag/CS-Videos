from manimlib.imports import *

from cs_education.csanim.code import CodeTextString, CodeBlock
from cs_education.csanim.stacks import StackFrame


# A single frame of all of the default colors, for reference.
class Colors(Scene):
    def construct(self):
        g = VGroup(*[
            TextMobject(n.replace('_', ' ')).set_color(v).scale(0.8)
            for n, v in COLOR_MAP.items()
        ])
        g.arrange_in_grid(9, 7)
        self.add(g)
        self.wait()


class CodeTextStringDemo(Scene):
    def construct(self):
        snippets = [
            ('Java', r"""
            public static int foo1(int a) {
                int b = a * 3;
                return a + b;
            }
            """),
            ('Java', r"""
            public static int foo2(int a) {
                int b = bar2(a, 5);
                return b;
            }
            """),
            ('C++', r"""
            BoardShape::~BoardShape() {
              for (auto dps : m_debugPathSets) {
                delete dps;
              }
            }
            """),
            ('Python', r"""
            for s in snippets:
                c = CodeTextString(s[1], s[0])
                self.play(
                    FadeOutAndShift(last_c, UP),
                    FadeInFromDown(c),
                )
                last_c = c
            """),
        ]

        last_c = Mobject()
        for s in snippets:
            c = CodeTextString(s[0], s[1])
            t = TextMobject(s[0]).next_to(c, UP, buff=LARGE_BUFF).scale(1.2)
            g = VGroup(c, t)
            self.play(
                FadeOutAndShift(last_c, UP),
                FadeInFromDown(g),
            )

            last_h = None
            for line_no in range(1, len(c) + 1):
                h = c.get_line_highlight_rect(line_no)
                if last_h:
                    self.play(FadeOut(last_h), FadeIn(h))
                else:
                    self.play(FadeIn(h))
                last_h = h
            self.play(FadeOut(last_h))

            r = c.get_line_highlight_rect((1, 3))
            self.play(FadeIn(r))
            self.play(FadeOut(r))

            l2 = SurroundingRectangle(c.get_line(2))
            self.play(Indicate(c.get_line(3)))
            self.play(Indicate(c.get_line(3)[1:3]))
            self.play(FadeIn(l2))
            g.add(l2)
            l3 = SurroundingRectangle(c.get_line(3))
            self.play(ReplacementTransform(l2, l3))
            g.add(l3)

            self.play(ScaleInPlace(g, 0.5))
            last_c = g

        self.wait()


class CodeBlockDemo(Scene):
    def construct(self):
        c1 = CodeBlock(
            'Java', r"""
            int foo() {
                int n = bar(1, 2);
                return n;
            }
            """)
        c2 = CodeBlock(
            'Java', r"""
            int bar(int x, int y) {
                int a = x + y;
                int b = a * 2;
                return b;
            }
            """)
        c1.to_edge(UP)
        c2.next_to(c1, DOWN, buff=LARGE_BUFF)
        self.play(FadeIn(c1), FadeIn(c2))
        # self.wait()

        self.play(c1.highlight_lines, 1)
        self.play(c1.highlight_lines, 2)
        self.play(c1.highlight_lines, (2, 3))
        self.play(c1.highlight_lines, 3)
        self.play(c1.fade_out_highlight)
        c1.move_highlight_rect(2)
        self.play(c1.highlight_lines, 2)
        self.wait()

        hr_caller, hr_callee = c1.setup_for_call(c2, 1)
        self.play(
            c1.highlight_caller,
            ReplacementTransform(hr_caller, hr_callee, path_arc=np.pi),
        )
        c2.complete_callee(hr_callee, self)
        self.wait()

        self.play(c2.highlight_lines, 2)
        self.play(c2.highlight_lines, 3)
        self.play(c2.highlight_lines, 4)
        self.wait()

        hr_returner, hr_returnee = c2.setup_for_return(c1)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=-np.pi),
            c1.highlight_returnee,
        )
        c1.complete_returnee(hr_returnee, self)

        self.play(c1.highlight_lines, 3)

        # Again...
        hr_caller, hr_callee = c1.setup_for_call(c2, 1)
        self.play(
            c1.highlight_caller,
            ReplacementTransform(hr_caller, hr_callee, path_arc=np.pi),
        )
        c2.complete_callee(hr_callee, self)
        self.wait()

        self.play(c2.highlight_lines, 2)
        self.play(c2.highlight_lines, 3)
        self.play(c2.highlight_lines, 4)
        self.wait()

        hr_returner, hr_returnee = c2.setup_for_return(c1)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=-np.pi),
            c1.highlight_returnee,
        )
        c1.complete_returnee(hr_returnee, self)

        self.play(c1.highlight_lines, 4)

        self.wait()

        self.play(FadeOut(c1), FadeOut(c2))
        self.wait()


class StackFrameDemo(Scene):
    def construct(self):
        frame_width = 3
        f1 = StackFrame('foo()', 1, ['a', 'b', ('c', 2)], width=frame_width)
        self.play(FadeIn(f1))
        self.play(f1.set_line, 2)
        self.play(f1.set_line, 3)
        self.play(f1.update_slot, 'b', 42)
        self.play(f1.set_line, 4, f1.update_slot, 'a', 43)

        f2 = StackFrame('bar(1, 2, 3)', 1, ['x'], width=frame_width)
        f2.next_to(f1, DOWN, buff=SMALL_BUFF)
        self.play(FadeIn(f2))
        self.wait()

        self.play(FadeOut(f1), FadeOut(f2))
        self.wait()
