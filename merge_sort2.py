from csanim.arrays import Array
from csanim.code import CodeBlock
from csanim.exposition import BasilExposition
from csanim.trees import Tree
from end_scene import EndScene
from manimlib.imports import *


class S01MergeSort2Intro(Scene):

    def construct(self):
        title = TextMobject('Merge Sort - Part 2').scale(1.5).to_edge(UP)
        self.play(ShowCreation(title))
        self.wait(duration=0.5)

        t1 = TextMobject("Divide-and-conquer with recursion")
        t1.shift(UP)
        self.play(ShowCreation(t1))
        self.wait(duration=2)

        t2 = TextMobject(
            "Watching the 3-part series of recursion videos first will help!")
        t3 = TextMobject("\\textit{Video links in the description}").scale(0.8)
        t2.set_color(YELLOW)
        t3.set_color(YELLOW)
        t2.next_to(t1, DOWN, buff=LARGE_BUFF)
        t3.next_to(t2, DOWN)
        self.play(FadeInFromDown(t2), FadeInFromDown(t3))
        self.wait(duration=4)

        visible = self.camera.get_mobjects_to_display(self.mobjects)
        self.play(*[FadeOut(o) for o in visible])


# Tree used to represent a merge sort both down and back up
class MergeSortTree(Tree):

    def __init__(self, values, parent, text_scale=1.0):
        super().__init__(parent)
        self.values = values
        self.result = None

        if parent is not None:
            self.text_scale = parent.text_scale
        else:
            self.text_scale = text_scale

        self.label = Array(values, show_labels=False).scale(self.text_scale)
        self.result_label = None

    def create_line_between(self):
        pl = self.parent.label
        l = self.label
        if pl.get_x() <= l.get_x():
            direction = RIGHT
        else:
            direction = LEFT
        w = pl.get_width() / 4
        return Line(pl.get_bottom() + direction * w + DOWN * SMALL_BUFF,
                    l.get_top() + UP * SMALL_BUFF,
                    stroke_width=2,
                    color=GREY)

    def create_result_label(self):
        self.result_label = Array(self.result, show_labels=False)
        self.result_label.scale(self.text_scale)
        self.result_label.move_to(self.label)
        return self.result_label


def build_merge_sort_tree(values, parent=None, text_scale=1.0):
    tree = MergeSortTree(values, parent, text_scale)
    if len(values) == 1:
        tree.result = [values[0]]
        tree.create_result_label()
        return tree

    middle = len(values) // 2
    left = build_merge_sort_tree(values[:middle], tree)
    right = build_merge_sort_tree(values[middle:], tree)

    merged = []
    l = r = 0
    while l < len(left.result) and r < len(right.result):
        if left.result[l] <= right.result[r]:
            merged.append(left.result[l])
            l += 1
        else:
            merged.append(right.result[r])
            r += 1
    if l < len(left.result):
        merged.extend(left.result[l:])
    else:
        merged.extend(right.result[r:])
    tree.result = merged
    tree.create_result_label()
    return tree


def update_tree_colors(tree, colors):
    for e, n in zip(tree.label.elements, tree.values):
        e.set_color(colors[n])
    for e, n in zip(tree.result_label.elements, tree.result):
        e.set_color(colors[n])
    for c in tree.children:
        update_tree_colors(c, colors)


# Base scene for all of our merge sort scenes
class MergeTreeBase(Scene):

    def get_call_rect_anims(self, tree, be):
        sr = SurroundingRectangle(tree.label, stroke_width=2)
        be.current_rect, tmp = sr, be.current_rect
        if tmp:
            return [ReplacementTransform(tmp, sr)]
        else:
            return [ShowCreation(sr)]

    def get_return_rect_anims(self, tree, be):
        if tree.parent is not None:
            sr = SurroundingRectangle(tree.parent.label, stroke_width=2)
            be.current_rect, tmp = sr, be.current_rect
            return [ReplacementTransform(tmp, sr)]
        else:
            return [Uncreate(be.current_rect)]

    @staticmethod
    def highlight_lines(be, line):
        if be.code_visible:
            be.play(be.code.highlight_lines, line)

    def run_merge_sort(self, tree, be, ret_line):
        if be.code_visible:
            be.deferred_play_next(*self.get_call_rect_anims(tree, be))
            if ret_line == 0:
                be.play(be.code.highlight_lines, 1)
            else:
                xi = be.code.pre_call(be.code, 1)
                be.play(*be.code.get_control_transfer_counterclockwise(xi))
                be.code.post_control_transfer(xi, self)
        else:
            be.play(*self.get_call_rect_anims(tree, be))

        self.highlight_lines(be, 2)
        if len(tree.children) == 0:
            if be.code_visible:
                be.deferred_play_next(be.code.highlight_lines, 3)
            be.play(tree.label.outline.set_color, GREEN)
            be.explain(be.base_case)
        else:
            self.highlight_lines(be, 5)
            be.explain(be.find_mid, mid=len(tree.values) // 2)

            lc = tree.children[0]
            rc = tree.children[1]
            if be.code_visible:
                self.highlight_lines(be, 7)
                be.explain(be.split_left, child=lc)

                self.highlight_lines(be, 8)
                be.explain(be.split_right, child=rc)
                be.play(be.code.highlight_lines, 9, be.code.set_annotation, 5,
                        None)
            else:
                # Show them together once the code is gone
                be.explain(be.split_both, lc=lc, rc=rc)

            be.explain(be.recurse_left)
            self.run_merge_sort(lc, be, 9)

            self.highlight_lines(be, 10)
            be.explain(be.recurse_right)
            self.run_merge_sort(rc, be, 10)

            self.highlight_lines(be, 11)
            self.do_merge(tree, tree.children[0], tree.children[1], be)
            be.play(tree.label.outline.set_color, GREEN)

        if be.code_visible:
            xi = be.code.pre_return(be.code, ret_line)
            be.deferred_play_next(*self.get_return_rect_anims(tree, be))
            be.play(*be.code.get_control_transfer_clockwise(xi))
            be.code.post_control_transfer(xi, self)
        else:
            be.play(*self.get_return_rect_anims(tree, be))

    def do_merge(self, parent, left, right, be):
        be.explain(be.merge_start, parent=parent)
        self.play(FadeOut(parent.label.elements), run_time=be.merge_run_time)
        left.result_label.move_to(left.label)
        right.result_label.move_to(right.label)
        l = r = m = 0
        while l < len(left.result) and r < len(right.result):
            if left.result[l] <= right.result[r]:
                c = left.result_label.elements[l].copy()
                l += 1
            else:
                c = right.result_label.elements[r].copy()
                r += 1
            self.play(c.move_to,
                      parent.label.elements[m],
                      run_time=be.merge_run_time)
            m += 1

        def append_rest(side, i, m):
            while i < len(side.result):
                c = side.result_label.elements[i].copy()
                i += 1
                self.play(c.move_to,
                          parent.label.elements[m],
                          run_time=be.merge_run_time)
                m += 1

        if l < len(left.result):
            append_rest(left, l, m)
        else:
            append_rest(right, r, m)

        be.explain(be.merge_end)


class MergeExposition(BasilExposition):

    def __init__(self, scene, tree, code):
        super().__init__(scene)
        self.tree_root = tree
        self.code = code
        self.run_time = 1.0 if len(tree.values) < 10 else 0.5
        self.merge_run_time = 0.3
        self.current_rect = None
        self.code_visible = True

    def find_mid(self, scene, count, mid=0):
        pass

    def split_left(self, scene, count, child=None):
        pass

    def split_right(self, scene, count, child=None):
        pass

    def split_both(self, scene, count, lc=None, rc=None):
        pass

    def recurse_left(self, scene, count):
        pass

    def recurse_right(self, scene, count):
        pass

    def base_case(self, scene, count):
        pass

    def merge_start(self, scene, count, parent=None):
        pass

    def merge_end(self, scene, count):
        pass


class S02Merge8WithCode(MergeTreeBase):

    def construct(self):
        unsorted = [11, 0, 8, 2, 2, 9, 14, 5]

        code_scale = 0.6
        # TODO: move to base, since it references code lines and runs this code
        ms_code = CodeBlock(
            'Java',
            r"""
            public static int[] mergeSort(int[] a) {
                if (a.length == 1) {
                    return a;
                }
                int m = a.length / 2;
                int[] l, r;
                l = Arrays.copyOfRange(a, 0, m);
                r = Arrays.copyOfRange(a, m, a.length);
                l = mergeSort(l);
                r = mergeSort(r);
                return merge(l, r);
            }
            """,
            code_scale=code_scale,
        )
        ms_code.set_annotation(5, None)

        t1 = TextMobject("Recursive mergesort in Java")
        t1.to_edge(UP)
        ms_code.next_to(t1, DOWN, buff=MED_LARGE_BUFF)
        self.play(FadeIn(t1))
        self.play(
            LaggedStartMap(FadeInFromDown, ms_code.get_code(), lag_ratio=0.2))
        self.wait(duration=3.0)

        t2 = TextMobject(
            "Let's trace through this and track our work with a tree",
            buff=LARGE_BUFF)
        t2.next_to(ms_code, DOWN, buff=LARGE_BUFF)
        self.play(FadeInFromDown(t2))
        self.wait(duration=3)

        self.play(ms_code.to_edge, DR, FadeOutAndShiftDown(t2),
                  FadeOutAndShift(t1, UP))

        colors = color_gradient([PINK, BLUE, YELLOW_D], 15)
        tree = build_merge_sort_tree(unsorted, text_scale=1.0)
        update_tree_colors(tree, colors)
        tree.layout(1.6, 1.2)
        g = tree.to_vgroup()
        g.center().to_edge(UP)

        be = Merge8Exposition(self, tree, ms_code)

        t1 = TextMobject("Start with an array of random numbers")
        t1.next_to(tree.label, DOWN, buff=MED_LARGE_BUFF)
        be.deferred_play(1, FadeIn(t1))
        be.deferred_wait(1)
        be.deferred_play(3, FadeOut(t1))

        be.play(FadeIn(tree.label))
        self.run_merge_sort(tree, be, 0)
        self.wait()

        t1 = TextMobject("We divide the problem on the way down")
        t2 = TextMobject("and we recombine by merging on the way up")
        t1.shift(DOWN * 1.5)
        t2.next_to(t1, DOWN)
        self.play(FadeInFromDown(t1))
        self.wait()
        self.play(FadeInFromDown(t2))
        self.wait(duration=3)

        t3 = TextMobject("We call this \\textit{divide-and-conquer}")
        t4 = TextMobject("\\textit{This is very common!} You'll see it a lot.")
        t3.shift(DOWN * 1.5)
        t4.next_to(t3, DOWN)
        self.play(FadeOutAndShiftDown(t1), FadeOutAndShiftDown(t2))
        self.play(FadeInFromDown(t3))
        self.wait()
        self.play(FadeInFromDown(t4))
        self.wait(duration=3)

        t5 = TextMobject("This one was nicely balanced and even...")
        t6 = TextMobject("let's try one that's a little bit odd")
        t5.shift(DOWN * 1.5)
        t6.next_to(t5, DOWN)
        self.play(FadeOutAndShiftDown(t3), FadeOutAndShiftDown(t4))
        self.play(FadeInFromDown(t5))
        self.wait()
        self.play(FadeInFromDown(t6))
        self.wait(duration=3)

        self.play(*[FadeOut(o) for o in self.mobjects])


class Merge8Exposition(MergeExposition):

    def find_mid(self, scene, count, mid=0):
        if count == 1:
            t1 = TextMobject("Find the middle so we\\\\can split it in half")
            t1.next_to(self.code.get_lines(5), LEFT, buff=LARGE_BUFF)
            scene.play(FadeIn(t1))
            scene.wait()
            scene.play(self.code.set_annotation, 5, 'm=%d' % mid)
            scene.play(Indicate(self.code.get_annotation(5), scale_factor=2.0))
            scene.wait()
            self.deferred_play_next(FadeOut(t1))
        elif count == 2:
            t1 = TextMobject("Again, find the middle")
            t1.next_to(self.code.get_lines(5), LEFT, buff=LARGE_BUFF)
            scene.play(FadeIn(t1), self.code.set_annotation, 5, 'm=%d' % mid)
            scene.wait()
            self.deferred_play_next(FadeOut(t1))
        elif self.code_visible:
            scene.play(self.code.set_annotation, 5, 'm=%d' % mid)

    def split_left(self, scene, count, child=None):
        if count == 1:
            t1 = TextMobject("Split off the left half...")
            t1.next_to(self.code.get_lines(7), LEFT, buff=LARGE_BUFF)
            self.play(FadeIn(t1))
            self.play(FadeIn(child.label), FadeIn(child.line_to_parent))
            self.play(Indicate(child.label))
            self.deferred_play(self.time + 5, FadeOut(t1))
        elif count == 2:
            t1 = TextMobject("And again, split into halves")
            t1.next_to(self.code.get_lines(7), LEFT, buff=LARGE_BUFF)
            self.play(FadeIn(t1))
            self.play(FadeIn(child.label), FadeIn(child.line_to_parent))
            self.deferred_play(self.time + 3, FadeOut(t1))
        else:
            self.play(FadeIn(child.label), FadeIn(child.line_to_parent))

    def split_right(self, scene, count, child=None):
        if count == 1:
            t1 = TextMobject("... and the right half")
            t1.next_to(self.code.get_lines(9), LEFT, buff=LARGE_BUFF)
            self.play(FadeIn(t1))
            self.play(FadeIn(child.label), FadeIn(child.line_to_parent))
            self.play(Indicate(child.label))
            self.deferred_play(self.time + 1, FadeOut(t1))
        else:
            self.play(FadeIn(child.label), FadeIn(child.line_to_parent))

    def split_both(self, scene, count, lc=None, rc=None):
        self.play(FadeIn(lc.label), FadeIn(lc.line_to_parent), FadeIn(rc.label),
                  FadeIn(rc.line_to_parent))

    def recurse_left(self, scene, count):
        if count == 1:
            t1 = TextMobject("Now go sort the left half")
            t1.next_to(self.code.get_lines(9), LEFT, buff=LARGE_BUFF)
            scene.play(FadeIn(t1))
            self.deferred_play_next(FadeOut(t1))
        elif count == 2:
            t1 = TextMobject("Rinse and repeat")
            t1.next_to(self.code.get_lines(9), LEFT, buff=LARGE_BUFF)
            scene.play(FadeIn(t1))
            self.deferred_play_next(FadeOut(t1))

        # Always delay a bit before calling
        if self.code_visible:
            scene.wait()

    def recurse_right(self, scene, count):
        if count == 1:
            t1 = TextMobject("Now do the right half")
            t1.next_to(self.code.get_lines(10), LEFT, buff=LARGE_BUFF)
            scene.play(FadeIn(t1))
            self.deferred_play_next(FadeOut(t1))
        elif count == 4:
            scene.play(FadeOutAndShift(self.code, RIGHT))
            self.code.shift(RIGHT * 10)
            self.code_visible = False

        # Always delay a bit before calling
        if self.code_visible:
            scene.wait()

    def base_case(self, scene, count):
        if count == 1:
            t1 = TextMobject("We've hit a base case")
            t1.next_to(self.code.get_lines(7), LEFT, buff=LARGE_BUFF * 2)
            t2 = TextMobject("So return this single-element,\\\\"
                             "\\textit{sorted} array")
            t2.next_to(t1, DOWN, buff=MED_LARGE_BUFF)
            scene.play(FadeIn(t1))
            scene.wait()
            scene.play(FadeIn(t2))
            scene.wait()
            self.deferred_play_next(FadeOut(t1), FadeOut(t2))
        elif count == 2:
            t1 = TextMobject("Again, we've hit the easy case")
            t1.next_to(self.code.get_lines(7), LEFT)
            t1.to_edge(LEFT, buff=MED_LARGE_BUFF)
            scene.play(FadeIn(t1))
            self.deferred_play_next(FadeOut(t1))

        # Always delay a bit before returning the base case
        if self.code_visible:
            scene.wait()

    def merge_start(self, scene, count, parent=None):
        if count == 1:
            t1 = TextMobject("Now we can merge\\\\the sorted halves")
            t1.next_to(self.code.get_lines(7), LEFT, buff=LARGE_BUFF * 2)
            t2 = TextMobject("\\texttt{merge()} from the first video")
            t2.scale(0.7).set_color(YELLOW)
            t2.next_to(self.code.get_lines(11), LEFT, buff=LARGE_BUFF * 2)
            l1 = Arrow(t2, self.code.get_current_highlight().get_left())
            l1.set_color(YELLOW)
            scene.play(FadeIn(t1))
            scene.wait()
            scene.play(FadeIn(t2), ShowCreation(l1))
            scene.wait()
            scene.play(FadeOutAndShift(t2, UP), FadeOutAndShift(l1, UP))
            scene.play(Indicate(parent.label, scale_factor=1.5))
            self.deferred_play_next(FadeOut(t1))
            t3 = TextMobject("\\textit{* Find a link to Merge Sort Part I "
                             "in the description}")
            t3.scale(0.5).set_color(BLUE)
            t3.to_edge(DR, buff=SMALL_BUFF)
            self.deferred_play(self.time + 2, FadeIn(t3))
            self.deferred_play(self.time + 40, FadeOut(t3))
        elif count == 2:
            t1 = TextMobject("Again, merge the\\\\sorted halves")
            t1.next_to(self.code.get_lines(7), LEFT, buff=LARGE_BUFF * 2)
            scene.play(FadeIn(t1))
            self.deferred_play_next(FadeOut(t1))


class S03MergeOdd(MergeTreeBase, EndScene):

    def construct(self):
        n = 11
        np.random.seed(42)
        unsorted = np.random.randint(0, 20, n).tolist()
        # unsorted = [11, 0, 8, 2, 2, 9, 14, 5]
        colors = color_gradient([PINK, BLUE, YELLOW_D], 20)
        tree = build_merge_sort_tree(unsorted, text_scale=1.0)
        update_tree_colors(tree, colors)
        tree.layout(1.6, 1.2)
        g = tree.to_vgroup()
        g.center().to_edge(UP)

        be = MergeOddExposition(self, tree, None)

        t1 = TextMobject("Start with %d numbers this time" % n)
        t1.next_to(tree.label, DOWN, buff=LARGE_BUFF)
        self.play(FadeIn(tree.label), FadeIn(t1))
        self.wait(duration=2)
        be.deferred_play_next(FadeOut(t1))

        self.run_merge_sort(tree, be, 0)
        self.wait()

        t1 = TextMobject("\\textit{This is classic divide-and-conquer!}")
        t1.to_edge(DOWN, buff=LARGE_BUFF)
        self.play(FadeOut(be.leftovers), FadeInFromDown(t1))

        self.wait(duration=5)

        x = self.camera.get_mobjects_to_display(self.mobjects)
        end_scale_group = VGroup(*x)
        end_fade_group = VGroup()
        self.animate_yt_end_screen(end_scale_group,
                                   end_fade_group,
                                   end_scale=0.6,
                                   show_elements=False)


class MergeOddExposition(MergeExposition):

    def __init__(self, scene, tree, code):
        super().__init__(scene, tree, code)
        self.code_visible = False
        self.run_time = 0.5
        self.merge_run_time = 0.2
        self.leftovers = VGroup()

    def split_both(self, scene, count, lc=None, rc=None):
        if count == 1:
            scene.play(FadeIn(lc.label), FadeIn(lc.line_to_parent),
                       FadeIn(rc.label), FadeIn(rc.line_to_parent))
            bl = BraceLabel(lc.label,
                            "5",
                            brace_direction=DOWN)
            br = BraceLabel(rc.label,
                            "6",
                            brace_direction=DOWN)
            scene.play(FadeIn(bl), FadeIn(br))
            scene.wait()
            self.deferred_play(self.time + 1, FadeOut(bl), FadeOut(br))
            return

        if count == 2:
            t1 = TextMobject("Another uneven split")
            t1.next_to(self.tree_root.label, DOWN, buff=LARGE_BUFF * 3)
            self.deferred_play_next(FadeIn(t1), run_time=1.0)
            self.deferred_wait(self.time + 1, duration=2)
            self.deferred_play(self.time + 2, FadeOut(t1))
        elif count == 5:
            t1 = TextMobject(
                "We end up with another level to handle the extras")
            t1.to_edge(DOWN, buff=LARGE_BUFF)
            self.deferred_play_next(FadeIn(t1), run_time=1.0)
            self.deferred_wait(self.time + 1)
            self.deferred_play(self.time + 6, FadeOut(t1))
        elif count == 6:
            t1 = TextMobject(
                "We're dividing recursively to find base cases,\\\\"
                "then merging (and sorting!) as we return.")
            t1.to_edge(DOWN)
            self.deferred_play_next(FadeInFromDown(t1), run_time=1.0)
            self.leftovers.add(t1)

        self.play(FadeIn(lc.label), FadeIn(lc.line_to_parent), FadeIn(rc.label),
                  FadeIn(rc.line_to_parent))

    def merge_start(self, scene, count, parent=None):
        if count == 3:
            t1 = TextMobject("Merging doesn't care if the sides are even")
            t1.to_edge(DOWN, buff=LARGE_BUFF)
            scene.play(FadeIn(t1))
            scene.wait(duration=1)
            self.deferred_play(self.time + 4, FadeOut(t1))
        elif count == 5:
            self.merge_run_time = 0.2
