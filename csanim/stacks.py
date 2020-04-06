from manimlib.imports import *


class StackFrame(VGroup):
    """
    Visual representation of a stack frame.

    Includes function name and curent line, and slots for each variable.
    """

    CONFIG = {
        'text_scale': 0.75,
        'width': 2,
        'slot_char_width': 5,
    }

    def __init__(self, code, func_label, line, args_and_vars, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)

        self.line = line
        self.code = code

        em = TextMobject('M').scale(self.text_scale)
        self.slot_height = em.get_height() + SMALL_BUFF * 2
        self.slot_width = em.get_width() * self.slot_char_width + SMALL_BUFF * 2

        slots = VGroup()
        self.slot_map = {}
        for i, v in enumerate(args_and_vars):
            if isinstance(v, str):
                vn = v
                vv = '-'
            elif isinstance(v, tuple):
                vn, vv = v
            else:
                vn = str(v)
                vv = '-'
            s = self.build_stack_slot(vn, vv)
            slots.add(s)
            self.slot_map[vn] = i  # Can't remember slot objs because they may change over time
        slots.arrange(DOWN, center=False, buff=0, aligned_edge=RIGHT)
        func_label = TextMobject(func_label + ' line: ', str(line + self.code.line_offset)) \
            .scale(self.text_scale).next_to(slots, UP, buff=SMALL_BUFF)
        self.add(slots, func_label)
        self.center()
        backbone = Line().set_opacity(0).set_width(self.width)
        self.add(backbone)
        br = BackgroundRectangle(self, buff=SMALL_BUFF, fill_opacity=0.15)
        # This fill used ot have an opacity gradient, opacity=[0.1, 0.2], but it caused noticalbe
        # banding in the final gradient. Shame, it was cool otherwise.
        br.set_fill(color=[ORANGE, BLUE])
        self.add(br)

    def build_stack_slot(self, name, value):
        var_name = TextMobject(name).scale(self.text_scale)
        slot_box = Rectangle(height=self.slot_height, width=self.slot_width, stroke_width=1)
        if isinstance(value, Mobject):
            var_value = value
        else:
            var_value = TextMobject(str(value)).scale(self.text_scale)
        var_value.move_to(slot_box)
        var_name.next_to(slot_box, LEFT)
        stack_slot = VGroup(slot_box, var_name, var_value)
        return stack_slot

    def slots(self):
        return self[0]

    def header_line(self):
        return self[1]

    def background_rect(self):
        return self[3]

    def set_line(self, line):
        t = self.header_line()[1]
        t.become(TextMobject(str(line + self.code.line_offset)).scale(self.text_scale).move_to(t))
        self.line = line
        return self

    def update_slot(self, var_name, val):
        si = self.slot_map[var_name]
        s = self.slots()[si]
        s[2].become(TextMobject(str(val)).scale(self.text_scale).move_to(s[2]))
        return self

    def align_data(self, mobject):
        # This ensures that after a transform our data fields get updated.
        # So far, only line can change with a transform.
        super().align_data(mobject)
        if isinstance(mobject, StackFrame):
            self.line = mobject.line

    def get_update_line_anims(self, line):
        # TODO: This is a mess. We need to return the set_line method as the last entry so we can
        # have auto-merge with update_slot calls in the play() that call this. That's not so bad,
        # but not great. Worse, though, is that the AnimationGroup should be unnecessary!
        # There is something I've missed wrt the frame holding the code, and when copies are
        # made during animation. Possibly my copy/align_data impls are wrong. Need to dig in more.
        return [
            AnimationGroup(
                ApplyMethod(self.code.highlight_lines, line),
            ),
            self.set_line, line,
        ]


class CallStack(VGroup):
    def animate_call(self, new_frame, scene):
        extra_anims = []
        if len(self) > 2:
            extra_anims.append(ApplyMethod(
                self.shift,
                DOWN * new_frame.get_height() + DOWN * SMALL_BUFF
            ))
        new_frame.next_to(self[-1], UP, buff=SMALL_BUFF)
        prev_code = self[-1].code
        if prev_code != new_frame.code:
            hr_caller, hr_callee = prev_code.setup_for_call(new_frame.code, 1)
            scene.play(
                *extra_anims,
                prev_code.highlight_caller,
                ReplacementTransform(hr_caller, hr_callee, path_arc=-np.pi),
                FadeInFrom(new_frame, UP),
                MaintainPositionRelativeTo(new_frame, self[-1]),
            )
            new_frame.code.complete_callee(hr_callee, self)
        else:
            scene.play(
                *extra_anims,
                new_frame.code.highlight_lines, 1,
                FadeInFrom(new_frame, UP),
                MaintainPositionRelativeTo(new_frame, self[-1]),
            )
        self.add(new_frame)

    def animate_return(self, scene):
        current_frame = self[-1]
        self.remove(current_frame)
        anim_stack_shift = []
        if len(self) > 2:
            anim_stack_shift.append(ApplyMethod(
                self.shift,
                UP * current_frame.get_height() + UP * SMALL_BUFF
            ))
        caller_frame = self[-1]
        if caller_frame.code != current_frame.code:
            hr_returner, hr_returnee = current_frame.code.setup_for_return(caller_frame.code)
            scene.play(
                ReplacementTransform(hr_returner, hr_returnee, path_arc=np.pi),
                caller_frame.code.highlight_returnee,
                FadeOutAndShift(current_frame, UP),
            )
            caller_frame.code.complete_returnee(hr_returnee, self)
        else:
            scene.play(
                *anim_stack_shift,
                FadeOutAndShift(current_frame, UP),
                caller_frame.code.highlight_lines, caller_frame.line,
            )
