from manimlib.imports import *

from cs_education.csanim.code import CodeBlock, CodeTextString
from cs_education.csanim.stacks import StackFrame, CallStack


# Follow-on to Recursion 1
# Making x^n faster
# Explain /2 and log2
# Graphicial representation Helen suggested
# Need to show the transition between power1 and power2, show how power2 impls the new eq.
# End with the power of 2 and log2 growth, links to more reading on big-oh.

class Intro(Scene):
    def construct(self):
        title = TextMobject('Recursion: Part 2').scale(1.5).to_edge(UP)
        self.play(ShowCreation(title))
        self.wait(duration=0.5)

        t1 = TextMobject("\\textit{The joy of dividing things by 2}")
        self.play(ShowCreation(t1))
        self.wait(duration=2)

        self.play(FadeOut(title), FadeOut(t1))


class RevisitPower1(Scene):
    def construct(self):
        # mmmfixme: save space for a link to the Part 1 video.

        t1 = TextMobject("Let's look at our \\texttt{power(x,n)} function from Part 1 again")
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
        self.wait()

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
        hr = SurroundingRectangle(power1_code.code_string().get_line(5)[-5:-2])
        self.play(
            ReplacementTransform(t2, t3),
            FadeInFromDown(f1),
            FadeIn(hr),
        )
        self.wait(duration=3)

        t4 = TextMobject('Can we do better?')
        self.play(
            *[FadeOut(o) for o in self.mobjects],
            FadeIn(t4),
        )
        self.wait()

        self.play(FadeOut(t4))


class Equations(Scene):
    def construct(self):
        #mmmfixme: pacing

        t1 = TextMobject("Let's go back to our original equation").shift(UP)
        self.play(FadeInFromDown(t1))
        self.wait()

        # Even case
        ef1 = TexMobject('x^n=', 'x \\times ... \\times x', '\\times', 'x \\times ... \\times x')
        eb1n = BraceLabel(ef1[1:], '$n$ \\textit{times}',
                          brace_direction=UP, label_constructor=TextMobject)
        eb1l = BraceLabel(ef1[1:2], '$\\frac{n}{2}$ \\textit{times}',
                          brace_direction=UP, label_constructor=TextMobject)
        eb1r = BraceLabel(ef1[3:4], '$\\frac{n}{2}$ \\textit{times}',
                          brace_direction=UP, label_constructor=TextMobject)

        ef3 = TexMobject('x^n=', 'x^{\\frac{n}{2}}', '\\times', 'x', '^{\\frac{n}{2}}')
        ef3.next_to(ef1, ORIGIN, index_of_submobject_to_align=0)
        eb3l = BraceLabel(ef3[1:2], '$\\frac{n}{2}$ \\textit{times}',
                          brace_direction=UP, label_constructor=TextMobject)

        if_even = TextMobject('\\textit{if $n$ is even:}').next_to(ef1, LEFT).set_color(YELLOW)
        self.play(ShowCreation(ef1), ShowCreation(eb1n), t1.shift, UP)
        self.wait(duration=2)

        self.play(ReplacementTransform(eb1n, eb1l), ShowCreation(eb1r), FadeIn(if_even), FadeOut(t1))
        self.wait(duration=2)

        self.play(ReplacementTransform(ef1[1], ef3[1]), ReplacementTransform(eb1l, eb3l))
        self.wait()

        tmp_ef3_right = VGroup(ef3[2].copy(), ef3[3].copy(), ef3[4].copy())
        tmp_ef3_right.next_to(ef1[2], ORIGIN, submobject_to_align=tmp_ef3_right[0])
        eb3r = BraceLabel(tmp_ef3_right[1:], '$\\frac{n}{2}$ \\textit{times}',
                          brace_direction=UP, label_constructor=TextMobject)

        self.play(ReplacementTransform(ef1[3:], tmp_ef3_right[1:]), ReplacementTransform(eb1r, eb3r))
        self.wait()

        self.play(
            ReplacementTransform(ef1[2], ef3[2]),
            ReplacementTransform(tmp_ef3_right[1:], ef3[3:]),
            FadeOutAndShift(eb3r, LEFT),
            FadeOut(eb3l),
        )
        self.remove(ef1[0])
        self.add(ef3)
        self.wait()

        even_group = VGroup(if_even, ef3)
        self.play(even_group.to_edge, UL)
        self.wait()

        # Odd case
        ot1 = TextMobject("Now, let's figure out what to do if $n$ is odd")\
            .shift(UP * 2).set_color(BLUE)
        self.play(FadeInFromDown(ot1))

        of1 = TexMobject('x^n=', 'x \\times ... \\times x', '\\times', 'x \\times ... \\times x',
                         '\\times x')
        ob1n = BraceLabel(of1[1:], '$n$ \\textit{times}',
                          brace_direction=UP, label_constructor=TextMobject)
        ob1nm1 = BraceLabel(of1[1:-1], '$n-1$ \\textit{times}',
                          brace_direction=UP, label_constructor=TextMobject)
        ob1l = BraceLabel(of1[1:2], '$\\frac{n-1}{2}$ \\textit{times}',
                          brace_direction=UP, label_constructor=TextMobject)
        ob1r = BraceLabel(of1[3:4], '$\\frac{n-1}{2}$ \\textit{times}',
                          brace_direction=UP, label_constructor=TextMobject)

        of3 = TexMobject('x^n=',
                         'x', '^{\\frac{n-1}{2}}',
                         '\\times',
                         'x', '^{\\frac{n-1}{2}}',
                         '\\times x')
        of3.next_to(of1, ORIGIN, index_of_submobject_to_align=0)
        ob3l = BraceLabel(of3[1:3], '$\\frac{n-1}{2}$ \\textit{times}',
                          brace_direction=UP, label_constructor=TextMobject)

        if_odd = TextMobject('\\textit{if $n$ is odd:}').next_to(of1, LEFT).set_color(YELLOW)
        self.play(ShowCreation(of1), ShowCreation(ob1n))
        self.wait()

        self.play(ReplacementTransform(ob1n, ob1nm1), FadeIn(if_odd), FadeOut(ot1))
        self.wait(duration=2)

        self.play(ReplacementTransform(ob1nm1, ob1l), ShowCreation(ob1r))
        self.wait(duration=2)

        self.play(ReplacementTransform(of1[1], of3[1:3]), ReplacementTransform(ob1l, ob3l))
        self.wait()

        tmp_of3_right = VGroup(of3[3].copy(), of3[4].copy(), of3[5].copy())
        tmp_of3_right.next_to(of1[2], ORIGIN, submobject_to_align=tmp_of3_right[0])
        ob3r = BraceLabel(tmp_of3_right[1:], '$\\frac{n-1}{2}$ \\textit{times}',
                          brace_direction=UP, label_constructor=TextMobject)

        self.play(ReplacementTransform(of1[3], tmp_of3_right[1:]), ReplacementTransform(ob1r, ob3r))
        self.wait()

        self.play(
            ReplacementTransform(of1[2], of3[3]),
            ReplacementTransform(tmp_of3_right[1:], of3[4:6]),
            ReplacementTransform(of1[4], of3[-1]),
            FadeOutAndShift(ob3r, LEFT),
            FadeOut(ob3l),
        )
        self.remove(of1[0])
        self.add(of3)
        self.wait()

        # Both
        originals = [if_even, ef3, if_odd, of3]
        for o in originals:
            o.generate_target()
        ef3.target.next_to(of3, UP, aligned_edge=LEFT)
        if_even.target.next_to(ef3.target[0], LEFT)
        VGroup(*[o.target for o in originals]).center().to_edge(TOP)

        self.play(*[MoveToTarget(o) for o in originals])
        self.wait()
        eqg = VGroup(*originals)

        # Simplify with int division
        t1 = TextMobject(
            'Fun Fact: if $n$ is odd, and we use \\texttt{int} as the datatype, then',
            tex_to_color_map={'int': RED}
        ).next_to(eqg, DOWN, buff=LARGE_BUFF)
        div_code = CodeTextString('Java', '(n-1)/2 == n/2').next_to(t1, DOWN)

        self.play(FadeInFromDown(t1), FadeInFromDown(div_code))
        self.wait(duration=2)

        t2 = TextMobject(
            'Integer division \\textit{truncates}: '
            '\\texttt{5/2 == 2}'
            ', \\textit{not} '
            '\\texttt{2.5}')
        t2.next_to(div_code, DOWN, buff=LARGE_BUFF)
        self.play(FadeInFromDown(t2))
        self.wait(duration=2)

        # Indicate movement before each exp transformation from code
        of4 = TexMobject('x^n=',
                         'x', '^{\\frac{n}{2}}',
                         '\\times',
                         'x', '^{\\frac{n}{2}}',
                         '\\times x')
        of4.next_to(of3, ORIGIN, index_of_submobject_to_align=0)

        def highlight_and_switch_exp(target_exp, old_exp):
            hrc = SurroundingRectangle(div_code[0][:7])
            hrf = SurroundingRectangle(old_exp)
            self.play(ShowCreation(hrc), ShowCreation(hrf))
            self.wait()
            self.play(Uncreate(hrc), Uncreate(hrf))
            self.play(Indicate(div_code[0][-3:]))
            self.play(ReplacementTransform(div_code[0][-3:].copy(), target_exp),
                      FadeOut(old_exp))

        highlight_and_switch_exp(of4[2], of3[2])
        tmp_of4_right = VGroup(of4[4].copy(), of4[5].copy())
        tmp_of4_right.next_to(of3[4], ORIGIN, submobject_to_align=tmp_of4_right[0])
        highlight_and_switch_exp(tmp_of4_right[1], of3[5])
        self.wait()

        self.play(
            ReplacementTransform(of3[3:5], of4[3:5]),
            ReplacementTransform(tmp_of4_right[1], of4[5]),
            ReplacementTransform(of3[-1], of4[-1]),
        )
        self.remove(*of3)
        self.add(of4)
        self.wait()

        self.play(*[FadeOut(o) for o in [t1, t2, div_code]])

        originals = [if_even, ef3, if_odd, of4]
        for o in originals:
            o.generate_target()
        for p in [ef3.target[1:], of4.target[1:6]]:
            p.set_color(ORANGE)
        eqtg = VGroup(*[o.target for o in originals]).center().to_edge(TOP)

        t1 = TextMobject('Using \\texttt{int} for $n$ makes the equations very similar,\\\\'
                         'and the coding very simple!', tex_to_color_map={'int': RED})
        t1.next_to(eqtg, DOWN, buff=MED_LARGE_BUFF)
        self.play(*[MoveToTarget(o) for o in originals], FadeIn(t1))
        self.wait()
        eqg = VGroup(*originals)

        # Transform to code
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
                return t * t * x;
            }	
            """).scale(code_scale)
        power2_code.to_edge(RIGHT)

        ef3.generate_target()
        of4.generate_target()
        ef3.target.next_to(power2_code.code_string().get_line(7), LEFT, buff=LARGE_BUFF)
        of4.target.next_to(power2_code.code_string().get_line(9), LEFT, buff=LARGE_BUFF)
        ef3.target.next_to(of4.target, UP, index_of_submobject_to_align=0, coor_mask=X_AXIS)

        et = TextMobject('\\textit{even:}')
        ot = TextMobject('\\textit{odd:}')
        ot.next_to(of4.target[0], LEFT)
        et.next_to(ef3.target[0], LEFT)

        self.play(FadeOut(t1))
        self.play(
            FadeOut(if_even), FadeOut(if_odd),
            FadeInFrom(power2_code, RIGHT),
            MoveToTarget(ef3), MoveToTarget(of4),
            ReplacementTransform(if_even, et), ReplacementTransform(if_odd, ot),
        )
        self.wait()

        highlights = [
            [
                SurroundingRectangle(power2_code.code_string().get_line(1)[-6:-2]),
                SurroundingRectangle(power2_code.code_string().get_line(5)[-5:-2]),
                SurroundingRectangle(ef3[-1]),
            ],
            [
                SurroundingRectangle(power2_code.code_string().get_line(5)[5:-1]),
                SurroundingRectangle(ef3[-2:]),
            ],
            [
                SurroundingRectangle(power2_code.code_string().get_line(7)[-4:-1]),
                SurroundingRectangle(ef3[1:]),
            ],
            [
                SurroundingRectangle(power2_code.code_string().get_line(9)[-6:-1]),
                SurroundingRectangle(of4[1:]),
            ],
        ]

        for g in highlights:
            self.play(*[ShowCreation(h) for h in g])
            self.wait(duration=1.5)
            self.play(*[Uncreate(h) for h in g])
        self.wait()

        self.play(*[FadeOut(o) for o in self.mobjects if o != power2_code])
        power2_code.generate_target()
        power2_code.target.center()
        power2_code.target.to_edge(UP)
        self.play(MoveToTarget(power2_code))


class RunPower2(Scene):
    def construct(self):
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
                return t * t * x;
            }	
            """).scale(code_scale)
        power2_code.to_edge(UP)
        self.add(power2_code)

        t1 = TextMobject("This version should call itself fewer than $n$ times!")
        t1.next_to(power2_code, DOWN, buff=LARGE_BUFF)
        self.play(FadeInFromDown(t1))
        self.wait(duration=2)

        t2 = TextMobject('How many times do you think \\texttt{power2(2,30)} will call itself?',
                         tex_to_color_map={'30': YELLOW})
        t2.next_to(t1, ORIGIN)
        self.play(FadeOutAndShift(t1, UP), FadeInFromDown(t2))
        self.wait(duration=2)

        t3 = TextMobject("We know it'll be less than 30!  Maybe 15?")
        t3.next_to(t2, DOWN, buff=MED_LARGE_BUFF)
        self.play(FadeInFromDown(t3))
        self.wait(duration=2)

        t4 = TextMobject("How about a lot less?  Let's see...")
        t4.next_to(t3, ORIGIN)
        self.play(ReplacementTransform(t3, t4))
        self.wait(duration=2)

        self.play(*[FadeOut(o) for o in self.mobjects if o != power2_code])

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
            FadeInFromDown(main_frame),
            FadeInFromDown(main_code),
        )
        self.wait()

        def call_power2(x, n, call_stack, cc_num):
            new_cc_num = TextMobject(str(len(call_stack) - 1)).move_to(cc_num).set_color(YELLOW)
            update_cc_anims = [ReplacementTransform(cc_num, new_cc_num)]

            call_ret_delay = 0.5
            stack_frame = StackFrame(
                power2_code, 'power(%d, %d)' % (x, n), 1, ['x', 'n', 't'], width=frame_width)
            call_stack.animate_call(stack_frame, self, extra_anims=update_cc_anims)

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
                self.wait(duration=call_ret_delay)

                t = call_power2(x, int(n / 2), call_stack, new_cc_num)
                self.play(
                    *stack_frame.get_update_line_anims(6),
                    stack_frame.update_slot, 't', t,
                )

                if n % 2 == 0:
                    self.play(*stack_frame.get_update_line_anims(7))
                    self.wait(duration=call_ret_delay)
                    call_stack.animate_return(self)
                    return t * t

                self.play(*stack_frame.get_update_line_anims(9))
                self.wait(duration=call_ret_delay)
                call_stack.animate_return(self)
                return t * t * x

        cc_label = TextMobject('Recursive Calls').scale(0.75)
        cc_label.to_edge(UL).shift(DOWN)
        call_counter = TextMobject('0').set_color(YELLOW).next_to(cc_label, DOWN)
        self.play(FadeIn(call_counter), FadeIn(cc_label))

        result = call_power2(2, 30, CallStack(main_frame), call_counter)
        self.play(
            *main_frame.get_update_line_anims(3),
            main_frame.update_slot, 'y', result,
        )
        self.wait()

        t1 = TextMobject('We got our answer in just 5 recursive calls!').set_color(YELLOW)
        t1.next_to(power2_code, DOWN, buff=MED_LARGE_BUFF)
        self.play(ShowCreation(t1))
        self.wait(duration=2)

        t1.generate_target()
        t1.target.center().to_edge(TOP)
        t2 = TextMobject('But why?').next_to(t1.target, DOWN, buff=LARGE_BUFF)
        self.play(
            MoveToTarget(t1),
            FadeInFromDown(t2),
            *[FadeOut(o) for o in self.mobjects if o != t1],
        )


class Log2(Scene):
    def construct(self):
        #   - Show the number of recursive calls is log(n) instead of n.
        #     - Graph 'em real quick… should be easy with manim.
        t1 = TextMobject('We got our answer in just 5 recursive calls!').set_color(YELLOW)
        t1.to_edge(TOP)
        t2 = TextMobject('But why?').next_to(t1.target, DOWN, buff=LARGE_BUFF)
        self.add(t1, t2)

        self.wait()


# mmmfixme: some leftover code from previous iterations, likely all broken.
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


class EqsOld(Scene):
    def construct(self):
        # Even case
        ef0 = TexMobject('x^n=', 'x', '\\times', 'x \\times ... \\times x')
        eb0 = BraceLabel(ef0[1:], '$n$ \\textit{times}',
                         brace_direction=UP, label_constructor=TextMobject)
        ef0g = VGroup(ef0, eb0)

        ef1 = TexMobject('x^n=', 'x \\times ... \\times x', '\\times', 'x \\times ... \\times x')
        ef1.next_to(ef0, ORIGIN, index_of_submobject_to_align=0)
        eb1n = BraceLabel(ef1[1:], '$n$ \\textit{times}',
                          brace_direction=UP, label_constructor=TextMobject)
        eb1l = BraceLabel(ef1[1:2], '$\\frac{n}{2}$ \\textit{times}',
                          brace_direction=UP, label_constructor=TextMobject)
        eb1r = BraceLabel(ef1[3:4], '$\\frac{n}{2}$ \\textit{times}',
                          brace_direction=UP, label_constructor=TextMobject)

        ef2 = TexMobject('x^n=', 'x \\times ... \\times x', '\\times', 'x^{\\frac{n}{2}}')
        ef2.next_to(ef0, ORIGIN, index_of_submobject_to_align=0)
        eb2r = BraceLabel(ef2[3:4], '$\\frac{n}{2}$ \\textit{times}',
                          brace_direction=UP, label_constructor=TextMobject)

        ef3 = TexMobject('x^n=', 'x^{\\frac{n}{2}}', '\\times', 'x^{\\frac{n}{2}}')
        ef3.next_to(ef0, ORIGIN, index_of_submobject_to_align=0)
        eb3r = BraceLabel(ef3[3:4], '$\\frac{n}{2}$ \\textit{times}',
                          brace_direction=UP, label_constructor=TextMobject)

        if_even = TextMobject('\\textit{if $n$ is even:}').next_to(ef0, LEFT)
        self.play(ShowCreation(ef0g))
        self.wait()

        self.play(ReplacementTransform(ef0, ef1), ReplacementTransform(eb0, eb1n))
        self.wait()

        self.play(ReplacementTransform(eb1n, eb1l), ShowCreation(eb1r), FadeIn(if_even))
        self.wait(duration=2)

        self.play(ReplacementTransform(ef1, ef2), ReplacementTransform(eb1r, eb2r))
        self.wait()

        self.play(ReplacementTransform(ef2, ef3), FadeOut(eb1l), ReplacementTransform(eb2r, eb3r))
        self.wait()

        even_group = VGroup(if_even, ef3)
        self.play(FadeOutAndShift(eb3r, UL), even_group.to_edge, UL)
        self.wait()

        # Prime1 eq
        p1f = TexMobject('x^n=', 'x', '\\times', 'x^{n-1}')
        p1t = TextMobject('From our first version, we know')
        p1t.next_to(p1f, UP)
        self.play(FadeIn(p1t), ShowCreation(p1f))
        self.wait()

        # Odd case
        ot1 = TextMobject('So if $n$ is odd, then $n-1$ is even... hmm...')
        ot1.next_to(p1f, UP)
        self.play(ReplacementTransform(p1t, ot1))
        self.wait()

        of1 = TexMobject('x^n=', 'x', '\\times', 'x^{\\frac{n-1}{2}} \\times x^{\\frac{n-1}{2}}')
        of1.next_to(p1f, ORIGIN, index_of_submobject_to_align=0)

        self.play(ReplacementTransform(VGroup(ef3[1:]).copy(), of1[3]), FadeOut(p1f[3]))
        self.remove(*p1f[:3])
        self.add(of1)
        self.wait()

        if_odd = TextMobject('\\textit{if $n$ is odd:}').next_to(of1[0], LEFT)
        self.play(FadeOut(ot1), FadeIn(if_odd))
        self.wait()

        # Both
        originals = [if_even, ef3, if_odd, of1]
        for o in originals:
            o.generate_target()
        ef3.target.next_to(of1, UP, aligned_edge=LEFT)
        if_even.target.next_to(ef3.target[0], LEFT)
        VGroup(*[o.target for o in originals]).center().to_edge(TOP)

        self.play(*[MoveToTarget(o) for o in originals])
        self.wait()
        eqg = VGroup(*originals)

        # Simplify with int division
        t1 = TextMobject(
            'Fun Fact: if $n$ is odd, and we use \\texttt{int} as the datatype, then'
        ).next_to(eqg, DOWN, buff=LARGE_BUFF)
        div_code = CodeTextString('Java', 'n / 2 == (n - 1) / 2').next_to(t1, DOWN)

        self.play(FadeInFromDown(t1), FadeInFromDown(div_code))
        self.wait()

        of2 = TexMobject('x^n=', 'x', '\\times', 'x^{\\frac{n}{2}} \\times x^{\\frac{n}{2}}')
        of2.next_to(of1, ORIGIN, index_of_submobject_to_align=0)

        self.play(ReplacementTransform(div_code, of2[3]), FadeOut(of1[3]), FadeOut(t1))
        self.remove(*of1[:3])
        self.add(of2)
        self.wait()

        originals = [if_even, ef3, if_odd, of2]
        for o in originals:
            o.generate_target()
        for p in [ef3.target[1:], of2.target[3]]:
            p.set_color(ORANGE)
        eqtg = VGroup(*[o.target for o in originals]).center().to_edge(TOP)

        t1 = TextMobject('Using \\texttt{int} for $n$ makes the equations very similar,\\\\'
                         'and the coding very simple!')
        t1.next_to(eqtg, DOWN, buff=MED_LARGE_BUFF)
        self.play(*[MoveToTarget(o) for o in originals], FadeIn(t1))
        self.wait()
        eqg = VGroup(*originals)

        # Transform to code
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
                return t * t * x;
            }	
            """).scale(code_scale)
        power2_code.to_edge(RIGHT)

        ef3.generate_target()
        of2.generate_target()
        ef3.target.next_to(power2_code.code_string().get_line(7), LEFT, buff=LARGE_BUFF)
        of2.target.next_to(power2_code.code_string().get_line(9), LEFT, buff=LARGE_BUFF)
        ef3.target.next_to(of2.target, UP, aligned_edge=RIGHT, coor_mask=X_AXIS)

        et = TextMobject('\\textit{even:}')
        ot = TextMobject('\\textit{odd:}')
        ot.next_to(of2.target[0], LEFT)
        et.next_to(ef3.target[0], LEFT)

        self.play(FadeOut(t1))
        self.play(
            FadeOut(if_even), FadeOut(if_odd),
            FadeInFrom(power2_code, RIGHT),
            MoveToTarget(ef3), MoveToTarget(of2),
            ReplacementTransform(if_even, et), ReplacementTransform(if_odd, ot),
        )
        self.wait()

        recursive_call_hr = SurroundingRectangle(power2_code.code_string().get_line(5)[5:-1])
        xn2_hr = SurroundingRectangle(ef3[-1])

        ec_hr = SurroundingRectangle(power2_code.code_string().get_line(7)[-4:-1])
        ef_hr = SurroundingRectangle(ef3[1:])

        oc_hr = SurroundingRectangle(power2_code.code_string().get_line(9)[-6:-1])
        of_hr = SurroundingRectangle(of2[1:])

        for f, c in [(xn2_hr, recursive_call_hr), (ef_hr, ec_hr), (of_hr, oc_hr)]:
            self.play(ShowCreation(f), ShowCreation(c))
            self.wait()
            self.play(Uncreate(f), Uncreate(c))
        self.wait()

