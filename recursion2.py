from manimlib.imports import *

from cs_education.csanim.code import CodeBlock
from cs_education.csanim.stacks import StackFrame, CallStack


class Recursion2Intro(Scene):
    def construct(self):
        title = TextMobject('Recursion: Part 2').scale(1.5).to_edge(UP)
        self.play(ShowCreation(title))
        self.wait(duration=0.5)


class Power2(Scene):
    def construct(self):
        t1 = TextMobject("Let's look at our \\texttt{power(x, n)} function again")
        t1.to_edge(UP)
        code_scale = 0.75
        power1_code = CodeBlock('Java', r"""
            public static int power(int x, int n) {
                if (n == 0) {
                    return 1;
                }
                int t = power(x, n - 1);
                return x * t;
            }
            """).scale(code_scale)
        power1_code.next_to(t1, DOWN, buff=MED_LARGE_BUFF)
        self.play(
            FadeIn(t1),
            FadeIn(power1_code),
        )

        t2 = TextMobject("How many times does it call itself?")
        t2.next_to(power1_code, DOWN, buff=MED_LARGE_BUFF)
        self.play(Write(t2))
        self.wait(duration=2)

        t3 = TextMobject("It call's itself $n$ times. Recall our original equation:")
        t3.move_to(t2)
        f1 = TexMobject('x^n=', 'x', '\\times', 'x \\times ... \\times x')
        f1.next_to(t3, DOWN)
        b1 = BraceLabel(f1[1:], '$n$ times',
                        brace_direction=DOWN, label_constructor=TextMobject)
        f1 = VGroup(f1, b1)
        self.play(
            ReplacementTransform(t2, t3),
            FadeInFromDown(f1),
        )
        self.wait()

        t4 = TextMobject('Can we do better?')
        self.play(
            *[FadeOut(o) for o in self.mobjects],
            FadeIn(t4),
        )
        self.wait()

        t4.generate_target()
        t4.target.to_edge(UP)
        t5 = TextMobject('Consider that $x^n=x^{n/2} \\times x^{n/2}$ if $n$ is even...')
        t6 = TextMobject(
            '...and $x^n=x \\times x^{\\lfloor n/2 \\rfloor} \\times '
            'x^{\\lfloor n/2 \\rfloor}$ if $n$ is odd.')
        t7 = TextMobject('Cutting things in half is a common recursive technique.')
        t5.next_to(t4.target, DOWN, buff=LARGE_BUFF * 1.5)
        t6.next_to(t5, DOWN, buff=MED_LARGE_BUFF)
        t7.next_to(t6, DOWN, buff=LARGE_BUFF)
        self.play(
            MoveToTarget(t4),
            FadeInFromDown(t5),
        )
        self.wait()
        self.play(FadeInFromDown(t6))
        self.wait()
        self.play(FadeInFromDown(t7))
        self.wait()

        t8 = TextMobject("That's gotta call itself fewer than n times, let's try it!")
        t8.next_to(t7, DOWN, buff=LARGE_BUFF)
        self.play(FadeInFromDown(t8))
        self.wait()

        code_scale = 0.7
        power2_code = CodeBlock('Java', r"""
            public static int power2(int x, int n) {
                if (n == 0) {
                    return 1;
                }
                int t = power2(x, n / 2);
                if (n % 2 == 0) {
                    return t * t;
                }
                return x * t * t;
            }	
            """).scale(code_scale)
        power2_code.to_edge(UP)

        self.play(
            *[FadeOut(o) for o in self.mobjects],
            FadeInFromDown(power2_code),
        )
        self.wait()

        # Start stepping through this and see it go.
        main_code = CodeBlock('Java', r"""
            public static void main(String[] args) {
                int y = power2(2, 30);
            }
            """, line_offset=10).scale(code_scale - 0.1)
        frame_width = 3.5
        main_frame = StackFrame(main_code, 'main()', 2, ['y'], width=frame_width, slot_char_width=8)
        main_code.highlight_lines(2)
        VGroup(main_code, main_frame).arrange(RIGHT, buff=LARGE_BUFF).to_edge(DOWN)
        self.play(
            power2_code.to_edge, UP,
            FadeInFromDown(main_frame),
            FadeInFromDown(main_code),
        )
        self.wait()

        def call_power2(x, n, call_stack):
            stack_frame = StackFrame(
                power2_code, 'power(%d, %d)' % (x, n), 1, ['x', 'n', 't'], width=frame_width)
            call_stack.animate_call(stack_frame, self)

            self.play(
                *stack_frame.get_update_line_anims(2),
                stack_frame.update_slot, 'x', x,
                stack_frame.update_slot, 'n', n,
            )

            if n == 0:
                self.play(*stack_frame.get_update_line_anims(3))
                call_stack.animate_return(self)
                return 1
            else:
                self.play(*stack_frame.get_update_line_anims(5))

                t = call_power2(x, int(n / 2), call_stack)
                self.play(
                    *stack_frame.get_update_line_anims(6),
                    stack_frame.update_slot, 't', t,
                )

                if n % 2 == 0:
                    self.play(*stack_frame.get_update_line_anims(7))
                    call_stack.animate_return(self)
                    return t * t

                self.play(*stack_frame.get_update_line_anims(9))
                call_stack.animate_return(self)
                return x * t * t

        t1 = TextMobject('How many times will \\texttt{power2(2, 30)} call itself?')
        t2 = TextMobject("We know it'll be less than 30! How about 15?")
        t3 = TextMobject("How about a lot less? Let's see...")
        mg = VGroup(main_code, main_frame)
        t1.next_to(mg, UP, buff=MED_LARGE_BUFF)
        t2.move_to(t1)
        t3.move_to(t2)
        self.play(ShowCreation(t1))
        self.wait()
        self.play(ReplacementTransform(t1, t2))
        self.wait()
        self.play(ReplacementTransform(t2, t3))
        self.wait()
        self.play(FadeOut(t3))

        result = call_power2(2, 30, CallStack(main_frame))
        self.play(
            *main_frame.get_update_line_anims(3),
            main_frame.update_slot, 'y', result,
        )
        self.wait()

        t1 = TextMobject('We got our answer in just 5 recursive calls!').set_color(YELLOW)
        t1.next_to(mg, UP, buff=MED_LARGE_BUFF)
        self.play(ShowCreation(t1))
        self.wait()

        #   - Show the number of recursive calls is log(n) instead of n.
        #     - Graph 'em real quick… should be easy with manim.


class Leftovers(Scene):
    def construct(self):
        t2 = TextMobject("Wait, just 5 recursive calls for $2^{30}$??")
        t2.to_edge(UP)
        self.play(
            *[FadeOut(o) for o in self.mobjects],
            FadeInFromDown(t2),
        )

        t3 = TextMobject("We're cutting $n$ in half with each recursive call...")
        t3.next_to(t2, DOWN, buff=LARGE_BUFF)
        self.play(FadeInFromDown(t3))
        t4 = TextMobject("and you can only cut 30 in half 5 times before you hit 0.")
        t4.next_to(t3, DOWN)
        self.play(FadeIn(t4))
        self.wait()

        f1 = TexMobject('30/2=15', '/2=7.5', '/2=3.75', '/2=1.875', '/2=0.9375')
        f1.next_to(t4, DOWN, buff=MED_LARGE_BUFF)
        for p in f1:
            self.play(Write(p))
            self.wait(duration=0.5)
        self.wait()

        t5 = TextMobject(
            "You can compute this directly with the base 2 logarithm:\\\\"
            "$\\log_2 30=%f$" % math.log2(30)
        )
        t5.next_to(f1, DOWN, buff=LARGE_BUFF)
        self.play(FadeIn(t5))
        self.wait()

        t6 = TextMobject(
            "That's the nice thing about dividing problems in half:\\\\"
            "the work done is proportional to $\\log_2 n$"
        )
        t6.next_to(t5, DOWN, buff=LARGE_BUFF)
        self.play(FadeInFromDown(t6))
        self.wait()


