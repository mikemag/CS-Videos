from manimlib.imports import *

from cs_education.csanim.arrays import Array, ArrayIndex


# Base class for all merge sort scenes, with support for a basic merge viz, and multi-level merge viz.
class MergeSortScenes(Scene):

    def __init__(self, **kwargs):
        self.merge_element_count = 0
        self.merge_current_level = 0
        self.merge_runtime = 1.0
        Scene.__init__(self, **kwargs)

    def construct(self):
        pass

    def merge_level_pair_begin(self, index):
        pass

    def merge_level_pair_end(self, index):
        pass

    def merge_level_extra_begin(self, index, extra):
        pass

    def merge_level_extra_end(self, index, extra):
        pass

    def merge_level(self, current_level, height, buff=SMALL_BUFF, speedy=False):
        new_level = VGroup()
        self.merge_current_level += 1
        for i in range(0, len(current_level), 2):
            if i + 1 < len(current_level):
                self.merge_level_pair_begin(i)
                left = current_level[i]
                right = current_level[i + 1]
                orig_group = VGroup(left, right)
                left = left.deepcopy()  # Leave the old ones in place, unharmed
                right = right.deepcopy()
                merged = Array([None] * (len(left.values) + len(right.values)),
                               show_labels=False)
                if height > 3:
                    merged.to_edge(TOP, buff=0.4)
                else:
                    merged.to_edge(TOP)
                halves = VGroup(left, right)
                if speedy:
                    self.play(
                        halves.arrange,
                        RIGHT,
                        {'buff': LARGE_BUFF},
                        halves.next_to,
                        merged,
                        DOWN,
                        ShowCreation(merged),
                        run_time=self.merge_runtime,
                    )
                else:
                    self.play(
                        halves.arrange,
                        RIGHT,
                        {'buff': LARGE_BUFF},
                        halves.next_to,
                        merged,
                        DOWN,
                        run_time=self.merge_runtime,
                    )
                    self.play(ShowCreation(merged))
                self.animate_merge(left, right, merged)
                self.play(merged.next_to,
                          orig_group,
                          UP, {'buff': buff},
                          run_time=self.merge_runtime)
                self.merge_level_pair_end(i)
            else:
                self.merge_level_extra_begin(i, current_level[i])
                merged = current_level[i].deepcopy()
                self.play(merged.next_to,
                          current_level[i],
                          UP, {'buff': buff},
                          run_time=self.merge_runtime)
                self.merge_level_extra_end(i, merged)
            new_level.add(merged)
        return new_level

    # dst[di] = src[si]
    def animate_merge_element(self, src, si, dest, di):
        self.merge_element_count += 1
        sec = src.elements[si.get_value()].copy()
        self.play(
            sec.move_to,
            dest.elements[di.get_value()],
            run_time=self.merge_runtime,
        )
        dest.elements.submobjects[di.get_value()] = sec
        dest.values[di.get_value()] = src.values[si.get_value()]
        self.play(
            *si.animate_set_index(si.get_value() + 1),
            *di.animate_set_index(di.get_value() + 1),
            run_time=self.merge_runtime,
        )

    def setup_animate_merge(self, left, right, merged):
        left_l = left.create_index(0, color=YELLOW, name='l')
        right_r = right.create_index(0, color=YELLOW, name='r')
        self.play(ShowCreation(left_l), ShowCreation(right_r))
        merged_m = merged.create_index(0, color=YELLOW, name='m', position=UP)
        self.play(ShowCreation(merged_m))
        self.wait()
        return left_l, right_r, merged_m

    def cleanup_animate_merge(self, left, left_l, right, right_r, merged,
                              merged_m):
        self.play(
            Uncreate(left_l),
            Uncreate(right_r),
            Uncreate(merged_m),
        )
        left.remove_index(left_l)
        right.remove(right_r)
        merged.remove_index(merged_m)
        self.play(FadeOutAndShift(left, UP + RIGHT),
                  FadeOutAndShift(right, UP + LEFT))

    def animate_merge(self, left, right, merged):
        left_l, right_r, merged_m = self.setup_animate_merge(
            left, right, merged)

        while left_l.get_value() < len(
                left.values) and right_r.get_value() < len(right.values):
            if left.values[left_l.get_value()] <= right.values[
                    right_r.get_value()]:
                self.animate_merge_element(left, left_l, merged, merged_m)
            else:
                self.animate_merge_element(right, right_r, merged, merged_m)

        while left_l.get_value() < len(left.values):
            self.animate_merge_element(left, left_l, merged, merged_m)

        while right_r.get_value() < len(right.values):
            self.animate_merge_element(right, right_r, merged, merged_m)

        self.cleanup_animate_merge(left, left_l, right, right_r, merged,
                                   merged_m)


# - Why make this movie?
#   - Merge Sort can be confusing for AP students
#     - It's recursive, with a confusingly simplistic base case.
#     - It's not clear where the sorting actually happens.
#       - In other sorts, there's a swap or something else very obvious about moving elements
#         around an array.
# - For AP CS students studying merge sort.
#   - Assumes they have the backgroud necessary: Java basics, arrays, what sorting is, and working on recursion.
# - This is for students who are trying to understand how the merge portion works.
# - See Part 2 for how the recursion works.
#
# TODO: need to credit music to https://www.bensound.com/royalty-free-music/track/summer-chill-relaxed-tropical
class MergeIntro(MergeSortScenes):

    def construct(self):

        # Merge Sort -- Part 1: Merging
        # for AP CS A students working on sorting
        t1 = TextMobject('Merge Sort - Part 1: Merging')
        t1.scale(1.5).to_edge(TOP)
        t2 = TextMobject('\\textit{for AP CS students working on sorting}')
        t2.next_to(t1, DOWN)
        self.play(ShowCreation(t1))
        self.play(FadeInFromDown(t2))
        self.wait(duration=1.5)

        # [1] Building Java Programs: A Back to Basics Approach by Stuart Reges and Marty Stepp.
        # Publisher: Pearson; 5 edition (March 28, 2019) ISBN-10: 013547194X ISBN-13: 978-0135471944
        # Chapter 13, and 13.4 Case Study: Implementing Merge Sort

        self.play(VGroup(t1, t2).shift, UP * 1.5)

        # Focus on:
        # * Where does the sorting happen?
        # * Visualizing the merge
        f1 = TextMobject("We'll focus on just two things:")
        f1.to_edge(
            LEFT)  # Leave room on the right for an animation added in iMovie
        bl = BulletedList('where does the sorting happen?',
                          'visualizing the merge',
                          buff=MED_SMALL_BUFF)
        bl.next_to(f1, DOWN, aligned_edge=LEFT).shift(RIGHT)
        self.play(FadeInFromDown(f1))
        self.wait()
        self.play(FadeInFromDown(bl[0]))
        self.wait()
        self.play(FadeInFromDown(bl[1]))
        self.wait(duration=2)

        q1 = TextMobject(
            'So lets get started with a seemingly simple question...')
        q1.shift(UP)
        self.play(ReplacementTransform(VGroup(*self.mobjects), q1))
        self.wait(duration=2)

        # TODO: keep both on the screen at the same time?
        q2 = TextMobject('Given two sorted arrays can we merge them into one?')
        q2.shift(UP)
        self.play(ReplacementTransform(q1, q2))
        self.wait()


# For a first example, start with a 4+4 merge.
# - Starting with some magically sorted arrays, i.e., in the middle of the problem.
#   - Here you have one job: just merge them into a larger sorted array.
# - So how do we do it?
#   - Make a new array big enough to hold the results
#   - Look at the beginning of each half and pick the smallest item
#   - Move that into the merged array, and advance past the one we picked
#   - Rinse and repeat until we've picked them all
# - This is where the sorting really occurs: in the merge!
#   - It's where the comparison is.
#   - And doing it with two already sorted arrays to make one larger one hopefully shows how
#     this effects a sort.
class MergeFirstExample(MergeSortScenes):

    def construct(self):
        skip_to = 0

        t1 = TextMobject('Given two sorted arrays can we merge them into one?')
        t1.shift(UP)
        # self.play(FadeInFromDown(t1))
        self.add(t1)
        self.wait()

        left = Array([2, 3, 4, 6], element_color=BLUE_D)
        right = Array([1, 3, 7, 8], element_color=LIGHT_BROWN)
        merged = Array([None] * 8)
        halves = VGroup(left, right).arrange(RIGHT, buff=LARGE_BUFF)

        # So, given two sorted arrays of 4 elements each...
        self.play(t1.to_edge, UP, ShowCreation(left), ShowCreation(right))
        self.wait()

        # Each of these are already sorted for us.
        # Someone nice sorted them for us, and for now we'll just accept that and not worry about
        # how they did it.
        if skip_to < 1:
            self.play(
                LaggedStartMap(CircleIndicate,
                               left.elements,
                               run_time=2,
                               lag_ration=0.7))
            self.play(
                LaggedStartMap(CircleIndicate,
                               right.elements,
                               run_time=2,
                               lag_ration=0.7))
            self.wait()

        # So now we have "one job": combine two sorted arrays into one sorted array.
        # To do that, we need space for the result. We'll make an empty array to hold them all.
        merged.shift(UP * 1.5)
        self.play(
            halves.next_to,
            merged,
            DOWN,
            MED_LARGE_BUFF,
            FadeInFromDown(merged),
        )
        self.wait()

        # To do the merge, we need to pick the smallest element from each half, copy it to the
        # result, and then move on.

        # So grab the first from each half, which is the smallest in each since the halves are
        # already sorted.
        self.play(left.shift, LEFT * 2.5, right.shift, RIGHT * 2.5)
        comp = TexMobject('left', '<=', 'right')
        comp.next_to(merged, BOTTOM, SMALL_BUFF)
        self.play(Write(comp))
        self.wait()

        comp_text = TextMobject('left[l]', ' <= ', 'right[r]')
        comp_text.next_to(merged, BOTTOM, SMALL_BUFF)
        code_image_main = ImageMobject('merge_sort/merge_code_main_loop',
                                       height=2.2)
        code_image_main.to_edge(BOTTOM, buff=0.01)
        self.play(ReplacementTransform(comp, comp_text),
                  FadeIn(code_image_main))
        self.wait()

        # So let's add an index for each half, starting at the front of each array to keep track
        # of where we are.
        left_l = left.create_index(0, color=YELLOW, name='l')
        right_r = right.create_index(0, color=YELLOW, name='r')
        self.play(ShowCreation(left_l), ShowCreation(right_r))
        self.wait()

        # And let's add an index to the beginning of the result to keep track of where we're going.
        merged_m = merged.create_index(0, color=YELLOW, name='m', position=UP)
        self.play(
            ShowCreation(merged_m),
            t1.to_edge,
            UP,
            {'buff': SMALL_BUFF},
        )
        self.wait()

        llo = -1
        rro = -1
        while left_l.get_value() < len(
                left.values) and right_r.get_value() < len(right.values):
            self.merge_element_count += 1

            if self.merge_element_count == 3:
                self.play(FadeOut(sort_text))

            ll = left_l.get_value()
            rr = right_r.get_value()
            if ll != llo:
                llo = ll
                lc = left.elements[ll].copy()
            if rr != rro:
                rro = rr
                rc = right.elements[rr].copy()
            if comp_text[0] != lc:
                self.play(lc.move_to,
                          comp_text[0],
                          Uncreate(comp_text[0]),
                          run_time=self.merge_runtime)
                comp_text.submobjects[0] = lc
            if comp_text[2] != rc:
                self.play(rc.move_to,
                          comp_text[2],
                          Uncreate(comp_text[2]),
                          run_time=self.merge_runtime)
                comp_text.submobjects[2] = rc
            self.wait(duration=self.merge_runtime)

            # In the room where it happens...
            if self.merge_element_count == 1:
                sort_text = TextMobject('this is where\\\\the sort happens')
                sort_text.next_to(comp_text, DOWN)
                self.play(FadeInFromDown(sort_text))

            # Highlight dups, and stable sort note and reference when we hit the first dups.
            if left.values[left_l.get_value()] == 3:
                self.merge_runtime = 0.3
                dups_text = TextMobject('dups favor the left!')
                dups_text.next_to(comp_text, DOWN)
                sr = SurroundingRectangle(VGroup(*comp_text))
                self.play(
                    FadeIn(sr),
                    FadeInFromDown(dups_text),
                )
                self.wait()
                self.play(FadeOut(dups_text), FadeOut(sr))

            # Compare them. Show the comparison and circle the smaller one.
            if left.values[left_l.get_value()] <= right.values[
                    right_r.get_value()]:
                self.play(CircleIndicate(lc), run_time=self.merge_runtime)
                # Move the smaller one into place.
                lc = lc.copy()
                self.play(lc.move_to,
                          merged.elements[merged_m.get_value()],
                          run_time=self.merge_runtime)
                merged.elements.submobjects[merged_m.get_value()] = lc
                self.wait(duration=self.merge_runtime)
                self.play(*left_l.animate_set_index(left_l.get_value() + 1),
                          *merged_m.animate_set_index(merged_m.get_value() + 1),
                          run_time=self.merge_runtime)
                self.wait(duration=self.merge_runtime)
            else:
                self.play(CircleIndicate(rc), run_time=self.merge_runtime)
                # Move the smaller one into place.
                rc = rc.copy()
                self.play(rc.move_to,
                          merged.elements[merged_m.get_value()],
                          run_time=self.merge_runtime)
                merged.elements.submobjects[merged_m.get_value()] = rc
                self.wait(duration=self.merge_runtime)
                self.play(*right_r.animate_set_index(right_r.get_value() + 1),
                          *merged_m.animate_set_index(merged_m.get_value() + 1),
                          run_time=self.merge_runtime)
                self.wait(duration=self.merge_runtime)
            if skip_to >= 2:
                break

        # Note on what to do with the last one. No new comparison to make since the left array
        # is complete. Thus we just add the rest on the right, which by def are all a) sorted
        # and b) larger than the last element of left.
        # - Note that only one of the while loops will run, and in this case, it's the second one.
        self.play(
            FadeOutAndShiftDown(code_image_main),
            Uncreate(comp_text),
        )
        self.wait()

        cleanup_text = TextMobject('Left is done,\\\\so finish right...')
        cleanup_text.next_to(merged, BOTTOM, SMALL_BUFF)
        code_image_cleanup = ImageMobject('merge_sort/merge_code_cleanup_loops',
                                          height=2.2)
        code_image_cleanup.to_edge(BOTTOM, buff=0.01)
        self.play(
            FadeInFromDown(cleanup_text),
            FadeInFromDown(code_image_cleanup),
        )
        self.wait()

        self.merge_runtime = 0.5

        while left_l.get_value() < len(left.values):
            self.animate_merge_element(left, left_l, merged, merged_m)
            if skip_to >= 3:
                break

        while right_r.get_value() < len(right.values):
            self.animate_merge_element(right, right_r, merged, merged_m)
            if skip_to >= 3:
                break

        self.play(Uncreate(left_l), Uncreate(right_r), Uncreate(merged_m),
                  Uncreate(cleanup_text))
        left.remove_index(left_l)
        right.remove(right_r)
        merged.remove_index(merged_m)

        # We've successfully merged the arrays into a new one.
        # This is the core of the merge algorithm shown in the book, but rewritten.
        t2 = TextMobject('Merged two arrays of 4 into one array of 8')
        t2.to_edge(UP)
        code_image_full = ImageMobject('merge_sort/merge_code_full', height=4.0)
        code_image_full.scale(1.2)
        code_image_full.to_edge(RIGHT)
        merged.generate_target(use_deepcopy=True)
        merged.target.to_edge(LEFT)
        left.generate_target(use_deepcopy=True)
        right.generate_target(use_deepcopy=True)
        g = VGroup(left.target, right.target).arrange(RIGHT,
                                                      buff=MED_LARGE_BUFF)
        g.next_to(merged.target, DOWN, buff=MED_LARGE_BUFF)

        self.play(
            ReplacementTransform(t1, t2),
            MoveToTarget(merged),
            MoveToTarget(left),
            MoveToTarget(right),
            FadeOutAndShiftDown(code_image_cleanup),
            FadeInFrom(code_image_full, RIGHT),
        )

        code_expl = TextMobject(
            r"\begin{enumerate}"
            r"\item[*]This code is different than what's in the book.\\"
            r"Study both and see which feels better to you!"
            r"\end{enumerate}",
            alignment="")
        code_expl.scale(0.7).next_to(code_image_full, DOWN, aligned_edge=LEFT)
        self.play(FadeInFromDown(code_expl))
        self.wait(duration=3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()


# Stepping back to look at the base case
class MergeBaseCase(MergeSortScenes):

    def construct(self):
        # Okay, so we know how to merge two sorted arrays, but where do we get those from?
        # Well, the simplest case is an array of a single number.
        # It seems a little silly, but it's important.
        #   - Seems like "duh", but it's important.
        # An array size of 1 represents the "base case" for recursive merge sorts.

        t1 = TextMobject(
            'Now we know how to merge\\\\smaller, sorted arrays into larger ones.'
        )
        self.play(FadeInFromDown(t1))
        self.wait(duration=3)

        t2 = TextMobject('But how do we find sorted arrays to merge?')
        self.play(ReplacementTransform(t1, t2))
        self.wait(duration=2)

        t3 = TextMobject('An array of size 1 is already sorted!')
        self.play(ReplacementTransform(t2, t3))
        self.wait()

        colors = [GREEN, YELLOW_D, PINK, BLUE]
        nums = [4, 12, 7]
        all_singles = VGroup(*[
            Array([n], show_labels=False, element_color=c)
            for n, c in zip(nums, colors)
        ])
        all_singles.arrange(RIGHT, buff=LARGE_BUFF * 3)
        all_taglines = VGroup(
            TextMobject('This array is sorted...'),
            TextMobject('... and so is this one...'),
            TextMobject('... and this one.'),
        )
        all_offsets = [UP, ORIGIN, DOWN]
        self.play(
            t3.to_edge,
            UP,
        )
        for a, t, o in zip(all_singles, all_taglines, all_offsets):
            a.shift(o)
            t.next_to(a, DOWN)
            self.play(
                ShowCreation(a),
                Write(t),
            )
        self.wait()

        t4 = TextMobject("Feels like a ``duh'' moment,\\\\but it's important!")
        all_singles[1].generate_target()
        all_singles[1].target.shift(UP)
        t4.next_to(all_singles[1].target, DOWN)
        self.play(
            FadeOut(all_singles[0]),
            FadeOut(all_taglines[0]),
            MoveToTarget(all_singles[1]),
            ReplacementTransform(all_taglines[1], t4),
            FadeOut(all_singles[2]),
            FadeOut(all_taglines[2]),
        )
        self.wait()

        t5 = TextMobject(
            r"This forms the ``\textbf{base case}'' for all merge sorts.",
            tex_to_color_map={'base case': GREEN})
        t5.next_to(t4, DOWN, buff=MED_LARGE_BUFF)
        self.play(Write(t5))
        self.wait(duration=2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()


# Show a small merge
# - Let's look at merging 4 numbers starting at the base case of 4 single-element arrays.
# - Take the first pair, merge it, and place the result someplace where we can find it later.
# - Same for the second pair.
# - Now, take the pair of previous results, and merge them to produce the final result.
class Merge4(MergeSortScenes):

    def construct(self):
        self.merge_runtime = 0.5

        colors = [RED, BLUE, GREEN, YELLOW_D]
        nums = [4, 3, 1, 7]
        all_singles = VGroup(*[
            Array([n], show_labels=False, element_color=c)
            for n, c in zip(nums, colors)
        ])
        all_singles.arrange(RIGHT, buff=0)
        t1 = TextMobject('So start with an array of random numbers...')
        t1.to_edge(TOP)
        self.play(FadeInFromDown(t1), ShowCreation(all_singles))
        self.wait(duration=2)

        t2 = TextMobject('And split it into many 1-element arrays.')
        t2.to_edge(TOP)
        all_singles.generate_target(use_deepcopy=True)
        all_singles.target.arrange(RIGHT, buff=MED_LARGE_BUFF)
        self.play(
            ReplacementTransform(t1, t2),
            MoveToTarget(all_singles),
        )
        self.wait(duration=2)

        level_labels = [
            TextMobject('Base cases'),
            TextMobject('Merged pairs'),
            TextMobject('Final result')
        ]
        self.play(ReplacementTransform(t2, level_labels[0].to_edge(LEFT)))
        self.wait()

        self.play(
            VGroup(all_singles, level_labels[0]).to_edge, BOTTOM,
            {'buff': SMALL_BUFF})
        self.wait()

        current_level = all_singles
        all_levels = [current_level]
        while len(current_level) > 1:
            current_level = self.merge_level(current_level,
                                             0,
                                             buff=MED_LARGE_BUFF,
                                             speedy=True)
            ll = level_labels[len(all_levels)]
            ll.next_to(current_level, LEFT).to_edge(LEFT)
            self.play(Write(ll))
            self.wait()
            all_levels.append(current_level)

        g = VGroup(*all_levels, *level_labels)
        self.play(g.center)
        self.wait(duration=2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()

    def setup_animate_merge(self, left, right, merged):
        show_labels = True
        if self.merge_current_level > 1:
            show_labels = False
        left_l = left.create_index(0,
                                   color=YELLOW,
                                   name='l',
                                   show_label=show_labels)
        right_r = right.create_index(0,
                                     color=YELLOW,
                                     name='r',
                                     show_label=show_labels)
        merged_m = merged.create_index(0,
                                       color=YELLOW,
                                       name='m',
                                       position=UP,
                                       show_label=show_labels)
        self.play(FadeIn(left_l),
                  FadeIn(right_r),
                  FadeIn(merged_m),
                  run_time=0.5)
        return left_l, right_r, merged_m

    def cleanup_animate_merge(self, left, left_l, right, right_r, merged,
                              merged_m):
        left.remove_index(left_l)
        right.remove(right_r)
        merged.remove_index(merged_m)
        self.play(FadeOut(left_l),
                  FadeOut(right_r),
                  FadeOut(merged_m),
                  run_time=0.5)
        self.play(FadeOutAndShift(left, UP + RIGHT),
                  FadeOutAndShift(right, UP + LEFT))


# Now show the big merge
# - A bigger set of numbers requires more levels of merging.
# - There's an odd number, so the first time when we take pairs the one on the end is left over.
#   - It's still sorted, so we just bring it along to the next level for free.
# - On the next level, the last pair is combined with the single leftover from the last level.
# - On the next level, the last array of three is left over, so we bring it to the next level again.
# - Etc, until the entire set is merged.
class Merge11(MergeSortScenes):

    def __init__(self, **kwargs):
        self.runtime_stack = []
        self.level_element_count = 0
        MergeSortScenes.__init__(self, **kwargs)

    def construct(self):
        n = 11

        t1 = TextMobject(
            "Let's do a bigger merge, with an odd number of elements")
        self.play(FadeInFromDown(t1))
        self.wait()

        np.random.seed(42)
        colors = color_gradient([PINK, BLUE, YELLOW_D], 20)
        all_singles = VGroup(*[
            Array([n], show_labels=False, element_color=colors[n])
            for i, n in enumerate(np.random.randint(0, 20, n))
        ])
        all_singles.arrange(RIGHT, buff=MED_SMALL_BUFF)
        t2 = TextMobject(str(n) + " numbers...")
        t2.next_to(all_singles, UP, buff=MED_LARGE_BUFF)
        self.play(FadeOutAndShift(t1, UP))
        self.play(ShowCreation(all_singles), FadeIn(t2))
        self.wait()

        b = BraceLabel(VGroup(*all_singles[-3:]),
                       'Watch the last 3',
                       brace_direction=UP,
                       label_constructor=TextMobject)
        self.play(ShowCreation(b), FadeOutAndShift(t2, UP))
        self.wait()

        self.play(
            all_singles.to_edge,
            BOTTOM,
            {'buff': MED_SMALL_BUFF},
            # FadeOutAndShift(t2, UP),
            FadeOutAndShift(b, UP))
        self.wait()

        current_level = all_singles
        all_levels = [current_level]
        squish_start_height = 14  # 4
        level_runtimes = [0.25, 0.25, 0.25, 0.25, 0.25]
        while len(current_level) > 1:
            if len(all_levels) == squish_start_height:
                g = VGroup(*all_levels[:-1])
                self.play(g.scale, 0.8, g.to_edge, BOTTOM, {'buff': SMALL_BUFF})
                self.play(all_levels[-1].next_to, all_levels[-2], UP,
                          {'buff': MED_SMALL_BUFF})
            if len(all_levels) > squish_start_height:
                self.play(all_levels[-2].scale, 0.8, all_levels[-2].next_to,
                          all_levels[-3], UP, {'buff': SMALL_BUFF})
                self.play(all_levels[-1].next_to, all_levels[-2], UP,
                          {'buff': SMALL_BUFF})

            self.level_element_count = 0
            self.merge_runtime = level_runtimes[self.merge_current_level]
            current_level = self.merge_level(current_level,
                                             len(all_levels),
                                             buff=MED_SMALL_BUFF,
                                             speedy=True)
            all_levels.append(current_level)

        merge_result = VGroup(*all_levels)
        self.play(merge_result.center)
        self.wait(duration=2)

        # In closing
        rt = TextMobject('Merge Sort - Part 1: Merging')
        rt.scale(1.5).to_edge(UP, buff=MED_SMALL_BUFF)

        one_element_array = all_levels[0][0]
        one_element_array.generate_target(use_deepcopy=True)
        oea_t = TextMobject('A one element array\\\\is sorted')
        oea_t.next_to(one_element_array.target, DOWN)
        oea_g = VGroup(one_element_array.target, oea_t)
        oea_g.next_to(rt, DOWN, buff=MED_LARGE_BUFF).to_edge(LEFT)

        two_to_four = VGroup(
            all_levels[1][0],
            all_levels[1][1],
            all_levels[2][0],
        )
        two_to_four.generate_target(use_deepcopy=True)
        ttf_t = TextMobject('Sorting happens while merging')
        ttf_t.next_to(two_to_four.target, DOWN)
        ttf_g = VGroup(two_to_four.target, ttf_t)
        ttf_g.next_to(rt, DOWN, buff=MED_LARGE_BUFF).to_edge(RIGHT)

        dups_from_left = VGroup(
            all_levels[3][0],
            all_levels[3][1],
            all_levels[4][0],
        )
        dups_from_left.generate_target(use_deepcopy=True)
        right_dup_fill_color = YELLOW
        dup_opacity = 0.2
        dups_from_left.target[1].backgrounds[1].set_fill(
            right_dup_fill_color, dup_opacity)
        dups_from_left.target[1].backgrounds[2].set_fill(
            right_dup_fill_color, dup_opacity)
        dups_from_left.target[2].backgrounds[4].set_fill(
            right_dup_fill_color, dup_opacity)
        dups_from_left.target[2].backgrounds[7].set_fill(
            right_dup_fill_color, dup_opacity)

        dfl_t = TextMobject(
            "Duplicates favor the left - merge sort is ``stable''")
        dfl_t.next_to(dups_from_left.target, DOWN)
        dfl_g = VGroup(dups_from_left.target, dfl_t)
        dfl_g.next_to(VGroup(oea_g, ttf_g), DOWN, buff=LARGE_BUFF)

        self.play(
            FadeOut(merge_result),
            FadeInFromDown(rt),
            FadeInFromDown(oea_g),
            FadeInFromDown(ttf_g),
            FadeInFromDown(dfl_g),
        )

        # self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()

    def setup_animate_merge(self, left, right, merged):
        left_l = left.create_index(0, color=YELLOW, name='l', show_label=False)
        right_r = right.create_index(0,
                                     color=YELLOW,
                                     name='r',
                                     show_label=False)
        merged_m = merged.create_index(0,
                                       color=YELLOW,
                                       name='m',
                                       position=UP,
                                       show_label=False)
        # self.play(FadeIn(left_l), FadeIn(right_r), FadeIn(merged_m),
        #           run_time=0.5)
        self.add(left_l, right_r, merged_m)
        return left_l, right_r, merged_m

    def cleanup_animate_merge(self, left, left_l, right, right_r, merged,
                              merged_m):
        left.remove_index(left_l)
        right.remove(right_r)
        merged.remove_index(merged_m)
        self.play(FadeOut(left_l),
                  FadeOut(right_r),
                  FadeOut(merged_m),
                  FadeOutAndShift(left, UP + RIGHT),
                  FadeOutAndShift(right, UP + LEFT),
                  run_time=self.merge_runtime)

    def merge_level_pair_begin(self, index):
        if self.level_element_count == 0:
            self.runtime_stack.append(self.merge_runtime)
            # self.merge_runtime *= 2

    def merge_level_pair_end(self, index):
        if self.level_element_count == 0:
            self.merge_runtime = self.runtime_stack.pop()
        self.level_element_count += 1
        self.merge_runtime *= 0.95

    def merge_level_extra_begin(self, index, extra):
        self.wait(duration=0.5)
        self.runtime_stack.append(self.merge_runtime)
        self.merge_runtime = 1
        self.play(ShowPassingFlashAround(extra))

        if self.merge_current_level == 1 or self.merge_current_level == 3:
            if self.merge_current_level == 1:
                pt = TextMobject('promote any\\\\un-paired array')
            else:
                pt = TextMobject('again, promote the\\\\un-paired array')
                pt.shift(UP * 2)
            pt.to_edge(RIGHT, buff=MED_SMALL_BUFF)
            a = Arrow(pt.get_bottom(), extra.get_top())
            self.play(FadeIn(pt), ShowCreation(a))
            self.wait()
            self.play(FadeOut(pt), FadeOut(a))

    def merge_level_extra_end(self, index, extra):
        # self.play(ShowPassingFlashAround(extra))
        # self.wait()
        self.merge_runtime = self.runtime_stack.pop()


class MergeNSpeedyClean(MergeSortScenes):

    def __init__(self, **kwargs):
        MergeSortScenes.__init__(self, **kwargs)

    def construct(self):
        n = 9
        np.random.seed(41)
        colors = color_gradient([PINK, BLUE, YELLOW_D], 20)
        all_singles = VGroup(*[
            Array([n], show_labels=False, element_color=colors[n])
            for i, n in enumerate(np.random.randint(0, 20, n))
        ])
        all_singles.arrange(RIGHT, buff=MED_SMALL_BUFF)
        all_singles.to_edge(BOTTOM, buff=SMALL_BUFF)
        self.play(ShowCreation(all_singles))

        current_level = all_singles
        all_levels = [current_level]
        self.merge_runtime = 0.5
        while len(current_level) > 1:
            current_level = self.merge_level(current_level,
                                             len(all_levels),
                                             buff=MED_SMALL_BUFF,
                                             speedy=True)
            all_levels.append(current_level)

        self.wait(duration=2)

    def setup_animate_merge(self, left, right, merged):
        left_l = left.create_index(0, color=YELLOW, show_label=False)
        right_r = right.create_index(0, color=YELLOW, show_label=False)
        merged_m = merged.create_index(0, color=YELLOW, show_label=False)
        self.add(left_l, right_r, merged_m)
        return left_l, right_r, merged_m

    def cleanup_animate_merge(self, left, left_l, right, right_r, merged,
                              merged_m):
        left.remove_index(left_l)
        right.remove(right_r)
        merged.remove_index(merged_m)
        self.play(FadeOut(left_l),
                  FadeOut(right_r),
                  FadeOut(merged_m),
                  FadeOutAndShift(left, UP + RIGHT),
                  FadeOutAndShift(right, UP + LEFT),
                  run_time=self.merge_runtime)


# Part 2

# So given an array of things to sort, how do we break it down into base cases we can merge?
# - Divide and Conquer technique! Merge Sort is a classic example.
#   - If you don't know how to solve a problem, but if you split it up and someone magically solves
#     the pieces, can you reform the pieces into a solution?
#   - If you can, then you've got a divide and conquer problem.
# - We've already learned that we can take two sorted arrays and merge them into a final sorted solution.
# - And we know that the base case is arrays of a single element.
# class MergeDivideAndConquer(MergeSortScenes):
#     def construct(self):
#         pass

# All together, the final algorithm
# - Start with a full array, and recurse down dividing it up.
# - We we hit the base case, return and start merges.
# - We re-use the space from the original we split on the way down.
# - Show this as the full array, then split it and slide the halves apart. Repeat.
# - Show this working as DFS. Leave the old parts in place, and the freshly sorted ones too.
# - This should be a down-then-up motion. To illustrate the "down and back" or "out and back"
#    or "call and return" of recursion.
# class MergeFull(MergeSortScenes):
#     def construct(self):
#         pass

# Consider: merge sorting as a streaming example
# - What if you were given two infinite streams of sorted data?
# - Show this as streams shifting in and out.
# - Weird because one stream could be stalled for a very long time!
# - Is this just a bad example?
# class MergeStreaming(MergeSortScenes):
#     def construct(self):
#         pass
