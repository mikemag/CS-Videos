from manimlib.imports import *


class ArrayIndex(VGroup):
    """
    Visualization of an array index.

    Includes a highlighting rectangle for the array element, and option pointer and label
    with index value.
    """

    CONFIG = {
        'wdith': 1,
        'height': 1,
        'name': 'i',
        'color': BLUE,
        'opacity': 0.75,
        'position': DOWN,
        'show_arrow': True,
        'show_label': True,
    }

    def __init__(self, parent, value, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)
        self.parent = parent
        self.index_tracker = ValueTracker(value)
        self.indicator_box = self.add_indicator_box()
        if self.show_label:
            self.label = always_redraw(lambda: self.get_label())
        else:
            self.label = None
            self.show_arrow = False  # No arrow without label
        if self.show_arrow:
            self.arrow = always_redraw(lambda: self.get_arrow())
        else:
            self.arrow = None
        self.add(*remove_nones([self.label, self.arrow, self.indicator_box]))

    def add_indicator_box(self):
        box = Rectangle(width=self.width - 0.1, height=self.height - 0.1)
        box.set_stroke(color=self.color,
                       opacity=self.get_box_opacity(self.get_value()))
        box.move_to(self.get_box_target(self.get_value()))
        return box

    def get_label(self):
        i = int(round(self.index_tracker.get_value(), 0))
        ni = TextMobject(self.name + '=' + str(i))
        ni.next_to(self.indicator_box, self.position, LARGE_BUFF)
        return ni

    def get_arrow(self):
        if self.label.get_y() < self.indicator_box.get_y():
            a = Arrow(self.label.get_top(),
                      self.indicator_box.get_bottom(),
                      buff=MED_SMALL_BUFF)
        else:
            a = Arrow(self.label.get_bottom(),
                      self.indicator_box.get_top(),
                      buff=MED_SMALL_BUFF)
        return a

    def set_index(self, value):
        self.indicator_box.set_stroke(opacity=self.get_box_opacity(value))
        self.indicator_box.move_to(self.get_box_target(value))
        self.index_tracker.set_value(value)
        return self

    def get_box_target(self, value):
        if value < 0:
            fpe_o = self.parent.elements[0].get_critical_point(ORIGIN)
            return fpe_o + LEFT * self.width
        elif value < len(self.parent.elements):
            return self.parent.elements[value].get_critical_point(ORIGIN)
        else:
            lpe_o = self.parent.elements[-1].get_critical_point(ORIGIN)
            return lpe_o + RIGHT * self.width

    def get_box_opacity(self, value):
        if 0 <= value < len(self.parent.elements):
            return self.opacity
        else:
            return 0.5

    def animate_set_index(self, value):
        return [
            self.indicator_box.set_stroke,
            {
                'opacity': self.get_box_opacity(value),
                'family': False
            },
            self.indicator_box.move_to,
            self.get_box_target(value),
            self.index_tracker.set_value,
            value,
        ]

    def get_value(self):
        return int(self.index_tracker.get_value())


class Array(VGroup):
    """
    Visualization of an array wwith elements, an outline, and optional multiple indices.
    """

    CONFIG = {
        'element_width': 0.6,
        'element_height': 0.6,
        'element_color': WHITE,
        'show_labels': True,
        'labels_scale': 0.5,
    }

    def __init__(self, values, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)

        self.values = values
        self.indicies = {}

        self.total_width = self.element_width * len(self.values)
        self.hw = self.element_width / 2
        self.hh = self.element_height / 2
        self.left_element_offset = (self.total_width / 2) - self.hw
        self.left_edge_offset = self.left_element_offset + self.hw

        # Add the outline of the array.
        self.add(self.create_bounding_box())

        # Add separators between the elements
        separators = VGroup()
        for i in range(1, len(self.values)):
            x = i * self.element_width
            separators.add(
                Line([x, -self.hh, 0], [x, self.hh, 0], stroke_width=2))
        separators.shift(LEFT * self.left_edge_offset)
        self.add(separators)

        # Add each element as a string, in order, spaced accordingly.
        self.elements = VGroup()
        self.backgrounds = VGroup()
        for i, v in enumerate(values):
            if v is not None:
                t = TextMobject(str(v))
            else:
                t = TexMobject('.', width=0, height=0, color=BLACK)
            t.move_to(i * RIGHT * self.element_width)
            self.elements.add(t)
            b = Rectangle(width=self.element_width - 0.1,
                          height=self.element_height - 0.1)
            b.set_stroke(color=BLACK, opacity=0)
            b.move_to(t.get_center())
            self.backgrounds.add(b)
        self.backgrounds.shift(LEFT * self.left_element_offset)
        self.add(self.backgrounds)
        self.elements.shift(LEFT * self.left_element_offset)
        self.elements.set_color(self.element_color)
        self.add(self.elements)

        # Add labels for the array, centered under each element.
        if self.show_labels:
            self.labels = VGroup()
            for i in range(len(self.values)):
                label = TextMobject(str(i)).scale(self.labels_scale)
                label.move_to((i * RIGHT * self.element_width) +
                              (UP * self.element_height * 0.8))
                self.labels.add(label)
            self.labels.shift(LEFT * self.left_element_offset)
            self.add(self.labels)

    def create_bounding_box(self):
        return Rectangle(width=self.total_width,
                         height=self.element_height,
                         stroke_width=2)

    def create_index(self, value, **kwargs):
        i = ArrayIndex(self,
                       value,
                       width=self.element_width,
                       height=self.element_height,
                       **kwargs)
        self.add(i)
        return i

    def remove_index(self, index):
        self.remove(index)

    def hide_labels(self):
        self.show_labels = False
        self.remove(self.labels)
