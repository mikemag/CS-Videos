from manimlib.imports import *

from cs_education.csanim.code import CodeBlock
from cs_education.csanim.stacks import StackFrame


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
        main_frame = StackFrame('main()', 3, [('args', args_ref), 'n'], width=frame_width)
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

        foo_frame = StackFrame('foo(2)', 5, ['x', 'n'], width=frame_width)
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

        bar_frame = StackFrame('bar(3, 4)', 10, ['x', 'y', 'a'], width=frame_width)
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

        t2 = TextMobject('It has a recursive call, meaning it calls itself.')
        t2.next_to(ss_code, DOWN, buff=LARGE_BUFF)
        rl = ss_code.code_string().get_line(3)
        # 012345 6 7 8901234567890 1 2345
        # double b = StrangeSqrt(a * -1);
        rc_highlight = SurroundingRectangle(rl[8:-1])
        self.play(
            FadeIn(t2),
            FadeIn(rc_highlight),
        )
        self.wait(duration=2)

        # Run with a positive input
        main_code = CodeBlock('Java', r"""
            ...
            double n = StrangeSqrt(4);
            ...
            """).scale(code_scale)
        frame_width = 3.5
        main_frame = StackFrame('main()', 3, ['n'], width=frame_width)
        main_code.highlight_lines(2)
        VGroup(main_code, main_frame).arrange(RIGHT).to_edge(DOWN)
        t3 = TextMobject("Let's see what it does with a positive input...")\
            .next_to(ss_code, DOWN, buff=LARGE_BUFF)
        self.play(
            FadeOutAndShift(t1, UP),
            FadeOut(t2),
            MaintainPositionRelativeTo(t2, ss_code),
            FadeOut(rc_highlight),
            MaintainPositionRelativeTo(rc_highlight, ss_code),
            FadeIn(t3),
            MaintainPositionRelativeTo(t3, ss_code),
            ss_code.to_edge, UP,
            FadeInFromDown(main_frame),
            FadeInFromDown(main_code),
        )
        self.wait(duration=2)

        ss_frame = StackFrame('StrangeSqrt(4)', 1, ['a', 'b'], width=frame_width)
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
            main_frame.update_slot, 'n', 2,
        )
        main_code.complete_returnee(hr_returnee, self)
        self.wait()

        t1 = TextMobject('That seems pretty normal...').next_to(ss_code, DOWN, buff=LARGE_BUFF)
        self.play(
            main_code.fade_out_highlight,
            main_frame.set_line, 4,
            FadeIn(t1),
        )
        self.wait()

        self.play(
            FadeOutAndShiftDown(main_code),
            FadeOutAndShiftDown(main_frame),
            FadeOut(t1),
        )

        # mmmfixme: left off annotating the animation here.
        # - Run again with -4, pause and highlight when we're about to make the recursive call.
        # - Make call, stop and point out new frame for same function at a different line #.
        #   - Different place for variables too.
        # - Run it to the last line, stop and point out where we'll return to.
        # - Let it go from there I think... we'll see.

        # Run with a negative input and see the recursion
        main_code = CodeBlock('Java', r"""
            ...
            double n = StrangeSqrt(-4);
            ...
            """).scale(code_scale)
        main_frame = StackFrame('main()', 3, ['n'], width=frame_width)
        main_code.highlight_lines(2)
        VGroup(main_code, main_frame).arrange(RIGHT).to_edge(DOWN)

        self.play(
            FadeInFromDown(main_frame),
            FadeInFromDown(main_code),
        )
        self.wait()

        ss_frame = StackFrame('StrangeSqrt(-4)', 1, ['a', 'b'], width=frame_width)
        ss_frame.next_to(main_frame, UP, buff=SMALL_BUFF)
        hr_caller, hr_callee = main_code.setup_for_call(ss_code, 1)
        self.play(
            main_code.highlight_caller,
            ReplacementTransform(hr_caller, hr_callee, path_arc=-np.pi),
            FadeInFrom(ss_frame, UP),
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

        ss2_frame = StackFrame('StrangeSqrt(4)', 1, ['a', 'b'], width=frame_width)
        ss2_frame.next_to(ss_frame, UP, buff=SMALL_BUFF)
        r1_call_site_rect = ss_code.highlight_rect().copy().set_color(WHITE)
        self.play(
            FadeInFrom(ss2_frame, UP),
            ss_code.highlight_lines, 1,
            FadeIn(r1_call_site_rect),
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
        )
        self.wait()

        hr_returner, hr_returnee = ss_code.setup_for_return(main_code)
        self.play(
            ReplacementTransform(hr_returner, hr_returnee, path_arc=np.pi),
            main_code.highlight_returnee,
            Uncreate(ss_frame),
            main_frame.update_slot, 'n', 2,
        )
        main_code.complete_returnee(hr_returnee, self)
        self.wait()
        self.play(
            main_code.fade_out_highlight,
            main_frame.set_line, 4,
        )
        self.wait()

        self.play(
            FadeOutAndShiftDown(main_code),
            FadeOutAndShiftDown(main_frame),
        )
        self.wait()

        # mmmfixme:
        # - Now, let's change this a bit and break it!


class BrokenRecursiveCalls(Scene):
    def construct(self):
        # - Now modify it if (a <= 0) and call it with foo(0).
        # - Start stepping through this and see the stack start to grow forever.
        # - When will this program end? Never?
        # - Well, the stack is finite, so eventually you get a SO. Use the Java SO exception and show it hit and stop.
        #   - A run on my machine gave 1024 calls before SO. A surprisingly round number!!
        #   - Make a note of machine, JVM version, etc. as a footnote small at the bottom.
        # - This is the most common mistake in recursion: an incorrect or missing base case leads to infinite recursion
        #   and SO.
        # - Second most common mistake: failing to reduce the input on the recursive call.
        #   - Maybe these mistakes are better illustrated elsewhere?
        # - So, that works, but it's a silly recursive function that doesn't do anything useful. Let's do something
        #   interesting.
        pass


class Power1(Scene):
    def construct(self):
        # - Compute x^n recursively
        # - Show the real equation for this.
        #   - x + x + x + …, n times in total. You could do that with a for loop!
        #   - It's also x * x^(n-1) and x^0 is 1. This is a recursive definition: f(x, n) = x * f(x, n-1) for n > 0,
        #     1 otherwise.
        #   - Check my def and make sure it's reasonable.
        # - Start with power1() since it's so simple.
        # - Show it, run it for (2, 3) or so, show the result.
        pass


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


class Power2(Scene):
    def construct(self):
        # Now look at power2()
        # Why make the change? Well, now it makes half the calls it would have made.
        # Who cares? Well, a couple of reasons:
        #   - It's faster if you do half the work.
        #   - Each call takes up room on the call stack, and it's finite, so this will work for larger inputs.
        #   - Show the number of recursive calls is log(n) instead of n.
        #     - Graph 'em real quick… should be easy with manim.
        pass


class Power3(Scene):
    def construct(self):
        # Bother to do power3()?
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
