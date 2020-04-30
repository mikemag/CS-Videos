from manimlib.imports import *

from csanim.code import CodeTextString, CodeBlock
from csanim.stacks import StackFrame
from csanim.trees import Tree


class FibTree(Tree):

    def __init__(self, n, parent, text_scale=1.0):
        super().__init__(parent)
        self.fib_n = n
        self.result = 0

        if parent is not None:
            self.text_scale = parent.text_scale
        else:
            self.text_scale = text_scale
        self.label = TextMobject("$F_{%d}$" % n).scale(self.text_scale)

    def __str__(self):
        return "F_" + str(self.fib_n) + " = " + str(self.result)


class TreeDemoFib(Scene):

    def construct(self):
        fib_n = 6
        text_scale = 0.75
        tree = TreeDemoFib.build_fib_tree(fib_n, text_scale=text_scale)
        tree.layout(1.0, 1.0)
        g = tree.to_vgroup()
        g.center().to_edge(UP)

        self.play(FadeIn(tree.label))
        ctx = {'current_rect': None, 'run_time': 1.0 if fib_n < 6 else 0.25}
        self.run_fib(tree, ctx)
        self.play(FadeOut(ctx['current_rect']))

    @staticmethod
    def build_fib_tree(n, parent=None, text_scale=1.0):
        tree = FibTree(n, parent, text_scale)
        if n == 0:
            tree.result = 0
            return tree
        elif n == 1:
            tree.result = 1
            return tree
        fn1 = TreeDemoFib.build_fib_tree(n - 1, tree)
        fn2 = TreeDemoFib.build_fib_tree(n - 2, tree)
        tree.result = fn1.result + fn2.result
        return tree

    def _update_rect(self, tree, ctx):
        sr = SurroundingRectangle(tree.label)
        if ctx['current_rect']:
            parent_change_anims = []
            if tree.parent is not None:
                parent_change_anims = [tree.parent.label.set_color, ORANGE]
            self.play(ReplacementTransform(ctx['current_rect'], sr),
                      tree.label.set_color,
                      YELLOW,
                      *parent_change_anims,
                      run_time=ctx['run_time'])
        else:
            self.play(ShowCreation(sr),
                      tree.label.set_color,
                      YELLOW,
                      run_time=ctx['run_time'])
        ctx['current_rect'] = sr

    def run_fib(self, tree, ctx):
        self._update_rect(tree, ctx)
        if len(tree.children) > 0:
            lc = tree.children[0]
            rc = tree.children[1]
            lc.label.set_color(BLUE)
            rc.label.set_color(BLUE)
            self.play(*[
                FadeIn(o) for o in
                [lc.label, lc.line_to_parent, rc.label, rc.line_to_parent]
            ],
                      run_time=ctx['run_time'])
            self.run_fib(tree.children[0], ctx)
            self._update_rect(tree, ctx)
            self.run_fib(tree.children[1], ctx)
            self._update_rect(tree, ctx)
        rl = TexMobject(str(tree.result)).scale(tree.text_scale)
        rl.move_to(tree.label)
        rl.set_color(GREEN_SCREEN)
        self.play(ReplacementTransform(tree.label, rl),
                  run_time=ctx['run_time'])


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
                h = c.get_lines_highlight_rect(line_no)
                if last_h:
                    self.play(FadeOut(last_h), FadeIn(h))
                else:
                    self.play(FadeIn(h))
                last_h = h
            self.play(FadeOut(last_h))

            r = c.get_lines_highlight_rect((1, 4))
            self.play(FadeIn(r))
            self.play(FadeOut(r))

            l2 = SurroundingRectangle(c.get_lines(2))
            self.play(Indicate(c.get_lines(3)))
            self.play(Indicate(c.get_lines(3)[1:3]))
            self.play(FadeIn(l2))
            g.add(l2)
            l3 = SurroundingRectangle(c.get_lines(3))
            self.play(ReplacementTransform(l2, l3))
            g.add(l3)

            self.play(ScaleInPlace(g, 0.5))
            last_c = g

        self.wait()


class CodeBlockDemo(Scene):

    def construct(self):
        code_scale = 0.75
        foo_code = CodeBlock(
            'Java',
            r"""
            int foo() {
                int n = bar(2, 1);
                n += bar(2, 2);
                return n;
            }
            """,
            add_labels=True,
            code_scale=code_scale,
        )
        bar_code = CodeBlock(
            'Java',
            r"""
            int bar(int x, int y) {
                if (x == 1) {
                    return y;
                }
                int b = bar(x - 1, y + 1);
                return b;
            }
            """,
            line_offset=5,
            add_labels=True,
            code_scale=code_scale,
        )

        title = TextMobject('CodeBlock Basics Demo')
        title.to_edge(UP)
        foo_code.next_to(title, DOWN)
        foo_code.fade_labels()
        bar_code.next_to(foo_code.get_code(),
                         DOWN,
                         buff=MED_LARGE_BUFF,
                         aligned_edge=LEFT,
                         submobject_to_align=bar_code.get_code())
        self.play(*[FadeIn(o) for o in [title, foo_code, bar_code]])
        self.wait(0.5)

        self.play(foo_code.highlight_lines, 1, bar_code.highlight_lines, (6, 8))
        self.wait(0.5)
        self.play(foo_code.highlight_lines, 2, bar_code.highlight_lines,
                  (8, 10))
        self.play(foo_code.highlight_lines, 3, bar_code.highlight_lines,
                  (10, 12))
        self.wait(0.5)
        self.play(Indicate(foo_code))
        self.wait(0.5)
        self.play(Indicate(bar_code))
        self.wait(0.5)
        self.play(foo_code.remove_highlight, bar_code.remove_highlight)
        self.wait(0.5)
        self.play(FadeOut(foo_code))
        self.wait(0.5)
        self.play(FadeIn(foo_code))
        self.wait(0.5)
        self.play(foo_code.show_labels, bar_code.fade_labels)
        self.wait(0.5)
        self.play(foo_code.fade_labels, bar_code.show_labels)
        self.wait(0.5)

        foo_code.move_hidden_highlight(2)
        bar_code.move_hidden_highlight((8, 10))
        self.wait(0.5)
        self.play(foo_code.highlight_lines, 2, bar_code.highlight_lines,
                  (8, 10))
        self.wait(0.5)
        self.play(foo_code.highlight_lines, 4, bar_code.highlight_lines, (6, 9))
        self.wait(0.5)
        self.play(foo_code.remove_highlight, bar_code.remove_highlight)
        self.wait(0.5)

        self.play(FadeOut(foo_code), FadeOut(bar_code))
        self.wait()


class CodeBlockSteppingDemo(Scene):

    def construct(self):
        code_scale = 0.75
        foo_code = CodeBlock(
            'Java',
            r"""
            int foo() {
                int n = bar(2, 1);
                n += bar(2, 2);
                return n;
            }
            """,
            code_scale=code_scale,
        )
        bar_code = CodeBlock(
            'Java',
            r"""
            int bar(int x, int y) {
                if (x == 1) {
                    return y;
                }
                int b = bar(x - 1, y + 1);
                return b;
            }
            """,
            line_offset=5,
            code_scale=code_scale,
        )
        main_code = CodeBlock('Java', 'off_screen')
        main_code.shift(UP * 8)  # Offscreen up
        self.add(main_code)

        title = TextMobject('CodeBlock Stepping Demo')
        title.to_edge(UP)
        foo_code.next_to(title, DOWN)
        bar_code.next_to(foo_code.get_code(),
                         DOWN,
                         buff=MED_LARGE_BUFF,
                         aligned_edge=LEFT,
                         submobject_to_align=bar_code.get_code())
        self.play(*[FadeIn(o) for o in [title, foo_code, bar_code]])
        self.wait()

        # Step through both code blocks until done.
        xi = main_code.pre_call(foo_code, 1)
        self.play(*main_code.get_control_transfer_counterclockwise(xi))
        foo_code.post_control_transfer(xi, self)

        foo_code.prep_annotations(2, 3)
        foo_code.generate_target().highlight_lines(2).set_annotation(2, 'n: ?')
        self.play(MoveToTarget(foo_code))
        n = self.run_bar(bar_code, foo_code, 2, 2, 1)
        self.play(foo_code.highlight_lines, 3, foo_code.set_annotation, 2, None,
                  foo_code.set_annotation, 3, 'n: %d' % n, bar_code.fade_labels)
        n += self.run_bar(bar_code, foo_code, 3, 2, 2)
        self.play(foo_code.highlight_lines, 4, foo_code.set_annotation, 3,
                  'n: %d' % n)

        xi = foo_code.pre_return(main_code, 1)
        self.play(*foo_code.get_control_transfer_clockwise(xi))
        main_code.post_control_transfer(xi, self)

        self.play(FadeOut(title), FadeOut(foo_code), FadeOut(bar_code))
        self.wait()

    def run_bar(self, bar_code, caller_code, caller_line, x, y):
        self.wait(0.5)
        xi = caller_code.pre_call(bar_code, 6)
        self.play(*caller_code.get_control_transfer_counterclockwise(xi))
        bar_code.post_control_transfer(xi, self)
        self.wait(0.5)

        self.play(bar_code.highlight_lines, 7)
        if x == 1:
            self.play(bar_code.highlight_lines, 8)
            self.wait(0.5)
            xi = bar_code.pre_return(caller_code, caller_line)
            self.play(*bar_code.get_control_transfer_clockwise(xi))
            caller_code.post_control_transfer(xi, self)
            self.wait(0.5)
            return y

        self.play(bar_code.highlight_lines, 10)
        b = self.run_bar(bar_code, bar_code, 10, x - 1, y + 1)

        self.play(bar_code.highlight_lines, 11)
        self.wait(0.5)
        xi = bar_code.pre_return(caller_code, caller_line)
        self.play(*bar_code.get_control_transfer_clockwise(xi))
        caller_code.post_control_transfer(xi, self)
        self.wait(0.5)
        return b


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
