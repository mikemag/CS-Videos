from manimlib.imports import *

from csanim.code import CodeBlock, CodeTextString
from csanim.stacks import StackFrame, CallStack
from end_scene import EndScene


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
        t1 = TextMobject(
            "Let's look at our \\texttt{power(x,n)} function from Part 1 again")
        t1.to_edge(UP)
        power1_code = CodeBlock(
            'Java', r"""
            public static int power(int x, int n) {
                if (n == 0) {
                    return 1;
                }
                int t = power(x, n - 1);
                return x * t;
            }
            """)
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

        t3 = TextMobject(
            "It call's itself $n$ times. Recall our original equation:")
        t3.move_to(t2)
        f1 = TexMobject('x^n=', 'x \\times x \\times ... \\times x',
                        '= x \\times x^{n-1}')
        f1.next_to(t3, DOWN)
        b1 = BraceLabel(f1[1],
                        '$n$ times',
                        brace_direction=DOWN,
                        label_constructor=TextMobject)
        f1 = VGroup(f1, b1)
        hr = SurroundingRectangle(power1_code.get_code().get_lines(5)[-5:-2])
        self.play(ReplacementTransform(t2, t3), FadeInFromDown(f1), FadeIn(hr))
        self.wait(duration=4)

        t4 = TextMobject('Can we do better?')
        self.play(*[FadeOut(o) for o in self.mobjects], FadeIn(t4))
        self.wait()

        self.play(FadeOut(t4))


class Equations(Scene):

    def construct(self):
        t1 = TextMobject("Let's go back to our original equation").shift(UP)
        self.play(FadeInFromDown(t1))
        self.wait()

        # Even case
        ef1 = TexMobject('x^n=', 'x \\times ... \\times x', '\\times',
                         'x \\times ... \\times x')
        eb1n = BraceLabel(ef1[1:],
                          '$n$ \\textit{times}',
                          brace_direction=UP,
                          label_constructor=TextMobject)
        eb1l = BraceLabel(ef1[1:2],
                          '$\\frac{n}{2}$ \\textit{times}',
                          brace_direction=UP,
                          label_constructor=TextMobject)
        eb1r = BraceLabel(ef1[3:4],
                          '$\\frac{n}{2}$ \\textit{times}',
                          brace_direction=UP,
                          label_constructor=TextMobject)

        ef3 = TexMobject('x^n=', 'x^{\\frac{n}{2}}', '\\times', 'x',
                         '^{\\frac{n}{2}}')
        ef3.next_to(ef1, ORIGIN, index_of_submobject_to_align=0)
        eb3l = BraceLabel(ef3[1:2],
                          '$\\frac{n}{2}$ \\textit{times}',
                          brace_direction=UP,
                          label_constructor=TextMobject)

        if_even = TextMobject('\\textit{if $n$ is even:}').next_to(
            ef1, LEFT).set_color(YELLOW)
        self.play(ShowCreation(ef1), ShowCreation(eb1n), t1.shift, UP)
        self.wait(duration=2)

        self.play(ReplacementTransform(eb1n, eb1l), ShowCreation(eb1r),
                  FadeIn(if_even), FadeOut(t1))
        self.wait(duration=2)

        self.play(ReplacementTransform(ef1[1], ef3[1]),
                  ReplacementTransform(eb1l, eb3l))
        self.wait()

        tmp_ef3_right = VGroup(ef3[2].copy(), ef3[3].copy(), ef3[4].copy())
        tmp_ef3_right.next_to(ef1[2],
                              ORIGIN,
                              submobject_to_align=tmp_ef3_right[0])
        eb3r = BraceLabel(tmp_ef3_right[1:],
                          '$\\frac{n}{2}$ \\textit{times}',
                          brace_direction=UP,
                          label_constructor=TextMobject)

        self.play(ReplacementTransform(ef1[3:], tmp_ef3_right[1:]),
                  ReplacementTransform(eb1r, eb3r))
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
        ot1 = TextMobject(
            "Now, let's figure out what to do if $n$ is odd").shift(
                UP * 2).set_color(BLUE)
        self.play(FadeInFromDown(ot1))

        of1 = TexMobject('x^n=', 'x \\times ... \\times x', '\\times',
                         'x \\times ... \\times x', '\\times x')
        ob1n = BraceLabel(of1[1:],
                          '$n$ \\textit{times}',
                          brace_direction=UP,
                          label_constructor=TextMobject)
        ob1nm1 = BraceLabel(of1[1:-1],
                            '$n-1$ \\textit{times}',
                            brace_direction=UP,
                            label_constructor=TextMobject)
        ob1l = BraceLabel(of1[1:2],
                          '$\\frac{n-1}{2}$ \\textit{times}',
                          brace_direction=UP,
                          label_constructor=TextMobject)
        ob1r = BraceLabel(of1[3:4],
                          '$\\frac{n-1}{2}$ \\textit{times}',
                          brace_direction=UP,
                          label_constructor=TextMobject)

        of3 = TexMobject('x^n=', 'x', '^{\\frac{n-1}{2}}', '\\times', 'x',
                         '^{\\frac{n-1}{2}}', '\\times x')
        of3.next_to(of1, ORIGIN, index_of_submobject_to_align=0)
        ob3l = BraceLabel(of3[1:3],
                          '$\\frac{n-1}{2}$ \\textit{times}',
                          brace_direction=UP,
                          label_constructor=TextMobject)

        if_odd = TextMobject('\\textit{if $n$ is odd:}').next_to(
            of1, LEFT).set_color(YELLOW)
        self.play(ShowCreation(of1), ShowCreation(ob1n))
        self.wait(duration=2)

        self.play(ReplacementTransform(ob1n, ob1nm1), FadeIn(if_odd),
                  FadeOut(ot1))
        self.wait(duration=2)

        self.play(ReplacementTransform(ob1nm1, ob1l), ShowCreation(ob1r))
        self.wait(duration=2)

        self.play(ReplacementTransform(of1[1], of3[1:3]),
                  ReplacementTransform(ob1l, ob3l))
        self.wait()

        tmp_of3_right = VGroup(of3[3].copy(), of3[4].copy(), of3[5].copy())
        tmp_of3_right.next_to(of1[2],
                              ORIGIN,
                              submobject_to_align=tmp_of3_right[0])
        ob3r = BraceLabel(tmp_of3_right[1:],
                          '$\\frac{n-1}{2}$ \\textit{times}',
                          brace_direction=UP,
                          label_constructor=TextMobject)

        self.play(ReplacementTransform(of1[3], tmp_of3_right[1:]),
                  ReplacementTransform(ob1r, ob3r))
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
            tex_to_color_map={
                'int': RED
            }).next_to(eqg, DOWN, buff=LARGE_BUFF)
        div_code = CodeTextString('Java', '(n-1)/2 == n/2').next_to(t1, DOWN)

        self.play(FadeInFromDown(t1), FadeInFromDown(div_code))
        self.wait(duration=3)

        t2 = TextMobject('Integer division \\textit{truncates}: '
                         '\\texttt{5/2 == 2}'
                         ', \\textit{not} '
                         '\\texttt{2.5}')
        t2.next_to(div_code, DOWN, buff=LARGE_BUFF)
        self.play(FadeInFromDown(t2))
        self.wait(duration=3)

        # Indicate movement before each exp transformation from code
        of4 = TexMobject('x^n=', 'x', '^{\\frac{n}{2}}', '\\times', 'x',
                         '^{\\frac{n}{2}}', '\\times x')
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
        tmp_of4_right.next_to(of3[4],
                              ORIGIN,
                              submobject_to_align=tmp_of4_right[0])
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

        t1 = TextMobject(
            'Using \\texttt{int} for $n$ makes the equations very similar,\\\\'
            'and the coding very simple!',
            tex_to_color_map={'int': RED})
        t1.next_to(eqtg, DOWN, buff=MED_LARGE_BUFF)
        self.play(*[MoveToTarget(o) for o in originals], FadeIn(t1))
        self.wait(duration=3)
        eqg = VGroup(*originals)

        # Transform to code
        code_scale = 0.7
        power2_code = CodeBlock(
            'Java',
            r"""
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
            """,
            code_scale=code_scale,
        )
        power2_code.to_edge(RIGHT)

        ef3.generate_target()
        of4.generate_target()
        ef3.target.next_to(power2_code.get_code().get_lines(7),
                           LEFT,
                           buff=LARGE_BUFF)
        of4.target.next_to(power2_code.get_code().get_lines(9),
                           LEFT,
                           buff=LARGE_BUFF)
        ef3.target.next_to(of4.target,
                           UP,
                           index_of_submobject_to_align=0,
                           coor_mask=X_AXIS)

        et = TextMobject('\\textit{even:}')
        ot = TextMobject('\\textit{odd:}')
        ot.next_to(of4.target[0], LEFT)
        et.next_to(ef3.target[0], LEFT)

        self.play(FadeOut(t1))
        self.play(
            FadeOut(if_even),
            FadeOut(if_odd),
            FadeInFrom(power2_code, RIGHT),
            MoveToTarget(ef3),
            MoveToTarget(of4),
            ReplacementTransform(if_even, et),
            ReplacementTransform(if_odd, ot),
        )
        self.wait()

        highlights = [
            [
                SurroundingRectangle(
                    power2_code.get_code().get_lines(1)[-6:-2]),
                SurroundingRectangle(
                    power2_code.get_code().get_lines(5)[-5:-2]),
                SurroundingRectangle(ef3[-1]),
            ],
            [
                SurroundingRectangle(power2_code.get_code().get_lines(5)[5:-1]),
                SurroundingRectangle(ef3[-2:]),
            ],
            [
                SurroundingRectangle(
                    power2_code.get_code().get_lines(7)[-4:-1]),
                SurroundingRectangle(ef3[1:]),
            ],
            [
                SurroundingRectangle(
                    power2_code.get_code().get_lines(9)[-6:-1]),
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
        power2_code = CodeBlock(
            'Java',
            r"""
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
            """,
            code_scale=code_scale,
        )
        power2_code.to_edge(UP)
        self.add(power2_code)

        t1 = TextMobject("This version should call itself fewer than $n$ times")
        t1.next_to(power2_code, DOWN, buff=LARGE_BUFF)
        self.play(FadeInFromDown(t1))
        self.wait(duration=2.5)

        t2 = TextMobject(
            'How many times do you think \\texttt{power2(2,30)} will call itself?',
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
        main_code = CodeBlock(
            'Java',
            r"""
            public static void main(String[] args) {
                int y = power2(2, 30);
            }
            """,
            line_offset=10,
            code_scale=code_scale - 0.1,
        )
        frame_width = 3.5
        main_frame = StackFrame(main_code,
                                'main()',
                                12, ['y'],
                                width=frame_width,
                                slot_char_width=8)
        main_code.highlight_lines(12)
        VGroup(main_code, main_frame).arrange(RIGHT,
                                              buff=LARGE_BUFF).to_edge(DOWN)
        self.play(
            FadeInFromDown(main_frame),
            FadeInFromDown(main_code),
        )
        self.wait()

        def call_power2(x, n, call_stack, cc_num):
            new_cc_num = TextMobject(str(len(call_stack) -
                                         1)).move_to(cc_num).set_color(YELLOW)
            update_cc_anims = [ReplacementTransform(cc_num, new_cc_num)]

            call_ret_delay = 0.5
            stack_frame = StackFrame(power2_code,
                                     'power(%d, %d)' % (x, n),
                                     1, ['x', 'n', 't'],
                                     width=frame_width)
            call_stack.animate_call(stack_frame,
                                    self,
                                    extra_anims=update_cc_anims)

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
                self.wait(duration=call_ret_delay)
                call_stack.animate_return(self)
                return 1
            else:
                self.play(*stack_frame.get_update_line_anims(5))
                self.wait(duration=call_ret_delay)

                t = call_power2(x, n // 2, call_stack, new_cc_num)
                self.play(
                    *stack_frame.get_update_line_anims(6),
                    stack_frame.update_slot,
                    't',
                    t,
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
        call_counter = TextMobject('0').set_color(YELLOW).next_to(
            cc_label, DOWN)
        self.play(FadeIn(call_counter), FadeIn(cc_label))

        result = call_power2(2, 30, CallStack(main_frame), call_counter)
        self.play(
            *main_frame.get_update_line_anims(13),
            main_frame.update_slot,
            'y',
            result,
        )
        self.wait()

        t1 = TextMobject(
            'We got our answer in just 5 recursive calls!').set_color(YELLOW)
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
        t1 = TextMobject(
            'We got our answer in just 5 recursive calls!').set_color(YELLOW)
        t1.to_edge(TOP)
        t2 = TextMobject('But why?').next_to(t1, DOWN, buff=LARGE_BUFF)
        self.add(t1, t2)
        self.wait()

        t3 = TextMobject(
            "We're cutting $n$ in half with \\underline{each} recursive call..."
        )
        t3.to_edge(TOP)
        self.play(FadeOut(t1), ReplacementTransform(t2, t3))
        self.wait(duration=2)

        t4 = TextMobject(
            "and you can only cut 30 in half 5 times before you hit 0.")
        t4.next_to(t3, DOWN)
        self.play(FadeIn(t4))
        self.wait()

        def get_div_by_2_nums(n):
            ns = [n]
            while n > 0:
                n //= 2
                ns.append(n)
            return ns

        def get_number_line(nums):
            us = (FRAME_WIDTH - LARGE_BUFF * 2) / (math.fabs(nums[0] -
                                                             nums[-1]))
            nts = nums.copy()
            if us < 0.2:
                nts.remove(1)

            nl = NumberLine(
                x_min=nums[-1],
                x_max=nums[0],
                include_numbers=True,
                unit_size=us,
                tick_size=0.01,
                longer_tick_multiple=0.15 / 0.01,
                numbers_to_show=nts,
                numbers_with_elongated_ticks=nums,
            )
            nl.center()
            return nl

        def animate_div_by_2(nums, nl, wait_time=0.5):
            dct = TextMobject('divisions: ', '0')
            dct.next_to(nl, DOWN, buff=MED_LARGE_BUFF)
            dc = TextMobject('0')
            dc.move_to(dct[-1])
            self.play(FadeInFromDown(dct[:-1]), FadeInFromDown(dc))
            self.wait(duration=wait_time)

            d = Dot(color=YELLOW)
            d.next_to(nl.n2p(nums[0]), UP)
            self.play(FadeInFrom(d, UP))
            self.wait(duration=wait_time)

            divs = 1
            for n in nums[1:]:
                d.generate_target()
                d.target.next_to(nl.n2p(n), UP)
                dc.generate_target()
                dc.target = TextMobject(str(divs)).move_to(dct[-1])
                divs += 1
                self.play(MoveToTarget(d, path_arc=np.pi / (n / 2 + 1)),
                          MoveToTarget(dc))
                self.wait(duration=wait_time / (1 if n > 6 else 2))

            self.play(FadeOut(dct[:-1]), FadeOut(dc), FadeOut(d))

        footnote = TextMobject(
            '\\textit{* Remember, this is integer division!}')
        footnote.scale(0.6).to_edge(DOWN)
        nums_30 = get_div_by_2_nums(30)
        nl1 = get_number_line(nums_30)
        nl1.next_to(t4, DOWN, buff=LARGE_BUFF)
        self.play(FadeIn(nl1), FadeInFromDown(footnote))
        animate_div_by_2(nums_30, nl1)
        self.play(FadeOut(nl1), FadeOutAndShiftDown(footnote))
        self.wait()

        t5 = TextMobject("What if we try $3^{100}$?").shift(UP)
        self.play(ReplacementTransform(t3, t5), FadeOut(t4))

        nums_100 = get_div_by_2_nums(100)
        nl2 = get_number_line(nums_100)
        nl2.next_to(t5, DOWN, buff=LARGE_BUFF)
        self.play(FadeIn(nl2))
        animate_div_by_2(nums_100, nl2, wait_time=0.3)
        self.play(FadeOut(nl2))

        t1 = TextMobject(
            'You can compute this directly with $\\log_2{n}$').to_edge(TOP)
        self.play(ReplacementTransform(t5, t1))

        t2 = TexMobject('\\log_2{30}', '=', '%.4f' % math.log2(30))
        t2a = TextMobject('5 times')
        t3 = TexMobject('\\log_2{100}', '=', '%.4f' % math.log2(100))
        t3a = TextMobject('7 times')
        t4 = TexMobject('\\log_2{1000}', '=', '%.4f' % math.log2(1000))
        t4a = TextMobject('10 times')
        t3.next_to(t2, DOWN, aligned_edge=LEFT)
        t4.next_to(t3, DOWN, aligned_edge=LEFT)
        t4a.next_to(t4, RIGHT, buff=LARGE_BUFF).next_to(t4[-1],
                                                        RIGHT,
                                                        coor_mask=Y_AXIS)
        t3a.next_to(t3[-1], RIGHT).next_to(t4a,
                                           UP,
                                           aligned_edge=RIGHT,
                                           coor_mask=X_AXIS)
        t2a.next_to(t2[-1], RIGHT).next_to(t3a,
                                           UP,
                                           aligned_edge=RIGHT,
                                           coor_mask=X_AXIS)
        g = VGroup(t2, t2a, t3, t3a, t4, t4a).center().next_to(t1,
                                                               DOWN,
                                                               buff=LARGE_BUFF)
        self.play(ShowCreation(t2), ShowCreation(t3))
        self.wait()
        self.play(FadeIn(t2a), FadeIn(t3a))
        self.wait(duration=3)

        self.play(*[FadeOut(o) for o in self.mobjects])


class Log2Graph(GraphScene, EndScene):
    CONFIG = {
        "x_axis_label":
            "$n$",
        "y_axis_label":
            "$time$",
        "x_axis_width":
            FRAME_HEIGHT,
        "y_axis_height":
            FRAME_HEIGHT / 2,
        "y_max":
            50,
        "y_min":
            0,
        "x_max":
            100,
        "x_min":
            0,
        "x_labeled_nums": [50, 100],
        "y_labeled_nums":
            range(0, 51, 10),
        "y_tick_frequency":
            10,
        "x_tick_frequency":
            10,
        "axes_color":
            BLUE,
        "graph_origin":
            np.array(
                (-FRAME_X_RADIUS + LARGE_BUFF, -FRAME_Y_RADIUS + LARGE_BUFF, 0))
    }

    def construct(self):
        t1 = TextMobject(
            "Dividing a problem in half over and over means\\\\"
            "the work done is proportional to $\\log_2{n}$").to_edge(UP)

        t2 = TextMobject(
            '\\textit{This is one of our\\\\favorite things to do in CS!}')
        t2.to_edge(RIGHT)

        t3 = TextMobject(
            'The new \\texttt{power(x,n)} is \\underline{much}\\\\better than the old!'
        )
        t3.scale(0.8)
        p1f = TexMobject('x^n=x \\times x^{n-1}').set_color(ORANGE)
        t4 = TextMobject('\\textit{vs.}').scale(0.8)
        p2f = TexMobject(
            'x^n=x^{\\frac{n}{2}} \\times x^{\\frac{n}{2}}').set_color(GREEN)
        p1v2g = VGroup(t3, p1f, t4, p2f).arrange(DOWN).center().to_edge(RIGHT)

        self.setup_axes()
        o_n = self.get_graph(lambda x: x, color=ORANGE, x_min=1, x_max=50)
        o_log2n = self.get_graph(lambda x: math.log2(x),
                                 color=GREEN,
                                 x_min=2,
                                 x_max=90)
        onl = TexMobject('O(n)')
        olog2nl = TexMobject('O(\\log_2{n})')
        onl.next_to(o_n.get_point_from_function(0.6), UL)
        olog2nl.next_to(o_log2n.get_point_from_function(0.8), UP)
        self.play(
            FadeIn(t1),
            FadeIn(self.axes),
            # FadeInFromDown(t2),
            FadeIn(p1v2g),
        )
        self.play(ShowCreation(o_n),
                  ShowCreation(o_log2n),
                  ShowCreation(onl),
                  ShowCreation(olog2nl),
                  run_time=3)
        self.wait(duration=5)

        end_scale_group = VGroup(*self.mobjects)
        end_fade_group = VGroup()
        self.animate_yt_end_screen(end_scale_group,
                                   end_fade_group,
                                   show_elements=False)


class EqsOld(Scene):

    def construct(self):
        # Even case
        ef0 = TexMobject('x^n=', 'x', '\\times', 'x \\times ... \\times x')
        eb0 = BraceLabel(ef0[1:],
                         '$n$ \\textit{times}',
                         brace_direction=UP,
                         label_constructor=TextMobject)
        ef0g = VGroup(ef0, eb0)

        ef1 = TexMobject('x^n=', 'x \\times ... \\times x', '\\times',
                         'x \\times ... \\times x')
        ef1.next_to(ef0, ORIGIN, index_of_submobject_to_align=0)
        eb1n = BraceLabel(ef1[1:],
                          '$n$ \\textit{times}',
                          brace_direction=UP,
                          label_constructor=TextMobject)
        eb1l = BraceLabel(ef1[1:2],
                          '$\\frac{n}{2}$ \\textit{times}',
                          brace_direction=UP,
                          label_constructor=TextMobject)
        eb1r = BraceLabel(ef1[3:4],
                          '$\\frac{n}{2}$ \\textit{times}',
                          brace_direction=UP,
                          label_constructor=TextMobject)

        ef2 = TexMobject('x^n=', 'x \\times ... \\times x', '\\times',
                         'x^{\\frac{n}{2}}')
        ef2.next_to(ef0, ORIGIN, index_of_submobject_to_align=0)
        eb2r = BraceLabel(ef2[3:4],
                          '$\\frac{n}{2}$ \\textit{times}',
                          brace_direction=UP,
                          label_constructor=TextMobject)

        ef3 = TexMobject('x^n=', 'x^{\\frac{n}{2}}', '\\times',
                         'x^{\\frac{n}{2}}')
        ef3.next_to(ef0, ORIGIN, index_of_submobject_to_align=0)
        eb3r = BraceLabel(ef3[3:4],
                          '$\\frac{n}{2}$ \\textit{times}',
                          brace_direction=UP,
                          label_constructor=TextMobject)

        if_even = TextMobject('\\textit{if $n$ is even:}').next_to(ef0, LEFT)
        self.play(ShowCreation(ef0g))
        self.wait()

        self.play(ReplacementTransform(ef0, ef1),
                  ReplacementTransform(eb0, eb1n))
        self.wait()

        self.play(ReplacementTransform(eb1n, eb1l), ShowCreation(eb1r),
                  FadeIn(if_even))
        self.wait(duration=2)

        self.play(ReplacementTransform(ef1, ef2),
                  ReplacementTransform(eb1r, eb2r))
        self.wait()

        self.play(ReplacementTransform(ef2, ef3), FadeOut(eb1l),
                  ReplacementTransform(eb2r, eb3r))
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

        of1 = TexMobject('x^n=', 'x', '\\times',
                         'x^{\\frac{n-1}{2}} \\times x^{\\frac{n-1}{2}}')
        of1.next_to(p1f, ORIGIN, index_of_submobject_to_align=0)

        self.play(ReplacementTransform(VGroup(ef3[1:]).copy(), of1[3]),
                  FadeOut(p1f[3]))
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
        div_code = CodeTextString('Java',
                                  'n / 2 == (n - 1) / 2').next_to(t1, DOWN)

        self.play(FadeInFromDown(t1), FadeInFromDown(div_code))
        self.wait()

        of2 = TexMobject('x^n=', 'x', '\\times',
                         'x^{\\frac{n}{2}} \\times x^{\\frac{n}{2}}')
        of2.next_to(of1, ORIGIN, index_of_submobject_to_align=0)

        self.play(ReplacementTransform(div_code, of2[3]), FadeOut(of1[3]),
                  FadeOut(t1))
        self.remove(*of1[:3])
        self.add(of2)
        self.wait()

        originals = [if_even, ef3, if_odd, of2]
        for o in originals:
            o.generate_target()
        for p in [ef3.target[1:], of2.target[3]]:
            p.set_color(ORANGE)
        eqtg = VGroup(*[o.target for o in originals]).center().to_edge(TOP)

        t1 = TextMobject(
            'Using \\texttt{int} for $n$ makes the equations very similar,\\\\'
            'and the coding very simple!')
        t1.next_to(eqtg, DOWN, buff=MED_LARGE_BUFF)
        self.play(*[MoveToTarget(o) for o in originals], FadeIn(t1))
        self.wait()
        eqg = VGroup(*originals)

        # Transform to code
        code_scale = 0.7
        power2_code = CodeBlock(
            'Java',
            r"""
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
            """,
            code_scale=code_scale,
        )
        power2_code.to_edge(RIGHT)

        ef3.generate_target()
        of2.generate_target()
        ef3.target.next_to(power2_code.get_code().get_lines(7),
                           LEFT,
                           buff=LARGE_BUFF)
        of2.target.next_to(power2_code.get_code().get_lines(9),
                           LEFT,
                           buff=LARGE_BUFF)
        ef3.target.next_to(of2.target, UP, aligned_edge=RIGHT, coor_mask=X_AXIS)

        et = TextMobject('\\textit{even:}')
        ot = TextMobject('\\textit{odd:}')
        ot.next_to(of2.target[0], LEFT)
        et.next_to(ef3.target[0], LEFT)

        self.play(FadeOut(t1))
        self.play(
            FadeOut(if_even),
            FadeOut(if_odd),
            FadeInFrom(power2_code, RIGHT),
            MoveToTarget(ef3),
            MoveToTarget(of2),
            ReplacementTransform(if_even, et),
            ReplacementTransform(if_odd, ot),
        )
        self.wait()

        recursive_call_hr = SurroundingRectangle(
            power2_code.get_code().get_lines(5)[5:-1])
        xn2_hr = SurroundingRectangle(ef3[-1])

        ec_hr = SurroundingRectangle(power2_code.get_code().get_lines(7)[-4:-1])
        ef_hr = SurroundingRectangle(ef3[1:])

        oc_hr = SurroundingRectangle(power2_code.get_code().get_lines(9)[-6:-1])
        of_hr = SurroundingRectangle(of2[1:])

        for f, c in [(xn2_hr, recursive_call_hr), (ef_hr, ec_hr),
                     (of_hr, oc_hr)]:
            self.play(ShowCreation(f), ShowCreation(c))
            self.wait()
            self.play(Uncreate(f), Uncreate(c))
        self.wait()
