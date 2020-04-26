from manimlib.imports import *

from cs_education.csanim.code import CodeBlock
from cs_education.csanim.stacks import StackFrame, CallStack
from cs_education.end_scene import EndScene


class S01Recursion3Intro(Scene):

    def construct(self):
        title = TextMobject('Recursion: Part 3').scale(1.5).to_edge(UP)
        self.play(ShowCreation(title))
        self.wait(duration=0.5)

        t1 = TextMobject("\\textit{Fun with multiple recursive calls}")
        self.play(ShowCreation(t1))
        self.wait(duration=2)

        self.play(FadeOut(title), FadeOut(t1))


class S02FibIntro(Scene):

    def construct(self):
        title = TextMobject("Fibonacci Numbers").scale(1.2)
        desc1 = TextMobject(
            "Each number is called $F_n$ and they make a sequence")
        title.to_edge(UP)
        desc1.next_to(title, DOWN, buff=LARGE_BUFF)
        self.play(FadeIn(title))
        self.play(ShowCreation(desc1))
        self.wait()

        f0 = TexMobject("F_0 = 0")
        f1 = TexMobject("F_1 = 1")
        fn = TexMobject("F_n = F_{n-1} + F_{n-2}")
        fg = VGroup(f0, f1, fn)
        fg.arrange(RIGHT, buff=LARGE_BUFF).shift(UP)
        self.play(ShowCreation(f0))
        self.wait()
        self.play(ShowCreation(f1))
        self.wait()
        self.play(ShowCreation(fn))
        self.wait(duration=2)

        seq_desc1 = TextMobject("Each number is the sum of the two before it")
        seq_desc1.next_to(fg, DOWN, buff=LARGE_BUFF)
        self.play(FadeInFromDown(seq_desc1))
        self.wait(duration=2)

        # seq_desc2 = TextMobject("Let's write it out")
        # seq_desc2.move_to(seq_desc1)
        # self.play(ReplacementTransform(seq_desc1, seq_desc2))
        # self.wait()
        seq_desc2 = seq_desc1

        fib_seq = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
        fs = TexMobject(*[str(n) + ',' for n in fib_seq], '...')
        fs.space_out_submobjects(1.25)
        fs.next_to(seq_desc2, DOWN, buff=MED_LARGE_BUFF)
        self.play(FadeIn(fs[0]), FadeIn(fs[1]))

        seq_speed = 1.0
        bl_prev = None
        s_prev = None
        for a, b, ta, tb, ts in zip(fib_seq[:-1], fib_seq[1:-1], fs[:-1],
                                    fs[1:-1], fs[2:-1]):
            bl = BraceLabel(VGroup(ta, tb),
                            '%d+%d=' % (a, b),
                            brace_direction=DOWN)
            s = TexMobject(str(a + b))
            s.next_to(bl.label, RIGHT)
            if bl_prev:
                self.play(ReplacementTransform(bl_prev, bl),
                          ReplacementTransform(s_prev, s),
                          run_time=seq_speed)
            else:
                self.play(ShowCreation(bl), ShowCreation(s))
            if seq_speed > 0.5:
                self.wait(duration=seq_speed)

            sc = s.copy()
            sc.generate_target()
            sc.target.next_to(ts,
                              direction=ORIGIN,
                              submobject_to_align=sc.target[0][0],
                              index_of_submobject_to_align=0)
            self.play(MoveToTarget(sc), FadeIn(ts[-1]), run_time=seq_speed / 2)

            if a >= 2:
                seq_speed = 0.3
            bl_prev = bl
            s_prev = s

        self.play(ShowCreation(fs[-1]), FadeOut(bl_prev), FadeOut(s_prev))
        self.clear()
        self.add(title, desc1, fg, seq_desc2, fs)
        self.wait()

        rec_desc1 = TextMobject("So, this looks a bit recursive!")
        rec_desc2 = TextMobject("Let's turn it into some code...")
        rec_desc1.next_to(fg, DOWN, buff=LARGE_BUFF)
        rec_desc2.next_to(rec_desc1, DOWN)
        self.play(ReplacementTransform(VGroup(seq_desc2, fs), rec_desc1))
        self.wait()
        self.play(FadeInFromDown(rec_desc2))
        self.wait(duration=2)

        self.play(*[FadeOut(o) for o in [title, desc1, rec_desc1, rec_desc2]])


class S03FibonacciToCode(Scene):

    def construct(self):
        f0 = TexMobject("F_0 = 0")
        f1 = TexMobject("F_1 = 1")
        fn = TexMobject("F_n = F_{n-1} + F_{n-2}")
        fg = VGroup(f0, f1, fn)
        fg.arrange(RIGHT, buff=LARGE_BUFF).shift(UP)
        self.add(fg)

        fib_small_code = CodeBlock(
            'Java',
            r"""
            public static int fib(int n) {
                if (n == 0) {
                    return 0;
                }
                if (n == 1) {
                    return 1;
                }
                return fib(n - 1) + fib(n - 2);
            }
            """,
        )
        fib_code = CodeBlock(
            'Java',
            r"""
            public static int fib(int n) {
                if (n == 0) {
                    return 0;
                }
                if (n == 1) {
                    return 1;
                }
                int fn1 = fib(n - 1);
                int fn2 = fib(n - 2);
                return fn1 + fn2;
            }
            """,
        )

        fib_small_code.to_edge(RIGHT)
        f0.generate_target()
        f1.generate_target()
        fn.generate_target()
        fsc = fib_small_code.get_code()
        eq_code_buff = LARGE_BUFF * 1.5
        f0.target.next_to(fsc.get_lines((2, 5)), LEFT, buff=eq_code_buff)
        f1.target.next_to(fsc.get_lines((5, 8)), LEFT, buff=eq_code_buff)
        fn.target.next_to(fsc.get_lines(8), LEFT, buff=eq_code_buff)
        self.play(*[MoveToTarget(o) for o in [f0, f1, fn]],)
        self.play(FadeInFrom(fib_small_code, RIGHT),)
        self.wait(duration=3)

        fib_small_code.generate_target()
        fib_small_code.target.move_to(fib_code, aligned_edge=UL)
        self.play(FadeOut(VGroup(f0, f1, fn)), MoveToTarget(fib_small_code))

        adj_desc = TextMobject(
            "Let's make this a little easier to trace through...")
        adj_desc.to_edge(DOWN)
        self.play(FadeIn(adj_desc))
        self.wait()

        fc = fib_code.get_code()
        self.play(
            fsc[-2].next_to,
            fc[-2],
            {
                'direction': ORIGIN,
                'index_of_submobject_to_align': 0,
            },
            fsc[-1].move_to,
            fc[-1],
            {'aligned_edge': LEFT},
        )

        # 012 345 6 78901 2 345
        # int fn1 = fib(n - 1);
        self.play(FadeIn(fc[-4][:7]),)

        # 012345 67890 1 23 4 56789 0 123
        # return fib(n - 1) + fib(n - 2);
        self.play(
            fsc[-2][6:14].move_to,
            fc[-4][7:15],
        )

        # 012345 678 9 0123
        # return fn1 + fn2;
        self.play(
            FadeIn(fc[-4][-1]),
            FadeIn(fc[-2][6:9]),
            fsc[-2][14].move_to,
            fc[-2][9],
        )

        self.play(FadeIn(fc[-3][:7]),)
        self.play(
            fsc[-2][15:23].move_to,
            fc[-3][7:15],
        )
        self.play(
            FadeIn(fc[-3][-1]),
            FadeIn(fc[-2][10:13]),
            fsc[-2][-1].move_to,
            fc[-2][-1],
        )
        self.clear()
        self.add(fib_code, adj_desc)
        self.wait()

        t1 = TextMobject("Okay, let's run it")
        t1.move_to(adj_desc)
        self.play(ReplacementTransform(adj_desc, t1))
        self.wait(duration=2)

        self.play(FadeOut(t1))


class S04RunFib(Scene):

    def construct(self):
        fib_code = CodeBlock(
            'Java',
            r"""
            public static int fib(int n) {
                if (n == 0) {
                    return 0;
                }
                if (n == 1) {
                    return 1;
                }
                int fn1 = fib(n - 1);
                int fn2 = fib(n - 2);
                return fn1 + fn2;
            }
            """,
        )
        self.add(fib_code)

        main_code = CodeBlock(
            'Java',
            r"""
            public static void main(String[] args) {
                int x = fib(3);
            }
            """,
            line_offset=11,
            code_scale=0.6,
        )

        frame_width = 2.5
        main_frame = StackFrame(main_code,
                                'main()',
                                13, ['x'],
                                width=frame_width)
        main_code.highlight_lines(13)
        VGroup(main_code, main_frame).arrange(RIGHT,
                                              buff=LARGE_BUFF * 2).to_edge(DOWN)
        self.play(
            fib_code.to_edge,
            UP,
            FadeInFromDown(main_frame),
            FadeInFromDown(main_code),
        )
        self.wait()

        def call_fib(run_ctx, n, call_stack):
            run_ctx['call_count'] += 1
            call_ret_delay = 0.5
            stack_frame = StackFrame(fib_code,
                                     'fib(%d)' % n,
                                     1, ['n', 'fn1', 'fn2'],
                                     width=frame_width)
            call_stack.animate_call(stack_frame, self)

            self.play(
                *stack_frame.get_update_line_anims(2),
                stack_frame.update_slot,
                'n',
                n,
            )

            if n == 0:
                self.play(*stack_frame.get_update_line_anims(3))
                self.wait(duration=call_ret_delay)
                call_stack.animate_return(self)
                return 0

            self.play(*stack_frame.get_update_line_anims(5))
            if n == 1:
                self.play(*stack_frame.get_update_line_anims(6))
                self.wait(duration=call_ret_delay)
                call_stack.animate_return(self)
                return 1

            self.play(*stack_frame.get_update_line_anims(8))
            self.wait(duration=call_ret_delay)
            fn1 = call_fib(run_ctx, n - 1, call_stack)
            self.play(
                *stack_frame.get_update_line_anims(9),
                stack_frame.update_slot,
                'fn1',
                fn1,
            )

            if run_ctx['call_count'] == 4:
                t1 = TextMobject('\\textit{Whoa!!}')
                t1.set_color(YELLOW).scale(1.2)
                t1.next_to(fib_code, LEFT, buff=MED_LARGE_BUFF)
                self.play(GrowFromCenter(t1))
                t2 = TextMobject("\\textit{I'm lost...}")
                t2.next_to(t1, DOWN, buff=LARGE_BUFF)
                self.play(FadeInFromPoint(t2, t2.get_center()))
                run_ctx['whoa_desc'] = VGroup(t1, t2)

            self.wait(duration=call_ret_delay)
            fn2 = call_fib(run_ctx, n - 2, call_stack)
            self.play(
                *stack_frame.get_update_line_anims(10),
                stack_frame.update_slot,
                'fn2',
                fn2,
            )

            self.wait(duration=call_ret_delay)
            call_stack.animate_return(self)
            return fn1 + fn2

        run_ctx = {
            'call_count': 0,
        }

        result = call_fib(run_ctx, 3, CallStack(main_frame))
        self.play(
            *main_frame.get_update_line_anims(14),
            main_frame.update_slot,
            'x',
            result,
        )
        self.wait(duration=2)

        hrm_desc = TextMobject("That worked, but it was really hard to follow!")
        hrm_desc.next_to(fib_code, DOWN, buff=MED_LARGE_BUFF)
        self.play(FadeOutAndShiftDown(main_frame),
                  FadeOutAndShiftDown(main_code), FadeOut(run_ctx['whoa_desc']))
        self.play(FadeInFromDown(hrm_desc))
        self.wait(duration=2.5)

        t1 = TextMobject("The call stack shows where we are at any moment")
        t1.move_to(hrm_desc)
        t2 = TextMobject("but we don't know where we've been...")
        t2.next_to(t1, DOWN)
        t3 = TextMobject("or where we're going...")
        t3.next_to(t2, DOWN)

        self.play(ReplacementTransform(hrm_desc, t1))
        self.wait(duration=2)
        self.play(FadeInFromDown(t2))
        self.wait(duration=2)
        self.play(FadeInFromDown(t3))
        self.wait(duration=2)

        t4 = TextMobject("Let's go again, but draw a new picture along the way")
        t4.move_to(t1)
        self.play(*[FadeOutAndShift(o, UP) for o in [t1, t2, t3]],
                  FadeInFromDown(t4))
        self.wait(duration=2.5)
        self.play(FadeOut(t4))


# This is a very rough binary tree setup, not generic at all yet.
# @TODO: factor this out and make it more generally usefull.
class BinaryTreeNode(VGroup):
    CONFIG = {
        'text_scale': 0.75,
    }

    def __init__(self, label, level=1, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)

        self.label = TextMobject(label).scale(self.text_scale)
        self.add(self.label)

        self.level = level
        self.left = None
        self.right = None
        self.parent = None


class BinaryTree(VGroup):
    CONFIG = {
        'text_scale': 0.75,
        'max_depth': 3,
        'leaf_height': 1,
        'level_buff': MED_SMALL_BUFF,
        'level_spreads': [],
    }

    def __init__(self, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)

        self.level_height_vec = DOWN * (self.leaf_height + MED_LARGE_BUFF)
        self.current_rect = None

    def get_line(self, p, n, direction):
        if not p:
            return None
        l = Line(p.get_corner(DOWN + direction) + DOWN * SMALL_BUFF,
                 n.get_corner(UP + direction * -1) + UP * SMALL_BUFF,
                 stroke_width=2,
                 color=GREY)
        return l

    def add_left_node(self, parent, label):
        level = parent.level + 1 if parent else 1
        n = BinaryTreeNode(label, level, text_scale=self.text_scale)
        n.parent = parent
        if parent:
            parent.left = n
            n.move_to(parent)
            n.shift(self.level_height_vec +
                    (LEFT * self.level_spreads[parent.level - 1]))
        l = self.get_line(parent, n, LEFT)
        self.add(n, l)
        return n, l

    def add_right_node(self, parent, label):
        level = parent.level + 1 if parent else 1
        n = BinaryTreeNode(label, level, text_scale=self.text_scale)
        n.parent = parent
        if parent:
            parent.right = n
            n.move_to(parent)
            n.shift(self.level_height_vec +
                    (RIGHT * self.level_spreads[parent.level - 1]))
        l = self.get_line(parent, n, RIGHT)
        self.add(n, l)
        return n, l


class S05RunFibWithTree(EndScene):

    def get_fib_code(self, scale):
        return CodeBlock(
            'Java',
            r"""
            public static int fib(int n) {
                if (n == 0) {
                    return 0;
                }
                if (n == 1) {
                    return 1;
                }
                int fn1 = fib(n - 1);
                int fn2 = fib(n - 2);
                return fn1 + fn2;
            }
            """,
            code_scale=scale,
        )

    def construct(self):
        fib_code = self.get_fib_code(0.75)
        fib_code.to_edge(UP)
        self.add(fib_code)

        fc2 = self.get_fib_code(0.6)
        fc2.to_edge(UR)
        self.play(ReplacementTransform(fib_code, fc2))
        fib_code = fc2

        first_fib_arg = 4
        main_code = CodeBlock(
            'Java',
            r"""
            public static void main(String[] args) {
                int x = fib(%d);
            }
            """ % first_fib_arg,
            line_offset=11,
            code_scale=0.6,
        )

        main_frame = StackFrame(main_code,
                                'main()',
                                13, ['x'],
                                width=2.5,
                                text_scale=0.6)
        main_code.highlight_lines(13)
        VGroup(main_code, main_frame).arrange(RIGHT,
                                              buff=LARGE_BUFF * 2).to_edge(DOWN)
        tree_area_frame = Polygon(
            np.array((-FRAME_X_RADIUS, FRAME_Y_RADIUS, 0)),
            np.array((fib_code.get_corner(UL)[0], FRAME_Y_RADIUS, 0)),
            np.array((fib_code.get_corner(DL)[0], main_code.get_top()[1], 0)),
            np.array((-FRAME_X_RADIUS, main_code.get_top()[1], 0)),
            mark_paths_closed=True,
            close_new_points=True,
        )

        ready_desc = TextMobject(
            "We'll compute $F_%d$\\\\and track \\textit{all} "
            "our work as we go" % first_fib_arg)
        ready_desc.move_to(tree_area_frame)
        self.play(FadeIn(ready_desc))
        self.wait(duration=2)

        self.play(
            fib_code.to_edge,
            UP,
            FadeInFromDown(main_frame),
            FadeInFromDown(main_code),
        )

        tree_text_scale = 1.0
        tmp_leaf = TextMobject('$F_%d$' % 1).scale(tree_text_scale)
        leaf_width = tmp_leaf.get_width()
        level_spread_factors = [4, 1.9, 1.75]
        level_spreads = [f * leaf_width for f in level_spread_factors]

        tree = BinaryTree(
            max_depth=first_fib_arg,
            leaf_height=tmp_leaf.get_height(),
            level_buff=LARGE_BUFF * 1.5,
            level_spreads=level_spreads,
            text_scale=tree_text_scale,
        )

        def update_for_return(current_node, val, run_ctx):
            v = TextMobject(str(val))
            # v = TextMobject(current_node.label.tex_string, '$=%d$' % val)
            v.set_color(GREEN_SCREEN)
            v.scale(tree_text_scale)
            v.move_to(current_node.label)
            self.play(ReplacementTransform(current_node.label, v))
            self.wait(duration=run_ctx['update_node_delay'])
            extra_anims = []
            if current_node.parent:
                sr = SurroundingRectangle(current_node.parent)
                extra_anims.append(ReplacementTransform(tree.current_rect, sr))
                tree.current_rect = sr
                extra_anims.append(
                    ApplyMethod(current_node.parent.set_color, YELLOW))
            else:
                extra_anims.append(FadeOut(tree.current_rect))
            return extra_anims

        def call_fib(run_ctx, call_stack, current_node, n):
            run_ctx['call_count'] += 1
            call_ret_delay = 0.5
            stack_frame = StackFrame(fib_code,
                                     'fib(%d)' % n,
                                     1, ['n', 'fn1', 'fn2'],
                                     width=call_stack[0].width,
                                     text_scale=call_stack[0].text_scale)
            sr = SurroundingRectangle(current_node)
            extra_anims = [current_node.set_color, YELLOW]
            if tree.current_rect:
                extra_anims.append(ReplacementTransform(tree.current_rect, sr))
            else:
                extra_anims.append(ShowCreation(sr))
            tree.current_rect = sr
            if current_node.parent:
                extra_anims.append(
                    ApplyMethod(current_node.parent.set_color, ORANGE))
            call_stack.animate_call(stack_frame, self, extra_anims=extra_anims)

            self.play(
                *stack_frame.get_update_line_anims(2),
                stack_frame.update_slot,
                'n',
                n,
            )
            if n == 0:
                self.play(*stack_frame.get_update_line_anims(3))
                self.wait(duration=call_ret_delay)

                extra_anims = []
                if run_ctx['call_count'] == 5:
                    s1 = TextMobject("and we know $F_0=0$")
                    s1.move_to(tree_area_frame).shift(DOWN)
                    self.play(FadeIn(s1))
                    extra_anims.append(FadeOut(s1))

                extra_anims.extend(update_for_return(current_node, 0, run_ctx))
                call_stack.animate_return(self, extra_anims=extra_anims)
                return 0

            self.play(*stack_frame.get_update_line_anims(5))
            if n == 1:
                self.play(*stack_frame.get_update_line_anims(6))
                self.wait(duration=call_ret_delay)

                extra_anims = []
                if run_ctx['call_count'] == 4:
                    s1 = TextMobject("we know $F_1=1$")
                    s1.move_to(tree_area_frame).shift(DOWN)
                    self.play(FadeIn(s1))
                    extra_anims.append(FadeOut(s1))

                extra_anims.extend(update_for_return(current_node, 1, run_ctx))
                call_stack.animate_return(self, extra_anims=extra_anims)
                return 1

            self.play(*stack_frame.get_update_line_anims(8))

            self.wait(duration=call_ret_delay)

            s1 = None
            if run_ctx['call_count'] == 1:
                s1 = TextMobject('we need $F_3$ and $F_2$')
                s1.move_to(tree_area_frame)
                self.play(FadeIn(s1))
                self.wait()
            elif run_ctx['call_count'] == 2:
                s1 = TextMobject('and now we need $F_2$ and $F_1$')
                s1.move_to(tree_area_frame).shift(DOWN)
                self.play(FadeIn(s1))
                self.wait()

            left_node, ll = tree.add_left_node(current_node, '$F_%d$' % (n - 1))
            right_node, rl = tree.add_right_node(current_node,
                                                 '$F_%d$' % (n - 2))
            left_node.set_color(BLUE)
            right_node.set_color(BLUE)
            self.add(ll, rl, tree.current_rect)  # Keep the rect on top of lines
            self.play(*[FadeIn(o) for o in [left_node, ll, right_node, rl]])

            if s1:
                self.wait()
                self.play(FadeOut(s1))
                s1 = None

            fn1 = call_fib(run_ctx, call_stack, left_node, n - 1)

            if run_ctx['call_count'] == 4:
                s1 = TextMobject("now do the other half")
                s1.move_to(tree_area_frame).shift(DOWN)
                self.play(FadeIn(s1))
            elif run_ctx['call_count'] == 6:
                t1 = TextMobject("Using a ``tree'' for this is \\textit{much} "
                                 "more helpful!").scale(0.8)
                t2 = TextMobject("Shows where we've ", "been", ", where we ",
                                 "are", ",\\\\and where we're ", "going")
                t2.scale(0.8)
                t2.set_color_by_tex_to_color_map({
                    "been": GREEN_SCREEN,
                    "are": YELLOW,
                    "going": BLUE,
                })
                t1.move_to(tree_area_frame).shift(DOWN)
                t2.next_to(t1, DOWN, buff=MED_SMALL_BUFF)
                self.play(FadeIn(t1))
                self.wait()
                self.play(Write(t2))
                self.wait()
                run_ctx['final_desc'] = VGroup(t1, t2)

            self.play(
                *stack_frame.get_update_line_anims(9),
                stack_frame.update_slot,
                'fn1',
                fn1,
            )

            if s1:
                self.wait()
                self.play(FadeOut(s1))
                s1 = None

            self.wait(duration=call_ret_delay)
            fn2 = call_fib(run_ctx, call_stack, right_node, n - 2)

            extra_anims = []
            if run_ctx['call_count'] == 5:
                s1 = TextMobject("add the two halves")
                s1.move_to(tree_area_frame).shift(DOWN)
                self.play(FadeIn(s1))
                extra_anims.append(FadeOut(s1))
                run_ctx['update_node_delay'] = 0.1

            self.play(
                *stack_frame.get_update_line_anims(10),
                stack_frame.update_slot,
                'fn2',
                fn2,
            )

            self.wait(duration=call_ret_delay)
            extra_anims.extend(
                update_for_return(current_node, fn1 + fn2, run_ctx))
            call_stack.animate_return(self, extra_anims=extra_anims)
            return fn1 + fn2

        root_node, _ = tree.add_left_node(None, '$F_%d$' % first_fib_arg)
        root_node.move_to(tree_area_frame)
        root_node.to_edge(UP)
        self.play(ShowCreation(root_node))
        self.wait()

        self.play(FadeOut(ready_desc))

        run_ctx = {
            'call_count': 0,
            'update_node_delay': 1.0,
        }

        result = call_fib(run_ctx, CallStack(main_frame, scroll_height=1),
                          root_node, first_fib_arg)
        self.play(
            *main_frame.get_update_line_anims(14),
            main_frame.update_slot,
            'x',
            result,
        )
        self.wait(duration=2)

        self.play(FadeOutAndShiftDown(main_code),
                  FadeOutAndShiftDown(main_frame))
        self.wait()

        t1 = TextMobject("It is common to see recursive algorithms "
                         "described with trees")
        t2 = TextMobject("\\textit{Try drawing them out as you go!}")
        t2.set_color(GREEN)
        t2.to_edge(DOWN)
        t1.next_to(t2, UP, buff=MED_LARGE_BUFF)
        self.play(FadeInFromDown(t1))
        self.wait(duration=1.5)
        self.play(Write(t2))
        self.wait(duration=5)

        x = self.camera.get_mobjects_to_display(self.mobjects)
        end_scale_group = VGroup(*x)
        end_fade_group = VGroup()
        self.animate_yt_end_screen(end_scale_group,
                                   end_fade_group,
                                   end_scale=0.6,
                                   show_elements=False)
