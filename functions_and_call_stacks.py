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
        # r = RoundedRectangle(width=right_x - left_x + 2 * buff,
        r = Rectangle(width=right_x - left_x + 2 * buff,
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

    def highlight_line(self, line_no, color=YELLOW):
        code_line = self.get_line(line_no)
        left_x = self.get_left()[0]
        right_x = code_line.get_right()[0]
        r = self.__get_highlight_rect(left_x, right_x, code_line, color)


class CodeBlock(VGroup):
    CONFIG = {
        'height': 1,
    }

    def __init__(self, language, raw_code_string, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)
        self.callsite_highlight = None
        code_string = CodeTextString(language, raw_code_string)
        highlight_rect = code_string.get_line_highlight_rect(1).set_opacity(0)
        hrg = VGroup(highlight_rect)
        self.add(code_string, hrg)

    def code_string(self):
        return self[0]

    def __highlight_rect_group(self):
        return self[1]

    def highlight_rect(self):
        return self.__highlight_rect_group()[0]

    def highlight_lines(self, lines, color=YELLOW):
        if isinstance(lines, tuple):
            r = self.code_string().get_multiline_highlight_rect(lines[0], lines[1], color=color)
        else:
            r = self.code_string().get_line_highlight_rect(lines, color=color)
        self.highlight_rect().become(r)
        return self

    def fade_out_highlight(self):
        self.highlight_rect().set_opacity(0)

    # Move it without changing it
    def move_highlight_rect(self, line):
        self.highlight_rect().move_to(
            self.code_string().get_line_highlight_rect(line)
        )

    # Returns a from and to highlight rect, each of which are independent of the code block
    def setup_for_call(self, callee):
        hr_from = self.highlight_rect().copy()
        self.callsite_highlight = self.highlight_rect().copy().set_color(WHITE)
        self.highlight_rect().set_opacity(0)
        hr_to = callee.code_string().get_line_highlight_rect(1)
        return hr_from, hr_to

    def highlight_caller(self):
        self.highlight_rect().become(self.callsite_highlight)

    def complete_callee(self, hr, scene):
        scene.remove(hr)
        self.__highlight_rect_group().remove(self.highlight_rect())
        self.__highlight_rect_group().add(hr)

    # Returns a from and to highlight rect, each of which are independent of the code block
    def setup_for_return(self, returnee):
        hr_from = self.highlight_rect().copy()
        self.__highlight_rect_group().remove(self.highlight_rect())
        self.__highlight_rect_group().add(
            self.code_string().get_line_highlight_rect(1).set_opacity(0))
        hr_to = returnee.highlight_rect().copy().set_color(YELLOW)
        return hr_from, hr_to

    def highlight_returnee(self):
        self.highlight_rect().set_opacity(0)

    def complete_returnee(self, hr, scene):
        scene.remove(hr)
        self.__highlight_rect_group().remove(self.highlight_rect())
        self.__highlight_rect_group().add(hr)


class CodeBlockDemo(Scene):
    def construct(self):
        c1 = CodeBlock('Java', r"""
            int foo() {
                int n = bar(1, 2);
                return n;
            }
            """)
        c2 = CodeBlock('Java', r"""
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

        hr_caller, hr_callee = c1.setup_for_call(c2)
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
        hr_caller, hr_callee = c1.setup_for_call(c2)
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


class StackFrame(VGroup):
    CONFIG = {
        'header_scale': 0.75,
    }

    def __init__(self, name, line, vars, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)

        # mmmfixme: prefer this to be static elsewhere
        em = TextMobject('M')
        self.slot_height = em.get_height() + SMALL_BUFF * 2
        self.slot_width = em.get_width() * 4 + SMALL_BUFF * 2

        slots = VGroup()
        self.slot_map = {}
        for i, v in enumerate(vars):
            if isinstance(v, str):
                vn = v
                vv = '-'
            elif isinstance(v, tuple):
                vn, vv = v
                vv = str(vv)
            else:
                vn = str(v)
                vv = '-'
            s = self.build_stack_slot(vn, vv)
            slots.add(s)
            self.slot_map[vn] = i  # Can't remember slot objs because they may change over time
        slots.arrange(DOWN, center=False, buff=0, aligned_edge=RIGHT)  # mmmfixme: check overlap
        frame_name = TextMobject(name + ' line: ', str(line)) \
            .scale(self.header_scale).next_to(slots, UP, buff=SMALL_BUFF)
        self.add(slots, frame_name)
        br = BackgroundRectangle(self, buff=SMALL_BUFF, fill_opacity=0.15)
        br.set_fill(color=[ORANGE, BLUE], opacity=[0.1, 0.2])
        self.add(br)

    def build_stack_slot(self, name, value):
        var_name = TextMobject(name)
        slot_box = Rectangle(height=self.slot_height, width=self.slot_width, stroke_width=1)
        var_value = TextMobject(value)
        var_value.move_to(slot_box)
        var_name.next_to(slot_box, LEFT)
        stack_slot = VGroup(slot_box, var_name, var_value)
        return stack_slot

    def slots(self):
        return self[0]

    def header_line(self):
        return self[1]

    def set_line(self, line):
        t = self.header_line()[1]
        t.become(TextMobject(str(line)).scale(self.header_scale).move_to(t))
        return self

    def update_slot(self, var_name, val):
        si = self.slot_map[var_name]
        s = self.slots()[si]
        s[2].become(TextMobject(str(val)).move_to(s[2]))
        return self


class FrameDemo(Scene):
    def construct(self):
        f1 = StackFrame('foo()', 1, ['a', 'b', ('c', 2)])
        self.play(FadeIn(f1))
        self.play(f1.set_line, 2)
        self.play(f1.set_line, 3)
        self.play(f1.update_slot, 'b', 42)
        self.play(f1.set_line, 4,
                  f1.update_slot, 'a', 43)
        self.play(FadeOut(f1))
        self.wait()


class FACStack(Scene):
    def construct(self):
        high_quality = False

        # - Foo calls bar passing some args. Bar does something, returns.
        foo_code = CodeBlock('Java', r"""
            int foo() {
                int n = bar(1, 2);
                return n;
            }
            """).scale(0.75)
        bar_code = CodeBlock('Java', r"""
            int bar(int x, int y) {
                int a = x + y;
                int b = a * 2;
                return b;
            }
            """).scale(0.75)
        fbg = VGroup(foo_code, bar_code)
        bar_code.next_to(foo_code, DOWN, aligned_edge=LEFT, buff=LARGE_BUFF)
        fbg.to_edge(TOP)
        title = TextMobject('We have two Java functions, foo() and bar()')
        title.to_edge(UP)
        self.play(
            ShowCreation(title),
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
            self.play(ReplacementTransform(VGroup(title, t2), t3))
        else:
            self.play(FadeOut(title), FadeOut(t2), FadeIn(t3))
        self.remove(title, t2)
        title = t3
        self.wait()

        t4 = TextMobject('First, make a place\\\\for each variable')
        t4.next_to(title, DOWN, buff=LARGE_BUFF).to_edge(LEFT)
        self.play(FadeIn(t4))
        self.wait()

        foo_vars = VGroup(TexMobject('n:', '\\_'))
        foo_vars.next_to(foo_code, LEFT, buff=LARGE_BUFF * 2)

        bar_vars = VGroup(
            TexMobject('x:', '\\_'),
            TexMobject('y:', '\\_').shift(DOWN * .75),
            TexMobject('a:', '\\_').shift(DOWN * 1.5),
            TexMobject('b:', '\\_').shift(DOWN * 2.25),
        )
        bar_vars.next_to(bar_code, LEFT, aligned_edge=TOP, buff=LARGE_BUFF * 2)
        self.play(Write(foo_vars))
        self.play(Write(bar_vars))
        self.wait()

        t5 = TextMobject("Start in foo()...")
        t5.move_to(t4, aligned_edge=LEFT)
        self.play(FadeOut(t4), FadeIn(t5))
        self.wait()

        # foo_l2_active = foo_code.get_line_highlight_rect(2)
        if high_quality:
            self.play(
                ReplacementTransform(t5, foo_l2_active),
            )
        else:
            foo_code.move_highlight_rect(2)
            self.play(
                FadeOut(t5),
                foo_code.highlight_lines, 2,
            )
        self.wait()

        foo_n_q = TexMobject('?').move_to(foo_vars[0][1], aligned_edge=BOTTOM).shift(UP * 0.1)
        self.play(Write(foo_n_q))
        foo_vars.add(foo_n_q)
        self.wait()

        hr_caller, hr_callee = foo_code.setup_for_call(bar_code)
        self.play(
            foo_code.highlight_caller,
            ReplacementTransform(hr_caller, hr_callee, path_arc=np.pi),
        )
        bar_code.complete_callee(hr_callee, self)
        self.wait()

        bar_x = TexMobject('1').move_to(bar_vars[0][1], aligned_edge=BOTTOM).shift(UP * 0.1)
        bar_y = TexMobject('2').move_to(bar_vars[1][1], aligned_edge=BOTTOM).shift(UP * 0.1)
        self.play(Write(bar_x), Write(bar_y))
        bar_vars_extras = VGroup()
        bar_vars_extras.add(bar_x, bar_y)
        self.play(bar_code.highlight_lines, 2)
        self.wait()

        bar_a = TexMobject('3').move_to(bar_vars[2][1], aligned_edge=BOTTOM).shift(UP * 0.1)
        self.play(Write(bar_a))
        bar_vars_extras.add(bar_a)
        self.play(bar_code.highlight_lines, 3)
        self.wait()

        bar_b = TexMobject('6').move_to(bar_vars[3][1], aligned_edge=BOTTOM).shift(UP * 0.1)
        self.play(Write(bar_b))
        bar_vars_extras.add(bar_b)
        self.play(bar_code.highlight_lines, 4)
        self.wait()

        hr_returner, hr_returnee = bar_code.setup_for_return(foo_code)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=-np.pi),
            foo_code.highlight_returnee,
        )
        foo_code.complete_returnee(hr_returnee, self)
        self.wait()

        foo_n = TexMobject('6').move_to(foo_vars[0][1], aligned_edge=BOTTOM).shift(UP * 0.1)
        self.play(
            foo_code.highlight_lines, 3,
            ReplacementTransform(foo_n_q, foo_n),
        )
        foo_vars.add(foo_n)
        self.wait()

        # - Now give the variables "homes" in each function. Variables like homes; they're warm
        #   and safe and sized just for them!
        print('Give variables homes')

        t1 = TextMobject('So how does the\\\\computer do this?').to_edge(LEFT)
        self.play(FadeIn(t1), foo_code.fade_out_highlight)
        self.wait()

        t2 = TextMobject('Every variable is stored\\\\someplace in memory').to_edge(LEFT)
        new_title = TextMobject('Where are variables stored?').to_edge(UP)
        self.play(
            FadeOut(t1),
            FadeOut(title),
            FadeIn(new_title),
            FadeIn(t2),
        )
        title = new_title
        self.wait()

        em = TextMobject('M')
        slot_height = em.get_height() + SMALL_BUFF * 2
        slot_width = em.get_width() * 4 + SMALL_BUFF * 2

        def build_var_home(name, value):
            var_name = TextMobject(name)
            slot_box = Rectangle(height=slot_height, width=slot_width, stroke_width=1)
            var_value = TextMobject(value)
            var_value.move_to(slot_box)
            var_name.next_to(slot_box, LEFT)
            stack_slot = VGroup(slot_box, var_name, var_value)
            return stack_slot

        foo_homes = build_var_home('n', '6')
        foo_homes.move_to(foo_vars, aligned_edge=LEFT)
        self.play(ReplacementTransform(foo_vars, foo_homes))
        self.wait()

        bar_var_vals = [('x', '1'), ('y', '2'), ('a', '3'), ('b', '6')]
        bar_homes = VGroup()
        bar_homes_shift = 0
        for n, v in bar_var_vals:
            bar_homes.add(build_var_home(n, v).shift(DOWN * bar_homes_shift))
            bar_homes_shift += 0.75
        bar_homes.move_to(bar_vars, aligned_edge=LEFT)
        t3 = TextMobject("Each variable lives in a\\\\``slot''").to_edge(LEFT)
        self.play(
            ReplacementTransform(bar_vars, bar_homes),
            # FadeOut(bar_vars),
            FadeOut(bar_vars_extras),
            FadeIn(bar_homes),
        )
        self.wait()
        self.play(
            FadeOut(t2),
            FadeIn(t3),
        )
        self.wait()

        # - Now arrange the homes into a "stack frame".
        print('Build stack frames')

        t4 = TextMobject("All slots for a function\\\\are put together in a\\\\``frame''")
        t4.to_edge(LEFT)
        self.play(FadeOut(t3), FadeIn(t4))

        foo_vars = [('n', '6')]
        foo_frame = StackFrame('foo()', 3, foo_vars)
        foo_frame.move_to(foo_homes, aligned_edge=LEFT)
        self.play(ReplacementTransform(foo_homes, foo_frame))
        self.wait()

        bar_frame = StackFrame('bar(1,2)', 4, bar_var_vals)
        bar_frame.move_to(bar_homes, aligned_edge=LEFT)
        self.play(ReplacementTransform(bar_homes, bar_frame))
        self.wait()

        t5 = TextMobject("They're happy and warm\\\\together!").next_to(t4, DOWN, buff=LARGE_BUFF)
        self.play(FadeIn(t5))
        self.wait()

        # mmmfixme: consider focusing on a frame a moment and addressing what's in it.
        # - current location within the function
        # - slots for every argument and local

        # Cool, so where do frames live?
        print('Where do frames live')
        t6 = TextMobject('So where do frames live?').to_edge(LEFT)
        self.play(
            FadeOut(t5),
            FadeOut(t4),
            FadeIn(t6),
        )
        self.wait()

        t7 = TextMobject("On the ``call stack''!").next_to(t6, DOWN, buff=LARGE_BUFF)
        self.play(FadeIn(t7))
        self.wait()

        # mmmfixme: add a small animation of a stack in action, push and pop, during this part.
        new_title = TextMobject('The Call Stack').to_edge(UP)
        t1 = TextMobject('Function calls push a new frame\\\\onto the call stack')\
            .to_edge(LEFT).shift(UP)
        t2 = TextMobject('Returning pops a frame off\\\\the stack').next_to(t1, DOWN, buff=LARGE_BUFF)

        self.play(
            ReplacementTransform(title, new_title),
            FadeOut(t6),
            FadeOut(t7),
            FadeOut(foo_frame),
            FadeOut(bar_frame),
            FadeIn(t1),
        )
        title = new_title
        self.wait()

        self.play(FadeIn(t2))
        self.wait()

        t3 = TextMobject("Let's run again and see\\\\the call stack in action...").to_edge(LEFT)
        self.play(
            FadeOut(t1),
            FadeOut(t2),
            FadeIn(t3)
        )
        self.wait()

        print('Run with real call stack')

        # mmmfixme: need all the frames to be the same width.
        # mmmfixme: give a background to the entire stack, to illustrate it's a thing?
        foo_frame = StackFrame('foo()', 2, ['n'])
        foo_frame.to_edge(DOWN)

        foo_code.move_highlight_rect(2)
        self.play(
            FadeInFromDown(foo_frame),
            foo_code.highlight_lines, 2,
            FadeOut(t3),
        )
        self.wait()

        t1 = TextMobject('Calling bar()\\\\pushes a frame').to_edge(LEFT)
        bar_frame = StackFrame('bar(1, 2)', 1, ['x', 'y', 'a', 'b'])
        bar_frame.next_to(foo_frame, UP, buff=SMALL_BUFF)
        hr_caller, hr_callee = foo_code.setup_for_call(bar_code)
        self.play(
            foo_code.highlight_caller,
            ReplacementTransform(hr_caller, hr_callee, path_arc=np.pi),
            FadeIn(t1),
            FadeInFrom(bar_frame, UP),
        )
        bar_code.complete_callee(hr_callee, self)
        self.wait()

        self.play(
            bar_frame.update_slot, 'x', 1,
            bar_frame.update_slot, 'y', 2,
            FadeOut(t1),
        )
        self.play(bar_code.highlight_lines, 2, bar_frame.set_line, 2)
        self.wait()

        self.play(bar_frame.update_slot, 'a', 3)
        self.play(bar_code.highlight_lines, 3, bar_frame.set_line, 3)
        self.wait()

        self.play(bar_frame.update_slot, 'b', 6)
        self.play(bar_code.highlight_lines, 4, bar_frame.set_line, 4)
        self.wait()

        t1 = TextMobject("Returning pops\\\\bar's frame").to_edge(LEFT)
        hr_returner, hr_returnee = bar_code.setup_for_return(foo_code)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=-np.pi),
            foo_code.highlight_returnee,
            Uncreate(bar_frame),
            FadeIn(t1),
        )
        foo_code.complete_returnee(hr_returnee, self)
        self.wait()

        self.play(
            foo_code.highlight_lines, 3,
            foo_frame.set_line, 3,
            foo_frame.update_slot, 'n', 6,
            FadeOut(t1),
        )
        self.wait()

        # self.play(foo_code.fade_out_highlight)
        # self.wait()

        # self.play(FadeOut(bar_frame), FadeOut(foo_frame))
        # self.wait()





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







