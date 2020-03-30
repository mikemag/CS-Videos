from manimlib.imports import *

import pygments
import pygments.lexers
from pygments.formatters import LatexFormatter



class FACIntro(Scene):
    def construct(self):
        t1 = TextMobject('Functions and Call Stacks')
        t1.scale(1.5).to_edge(TOP)
        self.play(ShowCreation(t1))
        self.wait()

        # Why?
        # * Understand the mechanics behind a function call.
        # * Helps to better understand pass by reference for languages that support it.
        # * Helps to better understand passing object references in all languages.
        # * Helps to better understand recursion.

        # So let's get to it!


# TODO: requires the mods to SVGMobject to respect fill colors.
class CodeTextString(SingleStringTexMobject):
    CONFIG = {
        'alignment': '',
        # TODO: could use a different template, or generate it once given a Pygments style.
        # - Also, can get the extra style code from LatexFormatter().get_style_defs()
        'template_tex_file_body': TEMPLATE_TEXT_FILE_BODY,
        'arg_separator': '',
        'line_tolerance': 0.2,  # Delta in y to determine line breaks from the SVG
    }

    def __init__(self, language, raw_code_string, **kwargs):
        digest_config(self, kwargs, locals())
        lexer = pygments.lexers.get_lexer_by_name(language)
        code = pygments.highlight(raw_code_string, lexer, LatexFormatter())
        super().__init__(code, **kwargs)
        self.raw_code_string = raw_code_string
        self.latex_code_string = code

        # The original LaTeX string has newlines in it, which makes it easy to separate.
        # The first and last lines are boilerplate from Pygments, so discard them.
        self.tex_strings = self.latex_code_string.splitlines()
        self.tex_strings = self.tex_strings[1:-1]

        # If the last line is empty it's okay, just trim it off too.
        if len(self.tex_strings[-1].strip()) == 0:
            self.tex_strings = self.tex_strings[:-1]

        self.break_up_by_lines()

    # Pygments has full control over the generated TeX, so let's not muck with it!
    def modify_special_strings(self, tex):
        return tex

    # Pick apart the code into individual lines, with the string that generated them.
    # This is much like TexMobject.break_up_by_substrings().
    # TODO: doesn't handle blank lines in the middle of the source...
    def break_up_by_lines(self):
        # The submobjects have no association with the original input, but they do have x,y coords.
        # So we can break lines by changes in Y. The lines are presented in-order in the SVG, too.
        new_submobjects = []
        current_line_y = self.submobjects[0].get_center()[1] - self.line_tolerance * 2
        line_group = None

        for o in self.submobjects:
            y = o.get_center()[1]
            if abs(y - current_line_y) > self.line_tolerance:
                if line_group:
                    new_submobjects.append(line_group)
                current_line_y = y
                line_group = VGroup()
            line_group.add(o)

        new_submobjects.append(line_group)  # Pickup the last group

        if len(new_submobjects) != len(self.tex_strings):
            warnings.warn('%s: split SVG into %d lines, but there are %d lines in the original '
                          'LaTeX from Pygments! See %s' % (self.name, len(new_submobjects),
                                                           len(self.tex_strings), self.file_path))

        self.submobjects = new_submobjects
        return self

    # The SVG is nicely colored for us, so don't try to adjust it further after we've gone to
    # all the work to import those colors from the SVG.
    # TODO: factor this better with the superclass.
    def init_colors(self):
        self.set_fill(
            # color=self.fill_color or self.color,
            opacity=self.fill_opacity,
        )
        self.set_stroke(
            # color=self.stroke_color or self.color,
            width=self.stroke_width,
            opacity=self.stroke_opacity,
        )
        self.set_background_stroke(
            color=self.background_stroke_color,
            width=self.background_stroke_width,
            opacity=self.background_stroke_opacity,
        )
        self.set_sheen(
            factor=self.sheen_factor,
            direction=self.sheen_direction,
        )
        return self

    # Line numbers start at 1
    def get_line(self, line_no):
        return self[line_no - 1]

    def __get_highlight_rect(self, left_x, right_x, lines_obj, color):
        buff = SMALL_BUFF
        r = RoundedRectangle(width=right_x - left_x + 2 * buff,
                      height=lines_obj.get_height() + 2 * buff,
                      stroke_width=0, stroke_opacity=0, fill_color=color,
                      fill_opacity=0.2, corner_radius=0.1)
        r.move_to(lines_obj, aligned_edge=RIGHT).shift(RIGHT * buff)
        return r

    def get_line_highlight_rect(self, line_no, color=YELLOW):
        code_line = self.get_line(line_no)
        left_x = self.get_left()[0]
        right_x = code_line.get_right()[0]
        return self.__get_highlight_rect(left_x, right_x, code_line, color)

    def get_multiline_highlight_rect(self, start_line_no, end_line_no, color=WHITE):
        g = VGroup(self[start_line_no-1:end_line_no])
        left_x = self.get_left()[0]
        right_x = g.get_right()[0]
        return self.__get_highlight_rect(left_x, right_x, g, color)


class FACStack(Scene):
    def construct(self):
        high_quality = False

        # - Foo calls bar passing some args. Bar does something, returns.
        foo_code = CodeTextString('Java', r"""
            int foo() {
                int n = bar(1, 2);
                return n;
            }
            """).scale(0.75)
        bar_code = CodeTextString('Java', r"""
            int bar(int x, int y) {
                int a = x + y;
                int b = a * 2;
                return b;
            }
            """).scale(0.75)
        fbg = VGroup(foo_code, bar_code)
        bar_code.next_to(foo_code, DOWN, aligned_edge=LEFT, buff=LARGE_BUFF)
        fbg.to_edge(TOP)
        t1 = TextMobject('We have two Java functions, foo() and bar()')
        t1.to_edge(UP)
        self.play(
            ShowCreation(t1),
            FadeInFromDown(fbg),
        )
        self.wait()

        # Let's write down what happens when we run this.
        t2 = TextMobject("Let's run them and write down\\\\"
                         "each variable as we go..."
                         )
        t2.to_edge(LEFT)
        self.play(Write(t2), fbg.to_edge, RIGHT)
        self.wait()

        t3 = TextMobject('Running foo() and bar() by hand').to_edge(UP)
        if high_quality:
            self.play(ReplacementTransform(VGroup(t1, t2), t3))
        else:
            self.play(FadeOut(t1), FadeOut(t2), FadeIn(t3))
        self.remove(t1, t2)
        t1 = t3
        self.wait()

        t4 = TextMobject('First, make a place\\\\for each variable')
        t4.next_to(t1, DOWN, buff=LARGE_BUFF).to_edge(LEFT)
        self.play(FadeIn(t4))
        self.wait()

        foo_vars = VGroup(TexMobject('n:', '\\_'))
        foo_vars.next_to(foo_code, LEFT, buff=LARGE_BUFF * 2)

        bar_vars = VGroup(
            TexMobject('x:', '\\_'),
            TexMobject('y:', '\\_').shift(DOWN*.75),
            TexMobject('a:', '\\_').shift(DOWN*1.5),
            TexMobject('b:', '\\_').shift(DOWN*2.25),
        )
        bar_vars.next_to(bar_code, LEFT, aligned_edge=TOP, buff=LARGE_BUFF * 2)
        self.play(Write(foo_vars))
        self.play(Write(bar_vars))
        self.wait()

        t5 = TextMobject("Start in foo()...")
        t5.move_to(t4, aligned_edge=LEFT)
        self.play(FadeOut(t4), FadeIn(t5))
        self.wait()

        foo_l2_active = foo_code.get_line_highlight_rect(2)
        self.play(
            # FadeOut(t5),
            # FadeIn(foo_l2_active),
            ReplacementTransform(t5, foo_l2_active)
        )
        self.wait()

        foo_n_q = TexMobject('?').move_to(foo_vars[0][1], aligned_edge=BOTTOM).shift(UP * 0.1)
        self.play(Write(foo_n_q))
        self.wait()

        foo_l2_inactive = foo_code.get_line_highlight_rect(2, color=WHITE)
        bar_l1 = bar_code.get_line_highlight_rect(1)
        self.play(
            FadeIn(foo_l2_inactive),
            ReplacementTransform(foo_l2_active, bar_l1, path_arc=np.pi)
        )
        self.wait()

        bar_x = TexMobject('1').move_to(bar_vars[0][1], aligned_edge=BOTTOM).shift(UP * 0.1)
        bar_y = TexMobject('2').move_to(bar_vars[1][1], aligned_edge=BOTTOM).shift(UP * 0.1)
        self.play(Write(bar_x), Write(bar_y))
        bar_l2 = bar_code.get_line_highlight_rect(2)
        self.play(FadeOut(bar_l1), FadeIn(bar_l2))
        self.wait()

        bar_a = TexMobject('3').move_to(bar_vars[2][1], aligned_edge=BOTTOM).shift(UP * 0.1)
        self.play(Write(bar_a))
        bar_l3 = bar_code.get_line_highlight_rect(3)
        self.play(FadeOut(bar_l2), FadeIn(bar_l3))
        self.wait()

        bar_b = TexMobject('6').move_to(bar_vars[3][1], aligned_edge=BOTTOM).shift(UP * 0.1)
        self.play(Write(bar_b))
        bar_l4 = bar_code.get_line_highlight_rect(4)
        self.play(FadeOut(bar_l3), FadeIn(bar_l4))
        self.wait()

        foo_l2_new = foo_code.get_line_highlight_rect(2, color=YELLOW)
        self.play(
            ReplacementTransform(bar_l4, foo_l2_new, path_arc=-np.pi),
            FadeOut(foo_l2_inactive),
        )
        self.wait()

        foo_l3 = foo_code.get_line_highlight_rect(3)
        foo_n = TexMobject('6').move_to(foo_vars[0][1], aligned_edge=BOTTOM).shift(UP * 0.1)
        self.play(
            FadeOut(foo_l2_new),
            FadeIn(foo_l3),
            ReplacementTransform(foo_n_q, foo_n),
        )
        # self.play(FadeOut(foo_l3))
        self.wait()

        # - Now give the variables "homes" in each function. Variables like homes; they're warm
        #   and safe and sized just for them!
        # - Now arrange the homes into a "stack frame".
        return
        print('Build stack frames')
        self.play(FadeOut(VGroup(foo_vars, bar_vars)))

        em = TextMobject('M')
        slot_height = em.get_height() + SMALL_BUFF * 2
        slot_width = em.get_width() * 4 + SMALL_BUFF * 2


        def build_stack_slot(name, value):
            var_name = TextMobject(name)
            slot_box = Rectangle(height=slot_height, width=slot_width, stroke_width=1)
            var_value = TextMobject(value)
            var_value.move_to(slot_box)
            var_name.next_to(slot_box, LEFT)
            stack_slot = VGroup(slot_box, var_name, var_value)
            return stack_slot

        def build_stack_frame(func_name, return_tag, vars):
            f = VGroup()
            for n, v in vars:
                f.add(build_stack_slot(n, v))

            f.arrange(DOWN, center=False, buff=0, aligned_edge=RIGHT)

            f.shift(RIGHT)
            frame_function_name = TextMobject(func_name).scale(0.5)
            # frame_function_name.rotate(np.pi / 2)
            frame_function_name.next_to(f, UP, buff=SMALL_BUFF)
            f.add(frame_function_name)

            # frame_return_tag = TextMobject(return_tag).scale(0.5)
            # frame_return_tag.next_to(f, DOWN, buff=SMALL_BUFF)
            # f.add(frame_return_tag)

            fr = BackgroundRectangle(f, buff=SMALL_BUFF)
            fr.set_fill(color=[ORANGE, BLUE], opacity=[0.1, 0.2])
            f.add(fr)
            return f

        foo_vars = [('n', '')]
        foo_frame = build_stack_frame('foo() line 2', 'Return to main()', foo_vars)
        foo_frame.to_edge(LEFT)
        self.play(FadeIn(foo_frame))
        self.wait()

        bar_vars = [('x', '1'), ('y', '2'), ('a', '3'), ('b', '6')]
        bar_frame = build_stack_frame('bar(1, 2) line 4', 'Return to foo() line 2', bar_vars)

        self.play(
            foo_frame.shift, DOWN * 2,
        )
        bar_frame.next_to(foo_frame, UP)
        self.play(
            FadeIn(bar_frame),
        )

        self.wait()






        # So, we've written down the values to track the as the program runs.
        # The computer has to do something similar, right? It has to have places for the variables,
        # and it has to keep track of them.
        # Let's morph this into something more formal, and closer to what the computer does.
        # Every variable has a piece of memory it lives in. It's home.

        # Put a variable in a box as it's "home".
        # Boxes should be a consistent size, regardless of primitive datatype.
        # Variable name to the left of the box, value in the box.
        # Variable name font can be the default, value should be fixed.
        # Value for references should be something like "Reference to object" or "Reference to <object name>"
        # Want to be able to create a frame given a list of variables and their initial values.
        # Want to be able to update a value easily given a variable name.
        # Return address should be "Return to foo() line 2"



        # - Slide in a call stack, starting with main() at the bottom.
        # - Show foo ready to call bar.
        # - Make the call, see the stack frame added to the stack for bar with room for the variables.
        # - Init the variables.
        # - Run thru bar and show the variables change.
        # - Then return back to foo and show the bar frame go away.
        # - Now do it again for different args to bar.
        # - Now let bar call baz.
        # - And finally return to main.
        # - Add a concept for the return address.
        # - Don't need to get into addresses of code. Perhaps just consider it "code locations"
        #   or something.


class CodeTestStringDemo(Scene):
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

            r = c.get_multiline_highlight_rect(1, 3)
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







