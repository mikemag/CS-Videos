from manimlib.imports import *

from cs_education.csanim.code import CodeBlock
from cs_education.csanim.stacks import StackFrame, CallStack


class Recursion1Intro(Scene):
    def construct(self):
        title = TextMobject('Recursion').scale(1.5).to_edge(TOP)
        subtitle = TextMobject('\\textit{An introduction}').next_to(title, DOWN)
        self.play(ShowCreation(title))
        self.play(FadeInFromDown(subtitle))
        self.wait()

        # Why?
        # Foundational part of CS
        # Lots of useful, important algorithms are most easily written recursively
        # Lots of data is recursive, and working on it with recursive algorithm is natural and easy
        # And it's on the AP exam!! :)


class FunctionCallsReview(Scene):
    def construct(self):
        # mmmfixme: needs pacing
        title = TextMobject('Quick Review: Function Calls').to_edge(UP)

        code_scale = 0.75
        main_code = CodeBlock('Java', r"""
            public static
            void main(String[] args) {
                int n = foo(2);
            }
            """).scale(code_scale)
        foo_code = CodeBlock('Java', r"""
            static int foo(int x) {
                int n = bar(x + 1, x * 2);
                return n;
            }
            """).scale(code_scale)
        bar_code = CodeBlock('Java', r"""
            static int bar(int x,
                           int y) {
                int a = x + y;
                return a;
            }
            """).scale(code_scale)
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
        main_frame = StackFrame(main_code, 'main()', 3, [('args', args_ref), 'n'], width=frame_width)
        main_frame.next_to(fbg, LEFT, buff=LARGE_BUFF).to_edge(DOWN)
        main_code.move_highlight_rect(3)
        text_scale = 0.75
        b1 = BraceLabel(main_frame, 'The call stack\\\\starts with main()',
                        brace_direction=LEFT, label_constructor=TextMobject, label_scale=text_scale)
        self.play(
            FadeInFrom(main_frame, UP),
            main_code.highlight_lines, 3,
            FadeInFrom(b1, UP),
        )
        self.wait()

        foo_frame = StackFrame(foo_code, 'foo(2)', 5, ['x', 'n'], width=frame_width)
        foo_frame.next_to(main_frame, UP, buff=SMALL_BUFF)
        b2 = BraceLabel(foo_frame, 'Calls push frames',
                        brace_direction=LEFT, label_constructor=TextMobject, label_scale=text_scale)
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
            foo_code.highlight_lines, 2, foo_frame.set_line, 6,
            foo_frame.update_slot, 'x', 2,
        )
        self.wait()

        bar_frame = StackFrame(bar_code, 'bar(3, 4)', 10, ['x', 'y', 'a'], width=frame_width)
        bar_frame.next_to(foo_frame, UP, buff=SMALL_BUFF)
        b3 = BraceLabel(bar_frame, 'Holds arguments\\\\and locals',
                        brace_direction=LEFT, label_constructor=TextMobject, label_scale=text_scale)
        hr_caller, hr_callee = foo_code.setup_for_call(bar_code, (1,2))
        self.play(
            foo_code.highlight_caller,
            ReplacementTransform(hr_caller, hr_callee, path_arc=np.pi),
            FadeInFrom(bar_frame, UP),
            FadeInFrom(b3, UP),
        )
        bar_code.complete_callee(hr_callee, self)
        self.wait()

        self.play(
            bar_code.highlight_lines, 3, bar_frame.set_line, 11,
            bar_frame.update_slot, 'x', 3,
            bar_frame.update_slot, 'y', 4,
        )
        self.wait()

        self.play(
            bar_code.highlight_lines, 4, bar_frame.set_line, 12,
            bar_frame.update_slot, 'a', 7,
        )
        self.wait()

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

        b4 = BraceLabel(foo_frame, 'Returns pop',
                        brace_direction=LEFT, label_constructor=TextMobject, label_scale=text_scale)
        self.play(
            foo_code.highlight_lines, 3, foo_frame.set_line, 7,
            foo_frame.update_slot, 'n', 7,
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
            main_code.highlight_lines, 4, main_frame.set_line, 4,
            main_frame.update_slot, 'n', 7,
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
        t2 = TextMobject('\\textit{It will help later!!}').next_to(t1, DOWN, buff=LARGE_BUFF)
        self.play(FadeIn(t1))
        self.wait()
        self.play(ShowCreation(t2))
        self.wait()

        # mmmfixme: transition to next scene


class RecursiveCalls(Scene):
    def construct(self):
        # mmmfixme: needs pacing
        code_scale = 0.75
        ss_code = CodeBlock('Java', r"""
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
        self.wait()

        t2 = TextMobject('It has a recursive call, meaning \\textit{it calls itself.}')
        t2.next_to(ss_code, DOWN, buff=LARGE_BUFF)
        # 012345 6 7 8901234567890 1 2345
        # double b = StrangeSqrt(a * -1);
        rl = ss_code.code_string().get_line(3)
        rc_highlight = SurroundingRectangle(rl[8:-1])
        self.play(
            FadeIn(t2),
            FadeIn(rc_highlight),
        )
        self.wait(duration=2)
        self.play(
            FadeOut(t2),
            FadeOut(rc_highlight),
        )

        # Run with a positive input
        main_code = CodeBlock('Java', r"""
            public static void main(String[] args) {
                double n = StrangeSqrt(4);
            }
            """).scale(code_scale - 0.1)
        frame_width = 3.5
        main_frame = StackFrame(main_code, 'main()', 9, ['n'], width=frame_width)
        main_code.highlight_lines(2)
        VGroup(main_code, main_frame).arrange(RIGHT, buff=LARGE_BUFF).to_edge(DOWN)
        t3 = TextMobject("Let's see what it does with a positive input...")\
            .next_to(ss_code, DOWN, buff=LARGE_BUFF)
        self.play(
            FadeOut(t1),
            MaintainPositionRelativeTo(t1, ss_code),
            ss_code.to_edge, UP,
            FadeIn(t3),
            MaintainPositionRelativeTo(t3, ss_code),
        )
        self.wait()
        self.play(
            FadeInFromDown(main_frame),
            FadeInFromDown(main_code),
        )
        self.wait()

        ss_frame = StackFrame(ss_code, 'StrangeSqrt(4)', 1, ['a', 'b'], width=frame_width)
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
            ss_code.highlight_lines, 2, ss_frame.set_line, 2,
            ss_frame.update_slot, 'a', 4,
        )
        self.wait()

        self.play(
            ss_code.highlight_lines, 6, ss_frame.set_line, 6,
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

        t1 = TextMobject('That seems pretty normal...').next_to(ss_code, DOWN, buff=LARGE_BUFF)
        self.play(
            main_code.highlight_lines, 3, main_frame.set_line, 10,
            main_frame.update_slot, 'n', 2,
            FadeIn(t1),
        )
        self.wait()

        t2 = TextMobject("Let's try it with a negative input...")\
            .next_to(ss_code, DOWN, buff=LARGE_BUFF)
        self.play(
            FadeOutAndShiftDown(main_code),
            FadeOutAndShiftDown(main_frame),
            FadeOut(t1),
            FadeIn(t2),
        )

        # Run with a negative input and see the recursion
        main_code = CodeBlock('Java', r"""
            public static void main(String[] args) {
                double n = StrangeSqrt(-4);
            }
            """).scale(code_scale - 0.1)
        main_frame = StackFrame(main_code, 'main()', 9, ['n'], width=frame_width)
        main_code.highlight_lines(2)
        VGroup(main_code, main_frame).arrange(RIGHT, buff=LARGE_BUFF).to_edge(DOWN)

        self.play(
            FadeInFromDown(main_frame),
            FadeInFromDown(main_code),
        )
        self.wait()

        ss_frame = StackFrame(ss_code, 'StrangeSqrt(-4)', 1, ['a', 'b'], width=frame_width)
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
            ss_code.highlight_lines, 2, ss_frame.set_line, 2,
            ss_frame.update_slot, 'a', -4,
        )
        self.wait()

        self.play(
            ss_code.highlight_lines, 3, ss_frame.set_line, 3,
        )
        self.wait()

        self.play(
            Indicate(rl[8:-1]),
        )

        ss2_frame = StackFrame(ss_code, 'StrangeSqrt(4)', 1, ['a', 'b'], width=frame_width)
        ss2_frame.next_to(ss_frame, UP, buff=SMALL_BUFF)
        r1_call_site_rect = ss_code.highlight_rect().copy().set_color(WHITE)
        self.play(
            FadeInFrom(ss2_frame, UP),
            ss_code.highlight_lines, 1,
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
        self.wait()

        # Now we have a positive input again
        self.play(
            ss_code.highlight_lines, 2, ss2_frame.set_line, 2,
            ss2_frame.update_slot, 'a', 4,
        )
        self.wait()

        self.play(
            ss_code.highlight_lines, 6, ss2_frame.set_line, 6,
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
        self.wait()

        # Return back to line 3...
        self.play(
            FadeOut(r1_call_site_rect),
            Uncreate(ss2_frame),
            ss_code.highlight_lines, 3, ss_frame.set_line, 3,
        )
        self.wait()

        self.play(
            ss_code.highlight_lines, 4, ss_frame.set_line, 4,
            ss_frame.update_slot, 'b', 2,
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
            main_code.highlight_lines, 3, main_frame.set_line, 10,
            main_frame.update_slot, 'n', 2,
        )
        self.wait()

        t1 = TextMobject(
            'Thinking about the call stack can help you keep track of\\\\'
            'what a recursive function is doing at any given moment.'
        ).next_to(ss_code, DOWN, buff=LARGE_BUFF)
        self.play(
            FadeOutAndShiftDown(main_code),
            FadeOutAndShiftDown(main_frame),
            FadeIn(t1),
        )
        self.wait()
        t2 = TextMobject('Try writing down part of the stack as you go.')\
            .next_to(t2, DOWN, buff=LARGE_BUFF)
        self.play(FadeInFromDown(t2))
        self.wait()

        self.play(
            FadeOut(t1),
            FadeOut(t2),
        )
        self.wait()


class BrokenRecursiveCalls(Scene):
    def construct(self):
        # mmmfixme: needs pacing

        # - Now, let's change this a bit and break it!
        # - Now modify it (a <= 0) and call it with foo(0).
        # - switch it out for the broken one, and highlight and note the change.
        code_scale = 0.75
        ss_good_code = CodeBlock('Java', r"""
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

        so_exception = TextMobject("Let's break this code in a very small way and\\\\see what happens...")
        so_exception.next_to(ss_good_code, DOWN, buff=LARGE_BUFF)
        self.play(FadeIn(so_exception))
        self.wait()

        gl2 = ss_good_code.code_string().get_line(2)
        ghr = SurroundingRectangle(gl2[3:6])
        self.play(ShowCreation(ghr))
        self.wait()

        ss_bad_code = CodeBlock('Java', r"""
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

        t2 = TextMobject("This small change will have a big effect on one case: 0\\\\"
                         "Let's run it and see.").next_to(ss_bad_code, DOWN, buff=LARGE_BUFF)
        self.play(
            FadeOut(so_exception),
            FadeIn(t2),
        )
        self.wait()

        self.play(
            FadeOut(t2),
            FadeOut(bhr),
        )
        self.wait()

        # - Start stepping through this and see the stack start to grow forever.
        main_code = CodeBlock('Java', r"""
            public static void main(String[] args) {
                double n = StrangeSqrt(0);
            }
            """).scale(code_scale - 0.1)
        frame_width = 3.5
        main_frame = StackFrame(main_code, 'main()', 9, ['n'], width=frame_width)
        main_code.highlight_lines(2)
        VGroup(main_code, main_frame).arrange(RIGHT, buff=LARGE_BUFF).to_edge(DOWN)
        self.play(
            FadeInFromDown(main_frame),
            FadeInFromDown(main_code),
        )
        self.wait()

        ss_frame = StackFrame(ss_bad_code, 'StrangeSqrt(0)', 1, ['a', 'b'], width=frame_width)
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
            ss_bad_code.highlight_lines, 2, ss_frame.set_line, 2,
            ss_frame.update_slot, 'a', 0,
        )
        self.wait()

        self.play(
            ss_bad_code.highlight_lines, 3, ss_frame.set_line, 3,
        )
        self.wait()

        def call_ss_again(stack_group, previous_frame, extras=None):
            wait_each_step = len(stack_group) < 3
            runtime = 1.0 if len(stack_group) < 2 else 0.5 if len(stack_group) < 6 else 0.20
            extra_anims = []
            if len(stack_group) > 2:
                extra_anims.append(ApplyMethod(
                    stack_group.shift,
                    DOWN * previous_frame.get_height() + DOWN * SMALL_BUFF
                ))
            if extras:
                extra_anims.extend(extras)

            f = StackFrame(ss_bad_code, 'StrangeSqrt(0)', 1, ['a', 'b'], width=frame_width)
            f.next_to(previous_frame, UP, buff=SMALL_BUFF)
            self.play(
                *extra_anims,
                ss_bad_code.highlight_lines, 1, f.set_line, 1,
                FadeIn(f),
                MaintainPositionRelativeTo(f, previous_frame),
                run_time=runtime,
            )
            if wait_each_step:
                self.wait()

            self.play(
                ss_bad_code.highlight_lines, 2, f.set_line, 2,
                f.update_slot, 'a', 0,
                run_time=runtime,
            )
            if wait_each_step:
                self.wait()

            self.play(
                ss_bad_code.highlight_lines, 3, f.set_line, 3,
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
        so_exception = TextMobject(
            "Hrm... when is this going to end??"
        ).next_to(main_code, UP, buff=LARGE_BUFF)
        extra_text = [FadeIn(so_exception)]
        for i in range(4):
            curr_ss_frame = call_ss_again(sg, curr_ss_frame, extra_text)
            extra_text = None

        t2 = TextMobject(
            "Never?"
        ).next_to(main_code, UP, buff=LARGE_BUFF)
        extra_text = [FadeOut(so_exception), FadeIn(t2)]
        for i in range(4):
            curr_ss_frame = call_ss_again(sg, curr_ss_frame, extra_text)
            extra_text = None

        sg.save_state()
        t3 = TextMobject(
            "The stack is getting quite deep!"
        ).next_to(main_code, UP, buff=LARGE_BUFF)
        self.play(
            sg.scale, 0.20, {'about_edge': TOP},
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
        so_frame = StackFrame(ss_bad_code, 'StrangeSqrt(0)', 1, ['a', 'b'], width=frame_width)
        so_frame.slots().set_color(ORANGE)
        so_frame.header_line().set_color(ORANGE)
        so_frame.background_rect().set_fill(color=[BLACK, RED])
        so_frame.next_to(curr_ss_frame, UP, buff=SMALL_BUFF)
        so_exception = TextMobject(
            '\\texttt{Exception in thread "main"\\\\java.lang.StackOverflowError}',
        ).set_color(YELLOW).scale(0.75).next_to(main_code, UP, buff=LARGE_BUFF)
        self.play(
            sg.shift, DOWN * so_frame.get_height() + DOWN * SMALL_BUFF,
            ss_bad_code.highlight_rect().set_color, ORANGE,
            FadeIn(so_frame),
            MaintainPositionRelativeTo(so_frame, curr_ss_frame),
            Write(so_exception),
        )
        sg.add(so_frame)
        self.wait()

        ss_bad_code.generate_target()
        so_exception.generate_target()
        ss_bad_code.target.scale(0.75)
        g = VGroup(so_exception.target, ss_bad_code.target).arrange(RIGHT, buff=LARGE_BUFF)
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
        self.wait()

        t2 = TextMobject(
            "This program made {\\raise.17ex\\hbox{$\\scriptstyle\\sim$}}15,000 calls before crashing.")
        t4 = TextMobject("\\textit{Java SE 13.0.1 on macOS Catalina 10.15.4}").scale(0.5)
        t2.next_to(t1, DOWN, buff=MED_LARGE_BUFF)
        t4.to_edge(DL)
        self.play(
            FadeIn(t2),
            FadeInFromDown(t4),
        )
        self.wait(duration=2)

        t5 = TextMobject('\\textit{Most common mistake with recursion.}')
        t6 = TextMobject("You'll see this a lot. Everyone does!")
        t6.next_to(t5, DOWN, buff=LARGE_BUFF)
        self.play(
            *[FadeOut(t) for t in [t1, t2, t4]],
            *[FadeIn(t) for t in [t5, t6]],
        )
        self.wait(duration=2)

        # Transition
        t1 = TextMobject("Alright, let's look at a more interesting function...")
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
        self.wait()

        t3 = TextMobject('Recall that')
        f1 = TexMobject('x^n=', 'x', '\\times', 'x \\times ... \\times x', 'x^{n-1}')
        f2 = TexMobject('x^n=', 'x', '\\times', 'x^{n-1}')
        f2.next_to(t3, RIGHT)
        dg = VGroup(t3, f2).center().shift(UP)  # Place t3 so the final result is centered
        f1.next_to(t3, RIGHT)
        b1 = BraceLabel(f1[1:-1], '$n$ times',
                        brace_direction=UP, label_constructor=TextMobject)
        g = VGroup(t3, f1[:-1], b1)  # For display
        self.play(
            t1.to_edge, UP,
            FadeOut(t2),
            FadeInFromDown(g),
        )
        self.wait()

        b2 = BraceLabel(f1[3], '$n-1$ times',
                        brace_direction=UP, label_constructor=TextMobject)
        self.play(
            ReplacementTransform(b1, b2),
        )
        self.wait()

        self.play(
            ReplacementTransform(f1[3], f2[3]),
            FadeOut(b2),
        )
        self.wait()

        t4 = TextMobject("That's starting to feel a bit recursive!")
        t4.next_to(dg, DOWN, buff=MED_LARGE_BUFF)
        self.play(FadeIn(t4))
        self.wait()

        code_scale = 0.75
        power_code = CodeBlock('Java', r"""
            public static int power(int x, int n) {
                if (n == 0) {
                    return 1;
                }
                int t = power(x, n - 1);
                return x * t;
            }
            """).scale(code_scale)
        self.play(
            *[FadeOut(o) for o in [t1, t3, t4, f1[:-1], f2[3]]],
            FadeInFromDown(power_code),
        )
        self.wait()

        b1 = BraceLabel(
            power_code.code_string().get_lines(2, 4),
            'Remember $x^0=1$, because math!',
            brace_direction=RIGHT, label_constructor=TextMobject, label_scale=0.75,
        )
        self.play(ShowCreation(b1))
        self.wait(duration=2)

        t1 = TextMobject("Let's step through it to see how it goes...")
        t1.next_to(power_code, DOWN)
        self.play(
            Uncreate(b1),
            FadeIn(t1),
        )
        self.wait();

        # Start stepping through this and see it go.
        main_code = CodeBlock('Java', r"""
            public static void main(String[] args) {
                int y = power(4, 3);
            }
            """, line_offset=7).scale(code_scale - 0.1)
        frame_width = 3.5
        main_frame = StackFrame(main_code, 'main()', 2, ['y'], width=frame_width)
        main_code.highlight_lines(2)
        VGroup(main_code, main_frame).arrange(RIGHT, buff=LARGE_BUFF).to_edge(DOWN)
        self.play(
            FadeOut(t1),
            power_code.to_edge, UP,
            FadeInFromDown(main_frame),
            FadeInFromDown(main_code),
        )
        self.wait()

        def call_power(x, n, call_stack):
            stack_frame = StackFrame(
                power_code, 'power(%d, %d)' % (x, n), 1, ['x', 'n', 't'], width=frame_width)
            call_stack.animate_call(stack_frame, self)

            self.play(
                stack_frame.get_update_line_anims(2),
                stack_frame.update_slot, 'x', x,
                stack_frame.update_slot, 'n', n,
            )

            if n == 0:
                self.play(
                    stack_frame.get_update_line_anims(3),
                )

                call_stack.animate_return(self)
                return 1
            else:
                self.play(
                    stack_frame.get_update_line_anims(5),
                )

                t = call_power(x, n - 1, call_stack)
                self.play(
                    stack_frame.get_update_line_anims(6),
                    stack_frame.update_slot, 't', t,
                )

                call_stack.animate_return(self)
                return x * t

        result = call_power(4, 3, CallStack(main_frame))
        self.play(
            main_frame.get_update_line_anims(3),
            main_frame.update_slot, 'y', result,
        )

        self.wait()






class Anatomy(Scene):
    def construct(self):
        # Look at power1() and highlight parts of it. Anatomy of a recursive function.
        # Always has two parts: base case and recursive step.
        # Base cases
        #   - All of these have a base case that ends the recursion and returns.
        #   - Computed directly from the inputs.
        #   - Base cases are often some variant of emptiness. Power1() is a good example, with n == 0.
        #     What if you returned x for n == 1?
        # The recursive step is some variant of decompose/reduce, call, recombine/compute.
        #   - Recursive case: compute the result with the help of one or more recursive calls to the same function.
        #     In this case, the data is reduced in some way in either size, complexity, or both.
        #   - In this case, reducing n by 1 each time.
        pass


class Power3(Scene):
    def construct(self):
        # Now look at power3()
        # Why make the change? Well, now it makes half the calls it would have made.
        # Who cares? Well, a couple of reasons:
        #   - It's faster if you do half the work.
        #   - Each call takes up room on the call stack, and it's finite, so this will work for larger inputs.
        #   - Show the number of recursive calls is log(n) instead of n.
        #     - Graph 'em real quick… should be easy with manim.
        pass


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
