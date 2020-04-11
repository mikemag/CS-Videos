from manimlib.imports import *

from cs_education.csanim.code import CodeBlock
from cs_education.csanim.stacks import StackFrame, CallStack


class Recursion1Intro(Scene):

    def construct(self):
        title = TextMobject('Recursion: Part 1').scale(1.5).to_edge(UP)
        self.play(ShowCreation(title))
        self.wait(duration=0.5)

        t1 = TextMobject(
            'Recursion is a fundamental part of CS,\\\\but it can be confusing to learn.'
        )
        t1.next_to(title, DOWN, buff=LARGE_BUFF)
        t2 = TextMobject("That's okay! It will get easier with practice.")
        t2.next_to(t1, DOWN, buff=LARGE_BUFF)
        self.play(FadeInFromDown(t1))
        self.wait()
        self.play(FadeInFromDown(t2))
        self.wait(duration=3)

        def animate_note_with_list(anchor, t, l, extra_anims):
            t.next_to(anchor, DOWN, buff=LARGE_BUFF)
            l.next_to(t, DOWN, buff=LARGE_BUFF)
            self.play(
                *extra_anims,
                FadeInFromDown(t),
            )
            self.wait()
            for part in l:
                self.play(FadeIn(part))
                self.wait(0.5)
            self.wait()

        t3 = TextMobject(
            'Many useful, important algorithms\\\\are easily written recursively'
        )
        l1 = TextMobject('Sorts', ', searches', ', mathematics', ', etc.')
        animate_note_with_list(title, t3, l1, [FadeOut(t1), FadeOut(t2)])

        t4 = TextMobject(
            'Lots of data is recursive,\\\\so using recursion on them is natural'
        )
        l2 = TextMobject('Lists', ', trees', ', file systems', ', HTML',
                         ', etc.')
        animate_note_with_list(title, t4, l2, [FadeOut(t3), FadeOut(l1)])

        t5 = TextMobject(
            "We'll take a look at two short\\\\recursive functions to get started"
        )
        t5.next_to(title, DOWN, buff=LARGE_BUFF)
        t6 = TextMobject(
            "Prereq: we'll look at call stacks as we run these functions.\\\\"
            "Check out the Call Stacks video if you need a quick review!"
        ).scale(0.75)
        t6.to_edge(BOTTOM)
        self.play(
            FadeOut(t4),
            FadeOut(l2),
            FadeInFromDown(t5),
            FadeInFromDown(t6),
        )
        self.wait(duration=3)

        self.play(*[FadeOut(o) for o in self.mobjects])
        self.wait()


class RecursiveCalls(Scene):

    def construct(self):
        code_scale = 0.75
        ss_code = CodeBlock(
            'Java', r"""
            public static double StrangeSqrt(double a) { 
                if (a < 0) { 
                    double b = StrangeSqrt(a * -1);
                    return b;
                } 
                return Math.sqrt(a);
            }
            """).scale(code_scale)

        t1 = TextMobject('Consider this somewhat strange square root function:')
        t1.next_to(ss_code, UP, buff=LARGE_BUFF)
        self.play(
            FadeIn(t1),
            ShowCreation(ss_code),
        )
        self.wait(duration=2.5)

        t2 = TextMobject(
            'It has a recursive call, meaning \\textit{it calls itself.}')
        t2.next_to(ss_code, DOWN, buff=LARGE_BUFF)
        # 012345 6 7 8901234567890 1 2345
        # double b = StrangeSqrt(a * -1);
        rl = ss_code.code_string().get_line(3)
        rc_highlight = SurroundingRectangle(rl[8:-1])
        self.play(
            FadeIn(t2),
            FadeIn(rc_highlight),
        )
        self.wait(duration=3)
        self.play(
            FadeOut(t2),
            FadeOut(rc_highlight),
        )

        # Run with a positive input
        main_code = CodeBlock(
            'Java', r"""
            public static void main(String[] args) {
                double n = StrangeSqrt(4);
            }
            """).scale(code_scale - 0.1)
        frame_width = 3.5
        main_frame = StackFrame(main_code,
                                'main()',
                                9, ['n'],
                                width=frame_width)
        main_code.highlight_lines(2)
        VGroup(main_code, main_frame).arrange(RIGHT,
                                              buff=LARGE_BUFF).to_edge(DOWN)
        t3 = TextMobject("Let's see what it does with a positive input...")\
            .next_to(ss_code, DOWN, buff=LARGE_BUFF)
        self.play(
            FadeOut(t1),
            MaintainPositionRelativeTo(t1, ss_code),
            ss_code.to_edge,
            UP,
            FadeIn(t3),
            MaintainPositionRelativeTo(t3, ss_code),
        )
        self.wait()
        self.play(
            FadeInFromDown(main_frame),
            FadeInFromDown(main_code),
        )
        self.wait()

        ss_frame = StackFrame(ss_code,
                              'StrangeSqrt(4)',
                              1, ['a', 'b'],
                              width=frame_width)
        ss_frame.next_to(main_frame, UP, buff=SMALL_BUFF)
        hr_caller, hr_callee = main_code.setup_for_call(ss_code, 1)
        self.play(
            main_code.highlight_caller,
            ReplacementTransform(hr_caller, hr_callee, path_arc=-np.pi),
            FadeInFrom(ss_frame, UP),
            FadeOut(t3),
        )
        ss_code.complete_callee(hr_callee, self)
        self.wait()

        self.play(
            ss_code.highlight_lines,
            2,
            ss_frame.set_line,
            2,
            ss_frame.update_slot,
            'a',
            4,
        )
        self.wait()

        self.play(
            ss_code.highlight_lines,
            6,
            ss_frame.set_line,
            6,
        )
        self.wait()

        hr_returner, hr_returnee = ss_code.setup_for_return(main_code)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=np.pi),
            main_code.highlight_returnee,
            Uncreate(ss_frame),
        )
        main_code.complete_returnee(hr_returnee, self)
        self.wait()

        t1 = TextMobject('That seems pretty normal...').next_to(ss_code,
                                                                DOWN,
                                                                buff=LARGE_BUFF)
        self.play(
            main_code.highlight_lines,
            3,
            main_frame.set_line,
            10,
            main_frame.update_slot,
            'n',
            2,
            FadeIn(t1),
        )
        self.wait(duration=2)

        t2 = TextMobject("Let's try it with a negative input...")\
            .next_to(ss_code, DOWN, buff=LARGE_BUFF)
        self.play(
            FadeOutAndShiftDown(main_code),
            FadeOutAndShiftDown(main_frame),
            FadeOut(t1),
            FadeIn(t2),
        )

        # Run with a negative input and see the recursion
        main_code = CodeBlock(
            'Java', r"""
            public static void main(String[] args) {
                double n = StrangeSqrt(-4);
            }
            """).scale(code_scale - 0.1)
        main_frame = StackFrame(main_code,
                                'main()',
                                9, ['n'],
                                width=frame_width)
        main_code.highlight_lines(2)
        VGroup(main_code, main_frame).arrange(RIGHT,
                                              buff=LARGE_BUFF).to_edge(DOWN)

        self.play(
            FadeInFromDown(main_frame),
            FadeInFromDown(main_code),
        )
        self.wait()

        ss_frame = StackFrame(ss_code,
                              'StrangeSqrt(-4)',
                              1, ['a', 'b'],
                              width=frame_width)
        ss_frame.next_to(main_frame, UP, buff=SMALL_BUFF)
        hr_caller, hr_callee = main_code.setup_for_call(ss_code, 1)
        self.play(
            main_code.highlight_caller,
            ReplacementTransform(hr_caller, hr_callee, path_arc=-np.pi),
            FadeInFrom(ss_frame, UP),
            FadeOut(t2),
        )
        ss_code.complete_callee(hr_callee, self)
        self.wait()

        self.play(
            ss_code.highlight_lines,
            2,
            ss_frame.set_line,
            2,
            ss_frame.update_slot,
            'a',
            -4,
        )
        self.wait()

        self.play(
            ss_code.highlight_lines,
            3,
            ss_frame.set_line,
            3,
        )
        self.wait()

        self.play(Indicate(rl[8:-1]),)

        ss2_frame = StackFrame(ss_code,
                               'StrangeSqrt(4)',
                               1, ['a', 'b'],
                               width=frame_width)
        ss2_frame.next_to(ss_frame, UP, buff=SMALL_BUFF)
        r1_call_site_rect = ss_code.highlight_rect().copy().set_color(WHITE)
        self.play(
            FadeInFrom(ss2_frame, UP),
            ss_code.highlight_lines,
            1,
            FadeIn(r1_call_site_rect),
        )
        self.wait()

        stack = VGroup(main_frame, ss_frame, ss2_frame)
        t1 = TextMobject('Same function, but with\\\\a new frame on the stack')\
            .next_to(stack, LEFT, buff=LARGE_BUFF).shift(UP * 0.5)
        a = Arrow(t1.get_right(), ss2_frame.get_left(), stroke_width=3)
        self.play(
            FadeIn(t1),
            GrowArrow(a),
        )
        self.wait(duration=2)

        # Now we have a positive input again
        self.play(
            ss_code.highlight_lines,
            2,
            ss2_frame.set_line,
            2,
            ss2_frame.update_slot,
            'a',
            4,
        )
        self.wait()

        self.play(
            ss_code.highlight_lines,
            6,
            ss2_frame.set_line,
            6,
            FadeOut(t1),
            FadeOut(a),
        )
        self.wait()

        t1 = TextMobject('The stack tells us where to return,\\\\and with which values')\
            .next_to(stack, LEFT, buff=LARGE_BUFF).shift(UP * 0.5)
        a = Arrow(t1.get_right(), ss_frame.get_left(), stroke_width=3)
        self.play(
            FadeIn(t1),
            GrowArrow(a),
        )
        self.wait(duration=2)

        # Return back to line 3...
        self.play(
            FadeOut(r1_call_site_rect),
            Uncreate(ss2_frame),
            ss_code.highlight_lines,
            3,
            ss_frame.set_line,
            3,
        )
        self.wait()

        self.play(
            ss_code.highlight_lines,
            4,
            ss_frame.set_line,
            4,
            ss_frame.update_slot,
            'b',
            2,
            FadeOut(t1),
            FadeOut(a),
        )
        self.wait()

        hr_returner, hr_returnee = ss_code.setup_for_return(main_code)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=np.pi),
            main_code.highlight_returnee,
            Uncreate(ss_frame),
        )
        main_code.complete_returnee(hr_returnee, self)
        self.wait()
        self.play(
            main_code.highlight_lines,
            3,
            main_frame.set_line,
            10,
            main_frame.update_slot,
            'n',
            2,
        )
        self.wait()

        t1 = TextMobject(
            'Thinking about the call stack can help you keep track of\\\\'
            'what a recursive function is doing at any given moment.').next_to(
                ss_code, DOWN, buff=LARGE_BUFF)
        self.play(
            FadeOutAndShiftDown(main_code),
            FadeOutAndShiftDown(main_frame),
            FadeIn(t1),
        )
        self.wait(duration=3)
        t2 = TextMobject('Try writing down part of the stack as you go.')\
            .next_to(t2, DOWN, buff=LARGE_BUFF)
        self.play(FadeInFromDown(t2))
        self.wait(duration=2)

        self.play(
            FadeOut(t1),
            FadeOut(t2),
        )
        self.wait()


class BrokenRecursiveCalls(Scene):

    def construct(self):
        # - Now, let's change this a bit and break it!
        # - Now modify it (a <= 0) and call it with foo(0).
        # - switch it out for the broken one, and highlight and note the change.
        code_scale = 0.75
        ss_good_code = CodeBlock(
            'Java', r"""
            public static double StrangeSqrt(double a) { 
                if (a < 0) { 
                    double b = StrangeSqrt(a * -1);
                    return b;
                } 
                return Math.sqrt(a);
            }
            """).scale(code_scale)
        ss_good_code.to_edge(UP)
        self.add(ss_good_code)

        t1 = TextMobject(
            "Let's break this code in a very small way and\\\\see what happens..."
        )
        t1.next_to(ss_good_code, DOWN, buff=LARGE_BUFF)
        self.play(FadeIn(t1))
        self.wait()

        gl2 = ss_good_code.code_string().get_line(2)
        ghr = SurroundingRectangle(gl2[3:6])
        self.play(ShowCreation(ghr))
        self.wait()

        ss_bad_code = CodeBlock(
            'Java', r"""
            public static double StrangeSqrt(double a) { 
                if (a <= 0) { 
                    double b = StrangeSqrt(a * -1);
                    return b;
                } 
                return Math.sqrt(a);
            }
            """).scale(code_scale)
        ss_bad_code.to_edge(UP)
        bl2 = ss_bad_code.code_string().get_line(2)
        bhr = SurroundingRectangle(bl2[3:7])
        self.play(
            ReplacementTransform(ss_good_code, ss_bad_code),
            ReplacementTransform(ghr, bhr),
        )
        self.wait()

        t2 = TextMobject(
            "This small change will have a big effect on one case: 0\\\\"
            "Let's run it and see.").next_to(ss_bad_code, DOWN, buff=LARGE_BUFF)
        self.play(
            FadeOut(t1),
            FadeIn(t2),
        )
        self.wait(duration=3)

        self.play(
            FadeOut(t2),
            FadeOut(bhr),
        )
        self.wait()

        # - Start stepping through this and see the stack start to grow forever.
        main_code = CodeBlock(
            'Java', r"""
            public static void main(String[] args) {
                double n = StrangeSqrt(0);
            }
            """).scale(code_scale - 0.1)
        frame_width = 3.5
        main_frame = StackFrame(main_code,
                                'main()',
                                9, ['n'],
                                width=frame_width)
        main_code.highlight_lines(2)
        VGroup(main_code, main_frame).arrange(RIGHT,
                                              buff=LARGE_BUFF).to_edge(DOWN)
        self.play(
            FadeInFromDown(main_frame),
            FadeInFromDown(main_code),
        )
        self.wait()

        ss_frame = StackFrame(ss_bad_code,
                              'StrangeSqrt(0)',
                              1, ['a', 'b'],
                              width=frame_width)
        ss_frame.next_to(main_frame, UP, buff=SMALL_BUFF)
        hr_caller, hr_callee = main_code.setup_for_call(ss_bad_code, 1)
        self.play(
            main_code.highlight_caller,
            ReplacementTransform(hr_caller, hr_callee, path_arc=-np.pi),
            FadeInFrom(ss_frame, UP),
        )
        ss_bad_code.complete_callee(hr_callee, self)
        self.wait()

        self.play(
            ss_bad_code.highlight_lines,
            2,
            ss_frame.set_line,
            2,
            ss_frame.update_slot,
            'a',
            0,
        )
        self.wait()

        self.play(
            ss_bad_code.highlight_lines,
            3,
            ss_frame.set_line,
            3,
        )
        self.wait()

        def call_ss_again(stack_group, previous_frame, extras=None):
            wait_each_step = len(stack_group) < 3
            runtime = 1.0 if len(stack_group) < 2 else 0.5 if len(
                stack_group) < 6 else 0.20
            extra_anims = []
            if len(stack_group) > 2:
                extra_anims.append(
                    ApplyMethod(
                        stack_group.shift,
                        DOWN * previous_frame.get_height() + DOWN * SMALL_BUFF))
            if extras:
                extra_anims.extend(extras)

            f = StackFrame(ss_bad_code,
                           'StrangeSqrt(0)',
                           1, ['a', 'b'],
                           width=frame_width)
            f.next_to(previous_frame, UP, buff=SMALL_BUFF)
            self.play(
                *extra_anims,
                ss_bad_code.highlight_lines,
                1,
                f.set_line,
                1,
                FadeIn(f),
                MaintainPositionRelativeTo(f, previous_frame),
                run_time=runtime,
            )
            if wait_each_step:
                self.wait()

            self.play(
                ss_bad_code.highlight_lines,
                2,
                f.set_line,
                2,
                f.update_slot,
                'a',
                0,
                run_time=runtime,
            )
            if wait_each_step:
                self.wait()

            self.play(
                ss_bad_code.highlight_lines,
                3,
                f.set_line,
                3,
                run_time=runtime,
            )
            if wait_each_step:
                self.wait()
            stack_group.add(f)
            return f

        sg = VGroup(main_frame, ss_frame)
        curr_ss_frame = ss_frame
        for i in range(3):
            curr_ss_frame = call_ss_again(sg, curr_ss_frame)

        # - When will this program end? Never?
        t1 = TextMobject("Hrm... when is this going to end??").next_to(
            main_code, UP, buff=LARGE_BUFF)
        extra_text = [FadeIn(t1)]
        for i in range(4):
            curr_ss_frame = call_ss_again(sg, curr_ss_frame, extra_text)
            extra_text = None

        t2 = TextMobject("Never?").next_to(main_code, UP, buff=LARGE_BUFF)
        extra_text = [FadeOut(t1), FadeIn(t2)]
        for i in range(4):
            curr_ss_frame = call_ss_again(sg, curr_ss_frame, extra_text)
            extra_text = None

        sg.save_state()
        t3 = TextMobject("The stack is getting quite deep!").next_to(
            main_code, UP, buff=LARGE_BUFF)
        self.play(
            sg.scale,
            0.20,
            {'about_edge': TOP},
            FadeOut(t2),
            FadeIn(t3),
        )
        self.wait(duration=2)
        self.play(sg.restore)

        extra_text = [FadeOut(t3)]
        for i in range(4):
            curr_ss_frame = call_ss_again(sg, curr_ss_frame, extra_text)
            extra_text = None

        # - Well, the stack is finite, so eventually you get a SO.
        #   Use the Java SO exception and show it hit and stop.
        so_frame = StackFrame(ss_bad_code,
                              'StrangeSqrt(0)',
                              1, ['a', 'b'],
                              width=frame_width)
        so_frame.slots().set_color(ORANGE)
        so_frame.header_line().set_color(ORANGE)
        so_frame.background_rect().set_fill(color=[BLACK, RED])
        so_frame.next_to(curr_ss_frame, UP, buff=SMALL_BUFF)
        so_exception = TextMobject(
            '\\texttt{Exception in thread "main"\\\\java.lang.StackOverflowError}',
        ).set_color(YELLOW).scale(0.75).next_to(main_code, UP, buff=LARGE_BUFF)
        self.play(
            sg.shift,
            DOWN * so_frame.get_height() + DOWN * SMALL_BUFF,
            ss_bad_code.highlight_rect().set_color,
            ORANGE,
            FadeIn(so_frame),
            MaintainPositionRelativeTo(so_frame, curr_ss_frame),
            Write(so_exception),
        )
        sg.add(so_frame)
        self.wait(duration=2)

        ss_bad_code.generate_target()
        so_exception.generate_target()
        ss_bad_code.target.scale(0.75)
        g = VGroup(so_exception.target,
                   ss_bad_code.target).arrange(RIGHT, buff=LARGE_BUFF)
        g.to_edge(UP)
        sg.generate_target()
        sg.target.scale(0.15).next_to(g, DOWN).to_edge(RIGHT)
        t1 = TextMobject(
            "Space for the call stack is limited,\\\\so we can't make recursive calls forever!"
        )
        self.play(
            *[MoveToTarget(t) for t in [so_exception, ss_bad_code, sg]],
            FadeOutAndShiftDown(main_code),
            FadeInFromDown(t1),
        )
        self.wait(duration=2)

        t2 = TextMobject(
            "This program made {\\raise.17ex\\hbox{$\\scriptstyle\\sim$}}15,000 calls before crashing."
        )
        t4 = TextMobject(
            "\\textit{Java SE 13.0.1 on macOS Catalina 10.15.4}").scale(0.5)
        t2.next_to(t1, DOWN, buff=MED_LARGE_BUFF)
        t4.to_edge(DL)
        self.play(
            FadeIn(t2),
            FadeInFromDown(t4),
        )
        self.wait(duration=4)

        t5 = TextMobject('\\textit{Most common mistake with recursion.}')
        t6 = TextMobject("You'll see this a lot. Everyone does!")
        t6.next_to(t5, DOWN, buff=LARGE_BUFF)
        self.play(
            *[FadeOut(t) for t in [t1, t2, t4]],
            *[FadeIn(t) for t in [t5, t6]],
        )
        self.wait(duration=3)

        # Transition
        t1 = TextMobject(
            "Alright, let's look at a more interesting function...")
        self.play(
            *[FadeOut(o) for o in self.mobjects],
            FadeIn(t1),
        )
        self.wait()

        self.play(FadeOut(t1))
        self.wait()


class Power1(Scene):

    def construct(self):
        t1 = TextMobject("Let's compute $x^n$").shift(UP)
        self.play(FadeIn(t1))
        self.wait()

        t2 = TextMobject("i.e., $2^4=16$, or $4^3=64$, etc.")
        t2.next_to(t1, DOWN, buff=LARGE_BUFF)
        self.play(FadeInFromDown(t2))
        self.wait(duration=2)

        t3 = TextMobject('Recall that')
        f1 = TexMobject('x^n=', 'x', '\\times', 'x \\times ... \\times x',
                        'x^{n-1}')
        f2 = TexMobject('x^n=', 'x', '\\times', 'x^{n-1}')
        f2.next_to(t3, RIGHT)
        dg = VGroup(t3, f2).center().shift(
            UP)  # Place t3 so the final result is centered
        f1.next_to(t3, RIGHT)
        b1 = BraceLabel(f1[1:-1],
                        '$n$ times',
                        brace_direction=UP,
                        label_constructor=TextMobject)
        g = VGroup(t3, f1[:-1], b1)  # For display
        self.play(
            FadeOut(t1),
            FadeOut(t2),
            FadeInFromDown(g),
        )
        self.wait(duration=3)

        b2 = BraceLabel(f1[3],
                        '$n-1$ times',
                        brace_direction=UP,
                        label_constructor=TextMobject)
        self.play(ReplacementTransform(b1, b2),)
        self.wait(duration=2)

        self.play(
            ReplacementTransform(f1[3], f2[3]),
            FadeOut(b2),
        )
        self.wait(duration=2)

        t4 = TextMobject("That's starting to feel a bit recursive!")
        t4.next_to(dg, DOWN, buff=MED_LARGE_BUFF)
        self.play(FadeIn(t4))
        self.wait()

        code_scale = 0.75
        power_code = CodeBlock(
            'Java', r"""
            public static int power(int x, int n) {
                if (n == 0) {
                    return 1;
                }
                int t = power(x, n - 1);
                return x * t;
            }
            """).scale(code_scale)
        self.play(
            *[FadeOut(o) for o in [t3, t4, f1[:-1], f2[3]]],
            FadeInFromDown(power_code),
        )
        self.wait()

        b1 = BraceLabel(
            power_code.code_string().get_lines(2, 4),
            'Remember $x^0=1$, because math!',
            brace_direction=RIGHT,
            label_constructor=TextMobject,
            label_scale=0.75,
        )
        self.play(ShowCreation(b1))
        self.wait(duration=2)

        t1 = TextMobject("Let's step through it to see how it goes...")
        t1.next_to(power_code, DOWN)
        self.play(FadeIn(t1),)
        self.wait()

        # Start stepping through this and see it go.
        main_code = CodeBlock('Java',
                              r"""
            public static void main(String[] args) {
                int y = power(4, 3);
            }
            """,
                              line_offset=7).scale(code_scale - 0.1)
        frame_width = 3.5
        main_frame = StackFrame(main_code,
                                'main()',
                                2, ['y'],
                                width=frame_width)
        main_code.highlight_lines(2)
        VGroup(main_code, main_frame).arrange(RIGHT,
                                              buff=LARGE_BUFF).to_edge(DOWN)
        self.play(
            FadeOut(t1),
            FadeOut(b1),
            power_code.to_edge,
            UP,
            FadeInFromDown(main_frame),
            FadeInFromDown(main_code),
        )
        self.wait()

        def call_power(x, n, call_stack):
            stack_frame = StackFrame(power_code,
                                     'power(%d, %d)' % (x, n),
                                     1, ['x', 'n', 't'],
                                     width=frame_width)
            call_stack.animate_call(stack_frame, self)

            self.play(
                *stack_frame.get_update_line_anims(2),
                stack_frame.update_slot,
                'x',
                x,
                stack_frame.update_slot,
                'n',
                n,
            )

            if n == 0:
                self.play(*stack_frame.get_update_line_anims(3))
                self.wait()
                call_stack.animate_return(self)
                return 1
            else:
                self.play(*stack_frame.get_update_line_anims(5))
                self.wait()
                t = call_power(x, n - 1, call_stack)

                self.play(
                    *stack_frame.get_update_line_anims(6),
                    stack_frame.update_slot,
                    't',
                    t,
                )
                self.wait()
                call_stack[-1].code = power_code
                call_stack.animate_return(self)
                return x * t

        result = call_power(4, 3, CallStack(main_frame))
        self.play(
            *main_frame.get_update_line_anims(3),
            main_frame.update_slot,
            'y',
            result,
        )
        self.wait()

        final_eq = TexMobject('4^3=', '64')
        final_eq.next_to(power_code, DOWN, buff=LARGE_BUFF)
        lhs = final_eq[0].copy().move_to(
            main_code.code_string().get_line(2)[12:15])
        rhs = final_eq[1].copy().move_to(main_frame.slots()[0])
        self.play(
            ReplacementTransform(lhs, final_eq[0]),
            ReplacementTransform(rhs, final_eq[1]),
        )
        self.wait(duration=2)

        self.play(*[FadeOut(o) for o in [final_eq, main_frame, main_code]])
        self.wait()


class Anatomy(Scene):

    def construct(self):
        # Look at power1() and highlight parts of it. Anatomy of a recursive function.
        # Always has two parts: base case and recursive step.
        code_scale = 0.75
        power_code = CodeBlock(
            'Java', r"""
            public static int power(int x, int n) {
                if (n == 0) {
                    return 1;
                }
                int t = power(x, n - 1);
                return x * t;
            }
            """).scale(code_scale)
        power_code.to_edge(UP)
        self.add(power_code)
        self.wait()

        title = TextMobject('Anatomy of a Recursive Function').to_edge(UP)
        power_code.generate_target()
        power_code.target.next_to(title, DOWN, buff=MED_LARGE_BUFF)
        self.play(
            FadeInFrom(title, UP),
            MoveToTarget(power_code),
        )
        self.wait()

        pc_groups = [
            VGroup(power_code.code_string().get_lines(s, e))
            for s, e in [(1, 1), (2, 4), (5, 6), (7, 7)]
        ]
        pc_t = [g.generate_target() for g in pc_groups]

        # Base Case
        #   - All of these have a base case that ends the recursion and returns.
        #   - Computed directly from the inputs.
        #   - Base cases are often some variant of emptiness. Power1() is a good example, with n == 0.
        #     What if you returned x for n == 1?
        base_shifts = [UP * 6, DOWN, DOWN * 6, DOWN * 6]
        power_code.save_state()
        for t, s in zip(pc_t, base_shifts):
            t.shift(s)

        t1 = TextMobject('Base Case').next_to(title, DOWN, buff=0.75)
        self.play(
            *[MoveToTarget(o) for o in pc_groups],
            FadeIn(t1),
        )
        self.wait()

        points_dwell_time = 2.5
        t2 = TextMobject(
            "- stops the recursion and returns\\\\",
            "- value is computed directly from the inputs, or constant\\\\",
            "- often it's some form of ``emptiness'' or ``singleness''\\\\",
            alignment="").next_to(title, DOWN, buff=LARGE_BUFF * 3.5)
        base_highlights = [
            SurroundingRectangle(pc_groups[1][0][1][0:6]),
            SurroundingRectangle(pc_groups[1][0][1][6:7]),
            SurroundingRectangle(pc_groups[1][0][0][3:7]),
        ]

        for t, h, ph in zip(t2, base_highlights, [None] + base_highlights):
            opt_anim = [FadeOut(ph)] if ph else []
            self.play(
                *opt_anim,
                FadeInFromDown(t),
                FadeIn(h),
            )
            self.wait(duration=points_dwell_time)
        self.play(FadeOut(base_highlights[-1]))
        self.wait()

        self.play(
            FadeOut(t1),
            FadeOut(t2),
            power_code.restore,
        )
        self.wait()

        # Recursive Step
        # The recursive step is some variant of decompose/reduce, call, recombine/compute.
        #   - Recursive case: compute the result with the help of one or more recursive calls to the same function.
        #     In this case, the data is reduced in some way in either size, complexity, or both.
        #   - In this case, reducing n by 1 each time.
        pc_t = [g.generate_target() for g in pc_groups]
        recurse_shifts = [UP * 6, UP * 6, UP * 0.45, DOWN * 6]
        power_code.save_state()
        for t, s in zip(pc_t, recurse_shifts):
            if s is not None:
                t.shift(s)

        t1 = TextMobject('Recursive Step').next_to(title, DOWN, buff=0.75)
        self.play(
            *[MoveToTarget(o) for o in pc_groups],
            FadeIn(t1),
        )
        self.wait()

        t2 = TextMobject(
            "- reduce: make the problem smaller, or break it into parts\\\\",
            "- call: one or more recursive calls\\\\",
            "- recombine: compute the result from the pieces\\\\",
            alignment="").next_to(title, DOWN, buff=LARGE_BUFF * 3.5)

        # 012345678901234567
        # intt=power(x,n-1);
        # returnx*t;
        recurse_highlights = [
            SurroundingRectangle(pc_groups[2][0][0][13:16]),
            SurroundingRectangle(pc_groups[2][0][0][5:17]),
            SurroundingRectangle(pc_groups[2][0][1][6:9]),
        ]

        for t, h, ph in zip(t2, recurse_highlights,
                            [None, *recurse_highlights]):
            opt_anim = [FadeOut(ph)] if ph else []
            self.play(
                *opt_anim,
                FadeInFromDown(t),
                FadeIn(h),
            )
            self.wait(duration=points_dwell_time)
        self.play(FadeOut(recurse_highlights[-1]))
        self.wait()

        self.play(
            FadeOut(t1),
            FadeOut(t2),
            power_code.restore,
        )
        self.wait(0.5)

        power_code.generate_target()
        power_code.target.to_edge(RIGHT)
        bcb = BraceLabel(power_code.target.code_string().get_lines(2, 4),
                         '\\textit{Base Case}',
                         brace_direction=LEFT,
                         label_constructor=TextMobject,
                         buff=LARGE_BUFF)
        rsb = BraceLabel(power_code.target.code_string().get_lines(5, 6),
                         '\\textit{Recursive Step}',
                         brace_direction=LEFT,
                         label_constructor=TextMobject,
                         buff=LARGE_BUFF)
        self.play(MoveToTarget(power_code),)
        self.play(
            ShowCreation(bcb),
            ShowCreation(rsb),
        )
        self.wait(0.5)

        t1 = TextMobject('Base Case', ':', ' stops the recursion')
        t2 = TextMobject('Recursive Step', ':', ' reduce - call - recombine')
        t2.next_to(t1.get_part_by_tex(':'),
                   DOWN,
                   submobject_to_align=t2.get_part_by_tex(':'),
                   buff=MED_LARGE_BUFF)
        g = VGroup(t1, t2).shift(DOWN * 1.5)
        self.play(FadeIn(g))
        self.wait(duration=points_dwell_time)

        t3 = TextMobject(
            "In Part 2 we'll look at making this function more efficient!"
        ).scale(0.75)
        t3.to_edge(DOWN).set_color(BLUE)
        self.play(Write(t3))

        # self.play(*[FadeOut(o) for o in self.mobjects])
        self.wait(duration=5)
