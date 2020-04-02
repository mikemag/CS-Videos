from manimlib.imports import *


class StackFrame(VGroup):
    """
    Visual representation of a stack frame.

    Includes function name and curent line, and slots for each variable.
    """

    CONFIG = {
        'text_scale': 0.75,
        'width': 2,
    }

    def __init__(self, name, line, vars, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)

        em = TextMobject('M').scale(self.text_scale)
        self.slot_height = em.get_height() + SMALL_BUFF * 2
        self.slot_width = em.get_width() * 5 + SMALL_BUFF * 2

        slots = VGroup()
        self.slot_map = {}
        for i, v in enumerate(vars):
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
        frame_name = TextMobject(name + ' line: ', str(line)) \
            .scale(self.text_scale).next_to(slots, UP, buff=SMALL_BUFF)
        self.add(slots, frame_name)
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

    def set_line(self, line):
        t = self.header_line()[1]
        t.become(TextMobject(str(line)).scale(self.text_scale).move_to(t))
        return self

    def update_slot(self, var_name, val):
        si = self.slot_map[var_name]
        s = self.slots()[si]
        s[2].become(TextMobject(str(val)).scale(self.text_scale).move_to(s[2]))
        return self
