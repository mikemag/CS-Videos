from manimlib.imports import *

from csanim.code import CodeTextString, CodeBlock
from csanim.stacks import StackFrame
from end_scene import EndScene


class FACIntro(Scene):

    def construct(self):
        t1 = TextMobject('Call Stacks')
        t1.scale(1.5).to_edge(UP)
        self.play(ShowCreation(t1))
        self.wait(duration=0.5)

        # Background information on call stacks, foundation for other
        # concepts which build upon this.
        t2 = TextMobject(
            "Learning the basics of the ``call stack'' helps with\\\\many "
            'concepts in CS:',
            alignment='').shift(UP)
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
        main_code = CodeBlock(
            'Java',
            r"""
            public static
            void main(String[] args) {
                foo();
            }
            """,
            code_scale=code_scale,
        )
        foo_code = CodeBlock(
            'Java',
            r"""
            static int foo() {
                int n = bar(1, 2);
                return n;
            }
            """,
            code_scale=code_scale,
        )
        bar_code = CodeBlock(
            'Java',
            r"""
            static int bar(int x,
                           int y) {
                int a = x + y;
                int b = a * 2;
                return b;
            }
            """,
            code_scale=code_scale,
        )
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
                         "each variable as we go...")
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

        foo_code.move_hidden_highlight(2)
        self.play(FadeOut(t5), foo_code.highlight_lines, 2)
        self.wait()

        foo_n_q = TexMobject('?').move_to(foo_vars[0][1],
                                          aligned_edge=BOTTOM).shift(UP * 0.1)
        self.play(Write(foo_n_q))
        foo_vars.add(foo_n_q)
        self.wait()

        xi = foo_code.pre_call(bar_code, (1, 3))
        self.play(*foo_code.get_control_transfer_counterclockwise(xi),)
        bar_code.post_control_transfer(xi, self)
        self.wait()

        bar_x = TexMobject('1').move_to(bar_vars[0][1],
                                        aligned_edge=BOTTOM).shift(UP * 0.1)
        bar_y = TexMobject('2').move_to(bar_vars[1][1],
                                        aligned_edge=BOTTOM).shift(UP * 0.1)
        a = Arrow(bar_code.get_code().get_lines(2),
                  VGroup(bar_x, bar_y).get_right(),
                  stroke_width=3)
        self.play(Write(bar_x), Write(bar_y), ShowCreationThenDestruction(a))
        bar_vars_extras = VGroup()
        bar_vars_extras.add(bar_x, bar_y)
        self.play(bar_code.highlight_lines, 3)
        self.wait()

        bar_a = TexMobject('3').move_to(bar_vars[2][1],
                                        aligned_edge=BOTTOM).shift(UP * 0.1)
        a = Arrow(bar_code.get_code().get_lines(3),
                  bar_a.get_right(),
                  stroke_width=3)
        self.play(Write(bar_a), ShowCreationThenDestruction(a))
        bar_vars_extras.add(bar_a)
        self.play(bar_code.highlight_lines, 4)
        self.wait()

        bar_b = TexMobject('6').move_to(bar_vars[3][1],
                                        aligned_edge=BOTTOM).shift(UP * 0.1)
        a = Arrow(bar_code.get_code().get_lines(4),
                  bar_b.get_right(),
                  stroke_width=3)
        self.play(Write(bar_b), ShowCreationThenDestruction(a))
        bar_vars_extras.add(bar_b)
        self.play(bar_code.highlight_lines, 5)
        self.wait()

        xi = bar_code.pre_return(foo_code, 2)
        self.play(*bar_code.get_control_transfer_clockwise(xi),)
        foo_code.post_control_transfer(xi, self)
        self.wait()

        foo_n = TexMobject('6').move_to(foo_vars[0][1],
                                        aligned_edge=BOTTOM).shift(UP * 0.1)
        a = Arrow(foo_code.get_code().get_lines(2),
                  foo_n.get_right(),
                  stroke_width=3)
        self.play(
            foo_code.highlight_lines,
            3,
            ReplacementTransform(foo_n_q, foo_n),
            ShowCreationThenDestruction(a),
        )
        foo_vars.add(foo_n)
        self.wait()

        # - Now give the variables "homes" in each function. Variables like
        # homes; they're warm and safe and sized just for them!
        print('Give variables homes')

        t1 = TextMobject('So how does the\\\\computer do this?').to_edge(LEFT)
        self.play(FadeIn(t1), foo_code.remove_highlight)
        self.wait(duration=2)

        t2 = TextMobject(
            'Every variable is stored\\\\someplace in memory').to_edge(LEFT)
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
            slot_box = Rectangle(height=slot_height,
                                 width=slot_width,
                                 stroke_width=1)
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

        t4 = TextMobject(
            "All slots for a function\\\\are put together in a\\\\``frame''")
        t4.to_edge(LEFT)
        self.play(FadeOut(t3), FadeIn(t4))

        frame_width = 2.8
        foo_vars = [('n', '6')]
        foo_frame = StackFrame(foo_code,
                               'foo()',
                               3,
                               foo_vars,
                               width=frame_width)
        foo_frame.move_to(foo_homes, aligned_edge=LEFT).shift(LEFT * .5)
        self.play(ReplacementTransform(foo_homes, foo_frame))
        self.wait()

        bar_frame = StackFrame(bar_code,
                               'bar(1,2)',
                               9,
                               bar_var_vals,
                               width=frame_width)
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

        t7 = TextMobject("On the ``call stack''!").next_to(t6,
                                                           DOWN,
                                                           buff=LARGE_BUFF)
        self.play(FadeIn(t7))
        self.wait()

        new_title = TextMobject('The Call Stack').to_edge(UP)
        t1 = TextMobject('Function calls push a new frame\\\\onto the stack')\
            .to_edge(LEFT).shift(UP)
        t2 = TextMobject('Returning pops a frame off\\\\the stack').next_to(
            t1, DOWN, buff=LARGE_BUFF)

        box_count = 8
        colors = color_gradient([BLUE, ORANGE], box_count)
        little_boxes = VGroup(*[
            Rectangle(height=0.25, width=0.75, fill_opacity=1, color=colors[i])
            for i in range(box_count)
        ])
        little_boxes.arrange(UP, buff=0.1)
        little_boxes.next_to(VGroup(foo_code, bar_code), LEFT, buff=LARGE_BUFF)

        self.play(
            ReplacementTransform(title, new_title),
            FadeOut(t6),
            FadeOut(t7),
            FadeOut(foo_frame),
            FadeOut(bar_frame),
            FadeIn(t1),
            LaggedStartMap(FadeInFrom,
                           little_boxes,
                           lambda m: (m, UP),
                           lag_ratio=1.0,
                           run_time=4.0),
        )
        title = new_title
        self.wait()

        self.play(
            FadeIn(t2),
            LaggedStartMap(FadeOutAndShift,
                           VGroup(*reversed(little_boxes)),
                           lambda m: (m, UP),
                           lag_ratio=1.0,
                           run_time=4.0),
        )
        self.wait(duration=1)

        t3 = TextMobject(
            "Let's run again and see\\\\the call stack in action...").to_edge(
                LEFT)
        t3.shift(UP)
        self.play(FadeOut(t1), FadeOut(t2), FadeIn(t3))
        self.wait()

        print('Run with real call stack')

        # Let's also put main() into the picture. Start it off-frame upper right
        t4 = TextMobject("... and get main()\\\\into the picture.")\
            .next_to(t3, DOWN, buff=LARGE_BUFF)
        main_code.next_to(title, DOWN, buff=MED_SMALL_BUFF).to_edge(RIGHT)
        main_code.shift(UP * 3 + RIGHT * 3)
        g = VGroup(main_code, foo_code, bar_code)
        self.play(
            g.arrange,
            DOWN,
            {
                'aligned_edge': LEFT,
                'buff': MED_SMALL_BUFF
            },
            g.next_to,
            title,
            DOWN,
            {'buff': MED_SMALL_BUFF},
            g.to_edge,
            RIGHT,
            FadeInFromDown(t4),
        )
        self.wait(duration=2)

        t1 = TextMobject('Start in main()...')
        t1.next_to(title, DOWN, buff=LARGE_BUFF).to_edge(LEFT)
        frame_width = 3.0
        args_ref = TextMobject('[ ]').scale(0.5)
        main_frame = StackFrame(main_code,
                                'main()',
                                3, [('args', args_ref)],
                                width=frame_width)
        main_frame.next_to(g, LEFT, buff=LARGE_BUFF).to_edge(DOWN)
        main_code.move_hidden_highlight(3)
        self.play(FadeIn(t1), FadeInFromDown(main_frame),
                  main_code.highlight_lines, 3, FadeOut(t3), FadeOut(t4))
        self.wait()

        foo_frame = StackFrame(foo_code, 'foo()', 5, ['n'], width=frame_width)
        foo_frame.next_to(main_frame, UP, buff=SMALL_BUFF)
        b1 = BraceLabel(foo_frame,
                        'Calling foo()\\\\pushes a frame',
                        brace_direction=LEFT,
                        label_constructor=TextMobject)

        xi = main_code.pre_call(foo_code, 1)
        self.play(
            *main_code.get_control_transfer_counterclockwise(xi),
            FadeInFrom(foo_frame, UP),
            FadeInFrom(b1, UP),
            FadeOut(t1),
        )
        foo_code.post_control_transfer(xi, self)
        self.wait(duration=2)

        self.play(foo_code.highlight_lines, 2, foo_frame.set_line, 6,
                  FadeOut(b1))
        self.wait()

        bar_frame = StackFrame(bar_code,
                               'bar(1, 2)',
                               10, ['x', 'y', 'a', 'b'],
                               width=frame_width)
        bar_frame.next_to(foo_frame, UP, buff=SMALL_BUFF)
        b1 = BraceLabel(bar_frame,
                        'Calling bar()\\\\pushes a frame',
                        brace_direction=LEFT,
                        label_constructor=TextMobject)

        xi = foo_code.pre_call(bar_code, (1, 3))
        self.play(
            *foo_code.get_control_transfer_counterclockwise(xi),
            FadeInFrom(bar_frame, UP),
            FadeInFrom(b1, UP),
        )
        bar_code.post_control_transfer(xi, self)
        self.wait()

        self.play(bar_frame.update_slot, 'x', 1, bar_frame.update_slot, 'y', 2,
                  FadeOut(b1))
        self.play(bar_code.highlight_lines, 3, bar_frame.set_line, 11)
        self.wait()

        self.play(bar_frame.update_slot, 'a', 3)
        self.play(bar_code.highlight_lines, 4, bar_frame.set_line, 12)
        self.wait()

        self.play(bar_frame.update_slot, 'b', 6)
        self.play(bar_code.highlight_lines, 5, bar_frame.set_line, 13)
        b1 = BraceLabel(bar_frame,
                        "Returning pops\\\\bar's frame",
                        brace_direction=LEFT,
                        label_constructor=TextMobject)
        self.play(FadeIn(b1))
        self.wait(duration=2)

        xi = bar_code.pre_return(foo_code, 2)
        self.play(
            *bar_code.get_control_transfer_clockwise(xi),
            Uncreate(bar_frame),
            FadeOut(b1),
        )
        foo_code.post_control_transfer(xi, self)
        self.wait()

        self.play(foo_code.highlight_lines, 3, foo_frame.set_line, 7,
                  foo_frame.update_slot, 'n', 6)
        b1 = BraceLabel(foo_frame,
                        "Returning pops\\\\foo's frame",
                        brace_direction=LEFT,
                        label_constructor=TextMobject)
        self.play(FadeIn(b1))
        self.wait()

        xi = foo_code.pre_return(main_code, 3)
        self.play(
            *foo_code.get_control_transfer_clockwise(xi),
            Uncreate(foo_frame),
            FadeOut(b1),
        )
        main_code.post_control_transfer(xi, self)
        self.wait()

        self.play(main_code.highlight_lines, 4, main_frame.set_line, 4)
        self.wait()

        t1 = TextMobject('And when main() returns\\\\the program ends').to_edge(
            LEFT)
        self.play(FadeIn(t1))
        self.wait()

        off_screen_code = CodeBlock('Java', 'off_screen')
        off_screen_code.shift(UP * 8)  # Offscreen up
        self.add(off_screen_code)

        xi = main_code.pre_return(off_screen_code, 1)
        self.play(
            *main_code.get_control_transfer_clockwise(xi),
            Uncreate(main_frame),
            FadeOut(t1),
        )
        off_screen_code.post_control_transfer(xi, self)
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
        main_code = CodeBlock(
            'Java',
            r"""
            public static
            void main(String[] args) {
                System.out.println(foo(1));
            }
            """,
            code_scale=code_scale,
        )
        # Start line: 5
        foo_code = CodeBlock(
            'Java',
            r"""
            foo(int a) {
                int b = bar(a, 2);
                int c = bar(a, b);
                return c;
            }
            """,
            code_scale=code_scale,
        )
        # Start line: 10
        bar_code = CodeBlock(
            'Java',
            r"""
            int bar(int x, int y) {
                int a = x + y;
                int b = a * 2;
                return b;
            }
            """,
            code_scale=code_scale,
        )

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
        main_frame = StackFrame(main_code,
                                'main()',
                                3, [('args', args_ref)],
                                width=frame_width)
        main_frame.next_to(cg, LEFT, buff=LARGE_BUFF * 2).to_edge(DOWN)
        main_code.move_hidden_highlight(3)
        self.play(
            FadeInFromDown(main_frame),
            main_code.highlight_lines,
            3,
        )
        self.wait()

        foo_frame = StackFrame(foo_code,
                               'foo(1)',
                               5, ['a', 'b', 'c'],
                               width=frame_width)
        foo_frame.next_to(main_frame, UP, buff=SMALL_BUFF)

        xi = main_code.pre_call(foo_code, 1)
        self.play(
            *main_code.get_control_transfer_counterclockwise(xi),
            FadeInFrom(foo_frame, UP),
        )
        foo_code.post_control_transfer(xi, self)
        self.wait()

        self.play(foo_code.highlight_lines, 2, foo_frame.set_line, 6,
                  foo_frame.update_slot, 'a', 1)
        self.wait()

        bar_frame = StackFrame(bar_code,
                               'bar(1, 2)',
                               10, ['x', 'y', 'a', 'b'],
                               width=frame_width)
        bar_frame.next_to(foo_frame, UP, buff=SMALL_BUFF)

        xi = foo_code.pre_call(bar_code, 1)
        self.play(
            *foo_code.get_control_transfer_counterclockwise(xi),
            FadeInFrom(bar_frame, UP),
        )
        bar_code.post_control_transfer(xi, self)
        self.wait()

        self.play(bar_code.highlight_lines, 2, bar_frame.set_line, 11,
                  bar_frame.update_slot, 'x', 1, bar_frame.update_slot, 'y', 2)
        self.wait()

        self.play(bar_code.highlight_lines, 3, bar_frame.set_line, 12,
                  bar_frame.update_slot, 'a', 3)
        self.wait()

        self.play(bar_code.highlight_lines, 4, bar_frame.set_line, 13,
                  bar_frame.update_slot, 'b', 6)
        self.wait()

        xi = bar_code.pre_return(foo_code, 2)
        self.play(
            *bar_code.get_control_transfer_clockwise(xi),
            Uncreate(bar_frame),
        )
        foo_code.post_control_transfer(xi, self)
        self.wait()

        self.play(foo_code.highlight_lines, 3, foo_frame.set_line, 7,
                  foo_frame.update_slot, 'b', 6)
        self.wait()

        bar_frame = StackFrame(bar_code,
                               'bar(1, 6)',
                               10, ['x', 'y', 'a', 'b'],
                               width=frame_width)
        bar_frame.next_to(foo_frame, UP, buff=SMALL_BUFF)
        xi = foo_code.pre_call(bar_code, 1)
        self.play(
            *foo_code.get_control_transfer_counterclockwise(xi),
            FadeInFrom(bar_frame, UP),
        )
        bar_code.post_control_transfer(xi, self)
        self.wait()

        self.play(bar_code.highlight_lines, 2, bar_frame.set_line, 11,
                  bar_frame.update_slot, 'x', 1, bar_frame.update_slot, 'y', 6)
        self.wait()

        self.play(bar_code.highlight_lines, 3, bar_frame.set_line, 12,
                  bar_frame.update_slot, 'a', 7)
        self.wait()

        self.play(bar_code.highlight_lines, 4, bar_frame.set_line, 13,
                  bar_frame.update_slot, 'b', 14)
        self.wait()

        xi = bar_code.pre_return(foo_code, 3)
        self.play(
            *bar_code.get_control_transfer_clockwise(xi),
            Uncreate(bar_frame),
        )
        foo_code.post_control_transfer(xi, self)
        self.wait()

        self.play(foo_code.highlight_lines, 4, foo_frame.set_line, 8,
                  foo_frame.update_slot, 'c', 14)
        self.wait()

        xi = foo_code.pre_return(main_code, 3)
        self.play(
            *foo_code.get_control_transfer_clockwise(xi),
            Uncreate(foo_frame),
        )
        main_code.post_control_transfer(xi, self)
        self.wait()

        def fake_frame(name):
            frame_name = TextMobject(name).scale(0.75)
            br = BackgroundRectangle(frame_name,
                                     buff=SMALL_BUFF,
                                     fill_opacity=0.15)
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

        self.play(main_code.highlight_lines, 4, main_frame.set_line, 4)

        off_screen_code = CodeBlock('Java', 'off_screen')
        off_screen_code.shift(UP * 8)  # Offscreen up
        self.add(off_screen_code)

        xi = main_code.pre_return(off_screen_code, 1)
        self.play(
            *main_code.get_control_transfer_clockwise(xi),
            Uncreate(main_frame),
        )
        off_screen_code.post_control_transfer(xi, self)
        self.wait()

        self.play(FadeOut(main_code), FadeOut(foo_code), FadeOut(bar_code))
        self.wait()


class FACClosing(EndScene):

    def construct(self):
        title = TextMobject('The Call Stack').to_edge(UP)
        self.add(title)

        frame_width = 3.0
        dummy_code = CodeBlock('Java', 'foo')
        args_ref = TextMobject('[ ]').scale(0.5)
        main_frame = StackFrame(dummy_code,
                                'main()',
                                3, [('args', args_ref)],
                                width=frame_width)
        foo_frame = StackFrame(dummy_code,
                               'foo()',
                               6, [('n', 6)],
                               width=frame_width)
        bar_frame = StackFrame(dummy_code,
                               'bar(1, 2)',
                               13, [('x', 1), ('y', 2), ('a', 3), ('b', 6)],
                               width=frame_width)
        main_frame.to_edge(DOWN)
        foo_frame.next_to(main_frame, UP)
        bar_frame.next_to(foo_frame, UP)
        frame_group = VGroup(main_frame, foo_frame, bar_frame)
        self.play(
            LaggedStartMap(FadeInFrom,
                           frame_group,
                           group=frame_group,
                           direction=UP,
                           lag_ratio=0.5))
        self.wait()

        text_scale = 0.75
        b1 = BraceLabel(main_frame,
                        'Always starts\\\\with main()',
                        brace_direction=LEFT,
                        label_constructor=TextMobject,
                        label_scale=text_scale)
        # b2 = BraceLabel(foo_frame, ['Calls push frames,\\\\', 'returns pop'],
        #                 brace_direction=RIGHT, label_constructor=TextMobject,
        #                 alignment='')
        b3 = BraceLabel(bar_frame.slots()[0:2],
                        'Parameters',
                        brace_direction=RIGHT,
                        label_constructor=TextMobject,
                        label_scale=text_scale)
        b4 = BraceLabel(bar_frame.slots()[2:4],
                        'Locals',
                        brace_direction=RIGHT,
                        label_constructor=TextMobject,
                        label_scale=text_scale)
        b5 = BraceLabel(bar_frame.slots()[0:4],
                        'Storage for all\\\\variables in a function',
                        brace_direction=LEFT,
                        label_constructor=TextMobject,
                        label_scale=text_scale)

        notes = VGroup(b1, b5, b3, b4)

        box_count = 8
        colors = color_gradient([BLUE, ORANGE], box_count)
        little_boxes = VGroup(*[
            Rectangle(height=0.25, width=0.75, fill_opacity=1, color=colors[i])
            for i in range(box_count)
        ])
        little_boxes.arrange(UP, buff=0.1)

        push_up = TextMobject('Calls push\\\\frames').scale(text_scale)
        push_up.next_to(little_boxes, DOWN)
        pua = Arrow(push_up.get_bottom(), push_up.get_top()).scale(2)
        pua.next_to(push_up, LEFT)
        pug = VGroup(push_up, pua)

        pop_down = TextMobject('Returns pop\\\\frames').scale(text_scale)
        pop_down.next_to(little_boxes, UP)
        pda = Arrow(pop_down.get_top(), pop_down.get_bottom()).scale(2)
        pda.next_to(pop_down, RIGHT)
        pdg = VGroup(pop_down, pda)

        bg = VGroup(little_boxes, pug, pdg)
        bg.to_edge(RIGHT, buff=MED_LARGE_BUFF)

        self.play(
            LaggedStartMap(ShowCreation,
                           notes,
                           group=notes,
                           lag_ratio=0.7,
                           run_time=3.0))
        self.play(
            FadeIn(pug),
            LaggedStartMap(FadeInFrom,
                           little_boxes,
                           lambda m: (m, RIGHT),
                           lag_ratio=1.0,
                           run_time=3.0))
        self.play(FadeIn(pdg))
        pdg.generate_target()
        pdg.target.next_to(little_boxes[3], UP,
                           submobject_to_align=pdg[0]).set_opacity(1.0)
        self.play(
            MoveToTarget(pdg, run_time=3.0),
            LaggedStartMap(FadeOutAndShift,
                           VGroup(*list(reversed(little_boxes))[:4]),
                           lambda m: (m, RIGHT),
                           lag_ratio=1.0,
                           run_time=2.0),
        )
        self.wait(duration=5)

        end_scale_group = VGroup(*self.mobjects)
        end_fade_group = VGroup(title)
        self.animate_yt_end_screen(end_scale_group,
                                   end_fade_group,
                                   show_elements=False,
                                   show_rects=False)


class Misc(Scene):

    def construct(self):
        colors = color_gradient([BLUE, ORANGE], 8)
        little_boxes = VGroup(*[
            Rectangle(height=0.25, width=0.75, fill_opacity=1, color=colors[i])
            for i in range(8)
        ])
        little_boxes.arrange(UP, buff=0.1)
        little_boxes.center()

        self.play(
            LaggedStartMap(FadeInFrom,
                           little_boxes,
                           lambda m: (m, UP + LEFT * 8),
                           lag_ratio=1.0,
                           run_time=4.0,
                           path_arc=-np.pi / 4),)

        self.play(
            LaggedStartMap(FadeOutAndShift,
                           VGroup(*reversed(little_boxes)),
                           lambda m: (m, UP + RIGHT * 8),
                           lag_ratio=1.0,
                           run_time=4.0,
                           path_arc=-np.pi / 8),)


class CallStackReview(Scene):

    def construct(self):
        title = TextMobject('Quick Review: The Call Stack').to_edge(UP)

        code_scale = 0.75
        main_code = CodeBlock(
            'Java',
            r"""
            public static
            void main(String[] args) {
                int n = foo(2);
            }
            """,
            code_scale=code_scale,
        )
        foo_code = CodeBlock(
            'Java',
            r"""
            static int foo(int x) {
                int n = bar(x + 1, x * 2);
                return n;
            }
            """,
            code_scale=code_scale,
        )
        bar_code = CodeBlock(
            'Java',
            r"""
            static int bar(int x,
                           int y) {
                int a = x + y;
                return a;
            }
            """,
            code_scale=code_scale,
        )
        fbg = VGroup(main_code, foo_code, bar_code)
        fbg.arrange(DOWN, buff=MED_SMALL_BUFF, aligned_edge=LEFT)
        fbg.to_edge(DR)
        self.play(
            ShowCreation(title),
            FadeInFrom(fbg, RIGHT),
        )
        self.wait()

        frame_width = 3.0
        args_ref = TextMobject('[ ]').scale(0.5)
        main_frame = StackFrame(main_code,
                                'main()',
                                3, [('args', args_ref), 'n'],
                                width=frame_width)
        main_frame.next_to(fbg, LEFT, buff=LARGE_BUFF).to_edge(DOWN)
        main_code.move_highlight_rect(3)
        text_scale = 0.75
        b1 = BraceLabel(main_frame,
                        'The call stack\\\\starts with main()',
                        brace_direction=LEFT,
                        label_constructor=TextMobject,
                        label_scale=text_scale)
        self.play(
            FadeInFrom(main_frame, UP),
            main_code.highlight_lines,
            3,
            FadeInFrom(b1, UP),
        )
        self.wait()

        foo_frame = StackFrame(foo_code,
                               'foo(2)',
                               5, ['x', 'n'],
                               width=frame_width)
        foo_frame.next_to(main_frame, UP, buff=SMALL_BUFF)
        b2 = BraceLabel(foo_frame,
                        'Calls push frames',
                        brace_direction=LEFT,
                        label_constructor=TextMobject,
                        label_scale=text_scale)
        hr_caller, hr_callee = main_code.setup_for_call(foo_code, 1)
        self.play(
            main_code.highlight_caller,
            ReplacementTransform(hr_caller, hr_callee, path_arc=np.pi),
            FadeInFrom(foo_frame, UP),
            FadeInFrom(b2, UP),
        )
        foo_code.complete_callee(hr_callee, self)
        self.wait()

        self.play(
            foo_code.highlight_lines,
            2,
            foo_frame.set_line,
            6,
            foo_frame.update_slot,
            'x',
            2,
        )
        self.wait()

        bar_frame = StackFrame(bar_code,
                               'bar(3, 4)',
                               10, ['x', 'y', 'a'],
                               width=frame_width)
        bar_frame.next_to(foo_frame, UP, buff=SMALL_BUFF)
        b3 = BraceLabel(bar_frame,
                        'Holds arguments\\\\and locals',
                        brace_direction=LEFT,
                        label_constructor=TextMobject,
                        label_scale=text_scale)
        hr_caller, hr_callee = foo_code.setup_for_call(bar_code, (1, 2))
        self.play(
            foo_code.highlight_caller,
            ReplacementTransform(hr_caller, hr_callee, path_arc=np.pi),
            FadeInFrom(bar_frame, UP),
            FadeInFrom(b3, UP),
        )
        bar_code.complete_callee(hr_callee, self)
        self.wait()

        self.play(
            bar_code.highlight_lines,
            3,
            bar_frame.set_line,
            11,
            bar_frame.update_slot,
            'x',
            3,
            bar_frame.update_slot,
            'y',
            4,
        )
        self.wait()

        self.play(
            bar_code.highlight_lines,
            4,
            bar_frame.set_line,
            12,
            bar_frame.update_slot,
            'a',
            7,
        )
        self.wait(duration=3)

        hr_returner, hr_returnee = bar_code.setup_for_return(foo_code)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=-np.pi),
            foo_code.highlight_returnee,
            Uncreate(bar_frame),
            FadeOutAndShift(b3, LEFT),
            FadeOutAndShift(b2, LEFT),
            FadeOutAndShift(b1, LEFT),
        )
        foo_code.complete_returnee(hr_returnee, self)
        self.wait()

        b4 = BraceLabel(foo_frame,
                        'Returns pop',
                        brace_direction=LEFT,
                        label_constructor=TextMobject,
                        label_scale=text_scale)
        self.play(
            foo_code.highlight_lines,
            3,
            foo_frame.set_line,
            7,
            foo_frame.update_slot,
            'n',
            7,
            ShowCreation(b4),
        )
        self.wait()

        hr_returner, hr_returnee = foo_code.setup_for_return(main_code)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=-np.pi),
            main_code.highlight_returnee,
            Uncreate(foo_frame),
            FadeOutAndShift(b4, LEFT),
        )
        main_code.complete_returnee(hr_returnee, self)
        self.wait()

        self.play(
            main_code.highlight_lines,
            4,
            main_frame.set_line,
            4,
            main_frame.update_slot,
            'n',
            7,
        )
        self.wait()

        hr_returner, hr_returnee = main_code.setup_for_return(main_code)
        hr_returnee.shift(UP * 4)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=-np.pi),
            Uncreate(main_frame),
        )
        self.remove(hr_returnee)
        self.wait()

        t1 = TextMobject('Take a moment to think about\\\\'
                         'where args and locals live,\\\\'
                         'and  what the call stack looks like.').to_edge(LEFT)
        t2 = TextMobject('\\textit{It will help later!!}').next_to(
            t1, DOWN, buff=LARGE_BUFF)
        self.play(FadeIn(t1))
        self.wait()
        self.play(ShowCreation(t2))
        self.wait(duration=2)
