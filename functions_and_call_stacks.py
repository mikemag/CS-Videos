from manimlib.imports import *

import pygments
import pygments.lexers
from pygments.formatters import LatexFormatter


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

    def get_line_highlight_rect(self, lines, color=YELLOW):
        if isinstance(lines, tuple):
            code_line = VGroup(self[lines[0] - 1:lines[1]])
        else:
            code_line = self.get_line(lines)
        left_x = self.get_left()[0]
        right_x = code_line.get_right()[0]
        return self.__get_highlight_rect(left_x, right_x, code_line, color)

    # def highlight_line(self, line_no, color=YELLOW):
    #     code_line = self.get_line(line_no)
    #     left_x = self.get_left()[0]
    #     right_x = code_line.get_right()[0]
    #     r = self.__get_highlight_rect(left_x, right_x, code_line, color)


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
    def setup_for_call(self, callee, lines):
        hr_from = self.highlight_rect().copy()
        self.callsite_highlight = self.highlight_rect().copy().set_color(WHITE)
        self.highlight_rect().set_opacity(0)
        hr_to = callee.code_string().get_line_highlight_rect(lines)
        return hr_from, hr_to

    def highlight_caller(self):
        self.highlight_rect().become(self.callsite_highlight)

    def complete_callee(self, hr, scene):
        scene.remove(hr)
        self.__highlight_rect_group().remove(self.highlight_rect())
        self.__highlight_rect_group().add(hr)

    # Returns a from and to highlight rect, each of which are independent of the code block
    def setup_for_return(self, returnee):
        hr_to = returnee.highlight_rect().copy().set_color(YELLOW)
        hr_from = self.highlight_rect().copy()
        self.__highlight_rect_group().remove(self.highlight_rect())
        self.__highlight_rect_group().add(
            self.code_string().get_line_highlight_rect(1).set_opacity(0))
        return hr_from, hr_to

    def highlight_returnee(self):
        self.highlight_rect().set_opacity(0)

    def complete_returnee(self, hr, scene):
        scene.remove(hr)
        self.__highlight_rect_group().remove(self.highlight_rect())
        self.__highlight_rect_group().add(hr)

    def add_line_labels(self, start_line):
        llg = VGroup()
        code_string = self.code_string()
        x = code_string.get_line(1).get_left()[0] - MED_SMALL_BUFF
        target_point = np.array([x, 0, 0])
        for i in range(len(self.code_string())):
            tn = TextMobject(str(i + start_line)).scale(0.5)
            target_point[1] = code_string.get_line(i + 1).get_center()[1]
            tn.move_to(target_point, aligned_edge=RIGHT)
            llg.add(tn)
        self.add(llg)
        return self

    def remove_line_labels(self):
        self.remove(self[2])
        return self


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
        c1.add_line_labels(1)
        c2.add_line_labels(5)
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


class StackFrame(VGroup):
    CONFIG = {
        'text_scale': 0.75,
        'width': 2,
    }

    def __init__(self, name, line, vars, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)

        em = TextMobject('M').scale(self.text_scale)
        self.slot_height = em.get_height() + SMALL_BUFF * 2
        self.slot_width = em.get_width() * 5 + SMALL_BUFF * 2

        slots = VGroup()
        self.slot_map = {}
        for i, v in enumerate(vars):
            if isinstance(v, str):
                vn = v
                vv = '-'
            elif isinstance(v, tuple):
                vn, vv = v
            else:
                vn = str(v)
                vv = '-'
            s = self.build_stack_slot(vn, vv)
            slots.add(s)
            self.slot_map[vn] = i  # Can't remember slot objs because they may change over time
        slots.arrange(DOWN, center=False, buff=0, aligned_edge=RIGHT)
        frame_name = TextMobject(name + ' line: ', str(line)) \
            .scale(self.text_scale).next_to(slots, UP, buff=SMALL_BUFF)
        self.add(slots, frame_name)
        self.center()
        backbone = Line().set_opacity(0).set_width(self.width)
        self.add(backbone)
        br = BackgroundRectangle(self, buff=SMALL_BUFF, fill_opacity=0.15)
        # This fill used ot have an opacity gradient, opacity=[0.1, 0.2], but it caused noticalbe
        # banding in the final gradient. Shame, it was cool otherwise.
        br.set_fill(color=[ORANGE, BLUE])
        self.add(br)

    def build_stack_slot(self, name, value):
        var_name = TextMobject(name).scale(self.text_scale)
        slot_box = Rectangle(height=self.slot_height, width=self.slot_width, stroke_width=1)
        if isinstance(value, Mobject):
            var_value = value
        else:
            var_value = TextMobject(str(value)).scale(self.text_scale)
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
        t.become(TextMobject(str(line)).scale(self.text_scale).move_to(t))
        return self

    def update_slot(self, var_name, val):
        si = self.slot_map[var_name]
        s = self.slots()[si]
        s[2].become(TextMobject(str(val)).scale(self.text_scale).move_to(s[2]))
        return self


class StackFrameDemo(Scene):
    def construct(self):
        frame_width = 3
        f1 = StackFrame('foo()', 1, ['a', 'b', ('c', 2)], width=frame_width)
        self.play(FadeIn(f1))
        self.play(f1.set_line, 2)
        self.play(f1.set_line, 3)
        self.play(f1.update_slot, 'b', 42)
        self.play(f1.set_line, 4,
                  f1.update_slot, 'a', 43)

        f2 = StackFrame('bar(1, 2, 3)', 1, ['x'], width=frame_width)
        f2.next_to(f1, DOWN, buff=SMALL_BUFF)
        self.play(FadeIn(f2))
        self.wait()

        self.play(FadeOut(f1), FadeOut(f2))
        self.wait()


class FACIntro(Scene):
    def construct(self):
        t1 = TextMobject('Call Stacks')
        t1.scale(1.5).to_edge(UP)
        self.play(ShowCreation(t1))
        self.wait(duration=0.5)

        # Background information on call stacks, foundation for other concepts which build upon this.
        t2 = TextMobject("Learning the basics of the ``call stack'' helps with\\\\many "
                         'concepts in CS:', alignment='').shift(UP)
        bl = BulletedList('pass-by-value vs. pass-by-reference',
                          'passing object references',
                          'recursion',
                          'debuggers',
                          buff=MED_SMALL_BUFF)
        bl.next_to(t2, DOWN)
        self.play(FadeInFromDown(t2))
        self.wait()

        for l in bl:
            self.play(FadeInFromDown(l))
            self.wait()
        self.wait(duration=2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()


class FACStack(Scene):
    def construct(self):
        high_quality = False

        # - Foo calls bar passing some args. Bar does something, returns.
        code_scale = 0.75
        main_code = CodeBlock('Java', r"""
            public static
            void main(String[] args) {
                foo();
            }
            """).scale(code_scale)
        foo_code = CodeBlock('Java', r"""
            static int foo() {
                int n = bar(1, 2);
                return n;
            }
            """).scale(code_scale)
        bar_code = CodeBlock('Java', r"""
            static int bar(int x,
                           int y) {
                int a = x + y;
                int b = a * 2;
                return b;
            }
            """).scale(code_scale)
        fbg = VGroup(foo_code, bar_code)
        bar_code.next_to(foo_code, DOWN, aligned_edge=LEFT, buff=LARGE_BUFF)
        fbg.to_edge(TOP)
        title = TextMobject('We have two Java functions, foo() and bar()')
        title.to_edge(UP)
        self.play(
            ShowCreation(title),
            FadeInFromDown(fbg),
        )
        self.wait(duration=2)

        # Let's write down what happens when we run this.
        t2 = TextMobject("Let's run them and write down\\\\"
                         "each variable as we go..."
                         )
        t2.to_edge(LEFT)
        self.play(Write(t2), fbg.to_edge, RIGHT, {'buff': MED_SMALL_BUFF})
        self.wait()

        t3 = TextMobject('Running foo() and bar() by hand').to_edge(UP)
        if high_quality:
            self.play(ReplacementTransform(VGroup(title, t2), t3))
        else:
            self.play(FadeOut(title), FadeOut(t2), FadeIn(t3))
        self.remove(title, t2)
        title = t3
        self.wait()

        t4 = TextMobject('First, make a place\\\\to write each variable')
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

        hr_caller, hr_callee = foo_code.setup_for_call(bar_code, (1, 2))
        self.play(
            foo_code.highlight_caller,
            ReplacementTransform(hr_caller, hr_callee, path_arc=np.pi),
        )
        bar_code.complete_callee(hr_callee, self)
        self.wait()

        bar_x = TexMobject('1').move_to(bar_vars[0][1], aligned_edge=BOTTOM).shift(UP * 0.1)
        bar_y = TexMobject('2').move_to(bar_vars[1][1], aligned_edge=BOTTOM).shift(UP * 0.1)
        a = Arrow(bar_code.code_string().get_line(2), VGroup(bar_x, bar_y).get_right(), stroke_width=3)
        self.play(Write(bar_x), Write(bar_y), ShowCreationThenDestruction(a))
        bar_vars_extras = VGroup()
        bar_vars_extras.add(bar_x, bar_y)
        self.play(bar_code.highlight_lines, 3)
        self.wait()

        bar_a = TexMobject('3').move_to(bar_vars[2][1], aligned_edge=BOTTOM).shift(UP * 0.1)
        a = Arrow(bar_code.code_string().get_line(3), bar_a.get_right(), stroke_width=3)
        self.play(Write(bar_a), ShowCreationThenDestruction(a))
        bar_vars_extras.add(bar_a)
        self.play(bar_code.highlight_lines, 4)
        self.wait()

        bar_b = TexMobject('6').move_to(bar_vars[3][1], aligned_edge=BOTTOM).shift(UP * 0.1)
        a = Arrow(bar_code.code_string().get_line(4), bar_b.get_right(), stroke_width=3)
        self.play(Write(bar_b), ShowCreationThenDestruction(a))
        bar_vars_extras.add(bar_b)
        self.play(bar_code.highlight_lines, 5)
        self.wait()

        hr_returner, hr_returnee = bar_code.setup_for_return(foo_code)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=-np.pi),
            foo_code.highlight_returnee,
        )
        foo_code.complete_returnee(hr_returnee, self)
        self.wait()

        foo_n = TexMobject('6').move_to(foo_vars[0][1], aligned_edge=BOTTOM).shift(UP * 0.1)
        a = Arrow(foo_code.code_string().get_line(2), foo_n.get_right(), stroke_width=3)
        self.play(
            foo_code.highlight_lines, 3,
            ReplacementTransform(foo_n_q, foo_n),
            ShowCreationThenDestruction(a),
        )
        foo_vars.add(foo_n)
        self.wait()

        # - Now give the variables "homes" in each function. Variables like homes; they're warm
        #   and safe and sized just for them!
        print('Give variables homes')

        t1 = TextMobject('So how does the\\\\computer do this?').to_edge(LEFT)
        self.play(FadeIn(t1), foo_code.fade_out_highlight)
        self.wait(duration=2)

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

        frame_width = 2.8
        foo_vars = [('n', '6')]
        foo_frame = StackFrame('foo()', 3, foo_vars, width=frame_width)
        foo_frame.move_to(foo_homes, aligned_edge=LEFT).shift(LEFT * .5)
        self.play(ReplacementTransform(foo_homes, foo_frame))
        self.wait()

        bar_frame = StackFrame('bar(1,2)', 9, bar_var_vals, width=frame_width)
        bar_frame.move_to(bar_homes, aligned_edge=LEFT).shift(LEFT * .5)
        self.play(ReplacementTransform(bar_homes, bar_frame))
        self.wait()

        t5 = TextMobject("\\textit{They're happy and warm\\\\together!}")\
            .scale(0.75).next_to(t4, DOWN, buff=LARGE_BUFF)
        self.play(FadeIn(t5))
        self.wait()

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

        new_title = TextMobject('The Call Stack').to_edge(UP)
        t1 = TextMobject('Function calls push a new frame\\\\onto the stack')\
            .to_edge(LEFT).shift(UP)
        t2 = TextMobject('Returning pops a frame off\\\\the stack').next_to(t1, DOWN, buff=LARGE_BUFF)

        box_count = 8
        colors = color_gradient([BLUE, ORANGE], box_count)
        little_boxes = VGroup(*[Rectangle(height=0.25, width=0.75, fill_opacity=1, color=colors[i])
                                for i in range(box_count)])
        little_boxes.arrange(UP, buff=0.1)
        little_boxes.next_to(VGroup(foo_code, bar_code), LEFT, buff=LARGE_BUFF)

        self.play(
            ReplacementTransform(title, new_title),
            FadeOut(t6),
            FadeOut(t7),
            FadeOut(foo_frame),
            FadeOut(bar_frame),
            FadeIn(t1),
            LaggedStartMap(FadeInFrom, little_boxes, lambda m: (m, UP), lag_ratio=1.0, run_time=4.0),
        )
        title = new_title
        self.wait()

        self.play(
            FadeIn(t2),
            LaggedStartMap(FadeOutAndShift, VGroup(*reversed(little_boxes)),
                                                   lambda m: (m, UP), lag_ratio=1.0,
                                                   run_time=4.0),
        )
        self.wait(duration=1)

        t3 = TextMobject("Let's run again and see\\\\the call stack in action...").to_edge(LEFT)
        t3.shift(UP)
        self.play(
            FadeOut(t1),
            FadeOut(t2),
            FadeIn(t3)
        )
        self.wait()

        print('Run with real call stack')

        # Let's also put main() into the picture. Start it off-frame upper right
        t4 = TextMobject("... and get main()\\\\into the picture.")\
            .next_to(t3, DOWN, buff=LARGE_BUFF)
        main_code.next_to(title, DOWN, buff=MED_SMALL_BUFF).to_edge(RIGHT)
        main_code.shift(UP * 3 + RIGHT * 3)
        g = VGroup(main_code, foo_code, bar_code)
        self.play(
            g.arrange, DOWN, {'aligned_edge': LEFT, 'buff': MED_SMALL_BUFF},
            g.next_to, title, DOWN, {'buff': MED_SMALL_BUFF},
            g.to_edge, RIGHT,
            FadeInFromDown(t4),
        )
        self.wait(duration=2)

        t1 = TextMobject('Start in main()...')
        t1.next_to(title, DOWN, buff=LARGE_BUFF).to_edge(LEFT)
        frame_width = 3.0
        args_ref = TextMobject('[ ]').scale(0.5)
        main_frame = StackFrame('main()', 3, [('args', args_ref)], width=frame_width)
        main_frame.next_to(g, LEFT, buff=LARGE_BUFF).to_edge(DOWN)
        main_code.move_highlight_rect(3)
        self.play(
            FadeIn(t1),
            FadeInFromDown(main_frame),
            main_code.highlight_lines, 3,
            FadeOut(t3),
            FadeOut(t4),
        )
        self.wait()

        foo_frame = StackFrame('foo()', 5, ['n'], width=frame_width)
        foo_frame.next_to(main_frame, UP, buff=SMALL_BUFF)
        b1 = BraceLabel(foo_frame, 'Calling foo()\\\\pushes a frame',
                        brace_direction=LEFT, label_constructor=TextMobject)
        hr_caller, hr_callee = main_code.setup_for_call(foo_code, 1)
        self.play(
            main_code.highlight_caller,
            ReplacementTransform(hr_caller, hr_callee, path_arc=np.pi),
            FadeInFrom(foo_frame, UP),
            FadeInFrom(b1, UP),
            FadeOut(t1),
        )
        foo_code.complete_callee(hr_callee, self)
        self.wait(duration=2)

        self.play(foo_code.highlight_lines, 2, foo_frame.set_line, 6, FadeOut(b1))
        self.wait()

        bar_frame = StackFrame('bar(1, 2)', 10, ['x', 'y', 'a', 'b'], width=frame_width)
        bar_frame.next_to(foo_frame, UP, buff=SMALL_BUFF)
        b1 = BraceLabel(bar_frame, 'Calling bar()\\\\pushes a frame',
                        brace_direction=LEFT, label_constructor=TextMobject)
        hr_caller, hr_callee = foo_code.setup_for_call(bar_code, (1, 2))
        self.play(
            foo_code.highlight_caller,
            ReplacementTransform(hr_caller, hr_callee, path_arc=np.pi),
            FadeInFrom(bar_frame, UP),
            FadeInFrom(b1, UP),
        )
        bar_code.complete_callee(hr_callee, self)
        self.wait()

        self.play(
            bar_frame.update_slot, 'x', 1,
            bar_frame.update_slot, 'y', 2,
            FadeOut(b1),
        )
        self.play(bar_code.highlight_lines, 3, bar_frame.set_line, 11)
        self.wait()

        self.play(bar_frame.update_slot, 'a', 3)
        self.play(bar_code.highlight_lines, 4, bar_frame.set_line, 12)
        self.wait()

        self.play(bar_frame.update_slot, 'b', 6)
        self.play(bar_code.highlight_lines, 5, bar_frame.set_line, 13)
        b1 = BraceLabel(bar_frame, "Returning pops\\\\bar's frame",
                        brace_direction=LEFT, label_constructor=TextMobject)
        self.play(FadeIn(b1))
        self.wait(duration=2)

        hr_returner, hr_returnee = bar_code.setup_for_return(foo_code)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=-np.pi),
            foo_code.highlight_returnee,
            Uncreate(bar_frame),
            FadeOut(b1),
        )
        foo_code.complete_returnee(hr_returnee, self)
        self.wait()

        self.play(
            foo_code.highlight_lines, 3,
            foo_frame.set_line, 7,
            foo_frame.update_slot, 'n', 6,
        )
        b1 = BraceLabel(foo_frame, "Returning pops\\\\foo's frame",
                        brace_direction=LEFT, label_constructor=TextMobject)
        self.play(FadeIn(b1))
        self.wait()

        hr_returner, hr_returnee = foo_code.setup_for_return(main_code)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=-np.pi),
            main_code.highlight_returnee,
            Uncreate(foo_frame),
            FadeOut(b1),
        )
        main_code.complete_returnee(hr_returnee, self)
        self.wait()

        self.play(
            main_code.highlight_lines, 4,
            main_frame.set_line, 4,
        )
        self.wait()

        t1 = TextMobject('And when main() returns\\\\the program ends').to_edge(LEFT)
        self.play(FadeIn(t1))
        self.wait()

        hr_returner, hr_returnee = main_code.setup_for_return(main_code)
        hr_returnee.shift(UP * 4)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=-np.pi),
            Uncreate(main_frame),
            FadeOut(t1),
        )
        self.remove(hr_returnee)
        self.wait()

        t1 = TextMobject("Alright, let's do a more complicated one!")
        self.play(
            FadeInFromDown(t1),
            FadeOutAndShift(g, RIGHT),
        )
        self.wait()


class FACHarderOne(Scene):
    def construct(self):
        title = TextMobject('The Call Stack').to_edge(UP)
        t1 = TextMobject("Alright, let's do a more complicated one!")
        self.add(title, t1)
        self.wait()

        code_scale = 0.75
        main_code = CodeBlock('Java', r"""
            public static
            void main(String[] args) {
                System.out.println(foo(1));
            }
            """).scale(code_scale)
        # Start line: 5
        foo_code = CodeBlock('Java', r"""
            foo(int a) {
                int b = bar(a, 2);
                int c = bar(a, b);
                return c;
            }
            """).scale(code_scale)
        # Start line: 10
        bar_code = CodeBlock('Java', r"""
            int bar(int x, int y) {
                int a = x + y;
                int b = a * 2;
                return b;
            }
            """).scale(code_scale)

        cg = VGroup(main_code, foo_code, bar_code)
        cg.arrange(DOWN, aligned_edge=LEFT, buff=MED_SMALL_BUFF)
        cg.next_to(title, DOWN, buff=MED_SMALL_BUFF).to_edge(RIGHT)
        self.play(
            FadeOut(t1),
            FadeInFrom(cg, RIGHT),
        )
        self.wait()

        frame_width = 3.0
        args_ref = TextMobject('[ ]').scale(0.5)
        main_frame = StackFrame('main()', 3, [('args', args_ref)], width=frame_width)
        main_frame.next_to(cg, LEFT, buff=LARGE_BUFF * 2).to_edge(DOWN)
        main_code.move_highlight_rect(3)
        self.play(
            FadeInFromDown(main_frame),
            main_code.highlight_lines, 3,
        )
        self.wait()

        foo_frame = StackFrame('foo(1)', 5, ['a', 'b', 'c'], width=frame_width)
        foo_frame.next_to(main_frame, UP, buff=SMALL_BUFF)
        hr_caller, hr_callee = main_code.setup_for_call(foo_code, 1)
        self.play(
            main_code.highlight_caller,
            ReplacementTransform(hr_caller, hr_callee, path_arc=np.pi),
            FadeInFrom(foo_frame, UP),
        )
        foo_code.complete_callee(hr_callee, self)
        self.wait()

        self.play(
            foo_code.highlight_lines, 2, foo_frame.set_line, 6,
            foo_frame.update_slot, 'a', 1,
        )
        self.wait()

        bar_frame = StackFrame('bar(1, 2)', 10, ['x', 'y', 'a', 'b'], width=frame_width)
        bar_frame.next_to(foo_frame, UP, buff=SMALL_BUFF)
        hr_caller, hr_callee = foo_code.setup_for_call(bar_code, 1)
        self.play(
            foo_code.highlight_caller,
            ReplacementTransform(hr_caller, hr_callee, path_arc=np.pi),
            FadeInFrom(bar_frame, UP),
        )
        bar_code.complete_callee(hr_callee, self)
        self.wait()

        self.play(
            bar_code.highlight_lines, 2, bar_frame.set_line, 11,
            bar_frame.update_slot, 'x', 1,
            bar_frame.update_slot, 'y', 2,
        )
        self.wait()

        self.play(
            bar_code.highlight_lines, 3, bar_frame.set_line, 12,
            bar_frame.update_slot, 'a', 3,
        )
        self.wait()

        self.play(
            bar_code.highlight_lines, 4, bar_frame.set_line, 13,
            bar_frame.update_slot, 'b', 6,
        )
        self.wait()

        hr_returner, hr_returnee = bar_code.setup_for_return(foo_code)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=-np.pi),
            foo_code.highlight_returnee,
            Uncreate(bar_frame),
        )
        foo_code.complete_returnee(hr_returnee, self)
        self.wait()

        self.play(
            foo_code.highlight_lines, 3, foo_frame.set_line, 7,
            foo_frame.update_slot, 'b', 6,
        )
        self.wait()

        bar_frame = StackFrame('bar(1, 6)', 10, ['x', 'y', 'a', 'b'], width=frame_width)
        bar_frame.next_to(foo_frame, UP, buff=SMALL_BUFF)
        hr_caller, hr_callee = foo_code.setup_for_call(bar_code, 1)
        self.play(
            foo_code.highlight_caller,
            ReplacementTransform(hr_caller, hr_callee, path_arc=np.pi),
            FadeInFrom(bar_frame, UP),
        )
        bar_code.complete_callee(hr_callee, self)
        self.wait()

        self.play(
            bar_code.highlight_lines, 2, bar_frame.set_line, 11,
            bar_frame.update_slot, 'x', 1,
            bar_frame.update_slot, 'y', 6,
        )
        self.wait()

        self.play(
            bar_code.highlight_lines, 3, bar_frame.set_line, 12,
            bar_frame.update_slot, 'a', 7,
        )
        self.wait()

        self.play(
            bar_code.highlight_lines, 4, bar_frame.set_line, 13,
            bar_frame.update_slot, 'b', 14,
        )
        self.wait()

        hr_returner, hr_returnee = bar_code.setup_for_return(foo_code)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=-np.pi),
            foo_code.highlight_returnee,
            Uncreate(bar_frame),
        )
        foo_code.complete_returnee(hr_returnee, self)
        self.wait()

        self.play(
            foo_code.highlight_lines, 4, foo_frame.set_line, 8,
            foo_frame.update_slot, 'c', 14,
        )
        self.wait()

        hr_returner, hr_returnee = foo_code.setup_for_return(main_code)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=-np.pi),
            main_code.highlight_returnee,
            Uncreate(foo_frame),
        )
        main_code.complete_returnee(hr_returnee, self)
        self.wait()

        def fake_frame(name):
            frame_name = TextMobject(name).scale(0.75)
            br = BackgroundRectangle(frame_name, buff=SMALL_BUFF, fill_opacity=0.15)
            br.set_fill(color=[ORANGE, BLUE])
            return VGroup(frame_name, br)

        println_funcs = [
            'BufferedWriter.write("14", 0, 2)',
            'BufferedWriter(Writer).write("14")',
            'PrintStream.writeln("14")',
            'PrintStream.println(14)',
        ]

        println_frames = [fake_frame(f) for f in reversed(println_funcs)]

        for n, p in zip(println_frames, [main_frame] + println_frames):
            n.next_to(p, UP, buff=SMALL_BUFF)
            self.play(FadeInFrom(n, UP))
        self.wait()

        for f in reversed(println_frames):
            self.play(Uncreate(f))
        # self.wait()

        self.play(
            main_code.highlight_lines, 4, main_frame.set_line, 4,
        )

        hr_returner, hr_returnee = main_code.setup_for_return(main_code)
        hr_returnee.shift(UP * 4)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=-np.pi),
            Uncreate(main_frame),
        )
        self.remove(hr_returnee)
        self.wait()

        self.play(FadeOut(main_code), FadeOut(foo_code), FadeOut(bar_code))
        self.wait


class FACClosing(Scene):
    def construct(self):
        title = TextMobject('The Call Stack').to_edge(UP)
        self.add(title)

        frame_width = 3.0
        args_ref = TextMobject('[ ]').scale(0.5)
        main_frame = StackFrame('main()', 3, [('args', args_ref)], width=frame_width)
        foo_frame = StackFrame('foo()', 6, [('n', 6)], width=frame_width)
        bar_frame = StackFrame('bar(1, 2)', 13,
                               [('x', 1), ('y', 2), ('a', 3), ('b', 6)], width=frame_width)
        main_frame.to_edge(DOWN)
        foo_frame.next_to(main_frame, UP)
        bar_frame.next_to(foo_frame, UP)
        self.play(
            LaggedStartMap(FadeInFrom, VGroup(main_frame, foo_frame, bar_frame),
                           direction=UP, lag_ratio=0.5)
        )
        self.wait()

        text_scale = 0.75
        b1 = BraceLabel(main_frame, 'Always starts\\\\with main()',
                        brace_direction=LEFT, label_constructor=TextMobject, label_scale=text_scale)
        # b2 = BraceLabel(foo_frame, ['Calls push frames,\\\\', 'returns pop'],
        #                 brace_direction=RIGHT, label_constructor=TextMobject,
        #                 alignment='')
        b3 = BraceLabel(bar_frame.slots()[0:2], 'Parameters',
                        brace_direction=RIGHT, label_constructor=TextMobject, label_scale=text_scale)
        b4 = BraceLabel(bar_frame.slots()[2:4], 'Locals',
                        brace_direction=RIGHT, label_constructor=TextMobject, label_scale=text_scale)
        b5 = BraceLabel(bar_frame.slots()[0:4], 'Storage for all\\\\variables in a function',
                        brace_direction=LEFT, label_constructor=TextMobject, label_scale=text_scale)

        push_up = TextMobject('Calls push frames').scale(text_scale)
        pua = Arrow(push_up.get_bottom(), push_up.get_top()).scale(2)
        pua.next_to(push_up, LEFT)
        pug = VGroup(push_up, pua)
        # pug.next_to(foo_frame, LEFT)
        pug.to_edge(LEFT).shift(DOWN)
        pop_down = TextMobject('Returns pop frames').scale(text_scale)
        pda = Arrow(pop_down.get_top(), pop_down.get_bottom()).scale(2)
        pda.next_to(pop_down, RIGHT)
        pdg = VGroup(pop_down, pda)
        # pdg.next_to(foo_frame, RIGHT)
        pdg.to_edge(RIGHT).shift(DOWN)

        notes = VGroup(b1, pug, pdg, b5, b3, b4)
        self.play(LaggedStartMap(ShowCreation, notes, lag_ratio=0.7), run_time=3)
        self.wait(duration=5)


class Misc(Scene):
    def construct(self):
        colors = color_gradient([BLUE, ORANGE], 8)
        little_boxes = VGroup(*[Rectangle(height=0.25, width=0.75, fill_opacity=1, color=colors[i])
                                for i in range(8)])
        little_boxes.arrange(UP, buff=0.1)
        little_boxes.center()

        self.play(
            LaggedStartMap(FadeInFrom, little_boxes, lambda m: (m, UP + LEFT*8),
                           lag_ratio=1.0, run_time=4.0, path_arc=-np.pi/4),
        )

        self.play(
            LaggedStartMap(FadeOutAndShift, VGroup(*reversed(little_boxes)),
                           lambda m: (m, UP + RIGHT*8),
                           lag_ratio=1.0, run_time=4.0, path_arc=-np.pi/8),
        )
