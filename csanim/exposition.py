import inspect
from collections import defaultdict

from manimlib.imports import *

# This is used to add exposition and annotations to other animations,
# like stepping through code while updating data structures. Subclasses of
# this can define hooks into the other animations and get callbacks where
# they can do more animations immediately, or add deferred animations to be
# merged with the regular animations.
#
# Merge Sort Part II shows two examples of this so far.
#
# TODO: make a good demo scene of using this.


class BasilExposition:

    def __init__(self, scene, show_clock=False):
        self.scene = scene
        self.time = 0
        self.run_time = 1.0
        self.anims_by_time = defaultdict(list)
        self.waits_by_time = {}
        self.expl_counters = defaultdict(int)

        if show_clock:
            self.clock = self._get_clock_text(0)
            scene.add(self.clock)
        else:
            self.clock = None

    @staticmethod
    def _get_clock_text(time):
        return TextMobject(str(time)).scale(0.5).to_edge(UL, buff=SMALL_BUFF)

    def _tick(self):
        self.time += 1

    def _consume_deferred_anims(self):
        a = []
        run_time = 0
        if self.time in self.anims_by_time:
            for anims, rt in self.anims_by_time[self.time]:
                a.extend(anims)
                run_time = max(run_time, rt)
        return a, run_time

    # To play an animation as part of code execution. This will tick the
    # exposition clock and include any deferred animations. It may also delay
    # as appropriate.
    def play(self, *anims, run_time=0):
        if self.clock is not None:
            new_clock = self._get_clock_text(self.time + 1)
            self.deferred_play_next(ReplacementTransform(self.clock, new_clock))
            self.clock = new_clock

        self._tick()
        deferred_anims, max_deferred_run_time = self._consume_deferred_anims()
        run_time = max(max_deferred_run_time, self.run_time)
        self.scene.play(*anims, *deferred_anims, run_time=run_time)
        if self.time in self.waits_by_time:
            self.scene.wait(duration=self.waits_by_time[self.time])

    # Convenience wrapper
    def wait(self, duration=DEFAULT_WAIT_TIME):
        self.scene.wait(duration=duration)

    # For everything you can figure out ahead of time. Like static text
    # explaining a step in the code, and even highlights and pointers to
    # things with a predictable place. These are merged with other animations.
    def deferred_play(self, time, *anims, run_time=0):
        self.anims_by_time[time].append(([*anims], run_time))

    def deferred_play_next(self, *anims, **kwargs):
        self.deferred_play(self.time + 1, *anims, **kwargs)

    def deferred_wait(self, time, duration=DEFAULT_WAIT_TIME):
        if time in self.waits_by_time:
            raise Exception("Redundant wait added at time " + str(time))
        self.waits_by_time[time] = duration

    # For things that need to "stop and explain" an ongoing sequence. These
    # can play and delay multiple animations that aren't part of another
    # animation in the normal sequence.
    #
    # A callback method is provided which receives a count of the number of
    # times it has been called, and any other named args passed through.
    def explain(self, method, **kwargs):
        caller_frame = inspect.stack()[1]
        self.expl_counters[caller_frame.lineno] += 1
        method(self.scene, self.expl_counters[caller_frame.lineno], **kwargs)
