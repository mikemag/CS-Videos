from manimlib.imports import *

import pygments.lexers
from pygments.formatters import LatexFormatter


class LevelRect(Rectangle):
    """
    A standard Rectangle that stays level when it's transformed.
    """

    def interpolate(self, mobject1, mobject2, alpha, path_func=straight_path):
        # Interpolate along a straight path for the change in the rect's size
        self.points = straight_path(mobject1.points, mobject2.points, alpha)

        # Now use the real path_func to figure out where we should be.
        if path_func is not straight_path:
            # c = path_func(mobject1.get_center(), mobject2.get_center(), alpha)
            # self.move_to(c)
            c = path_func(mobject1.get_left(), mobject2.get_left(), alpha)
            self.move_to(c, aligned_edge=LEFT)

        self.interpolate_color(mobject1, mobject2, alpha)
        return self


# NB: requires the mods to SVGMobject to respect fill colors.
class CodeTextString(SingleStringTexMobject):
    """
    A snippet of code in a given language, possibly multiple lines.

    The code will be formatted with Pygments based on the language given.
    Each line is split apart and available using normal indexing.

    Supports getting highlighting rectangles for lines or groups of lines.
    """

    CONFIG = {
        'alignment': '',
        # TODO: could use a different template, or generate it once given a
        #  Pygments style. - Also, can get the extra style code from
        #  LatexFormatter().get_style_defs()
        'template_tex_file_body': TEMPLATE_TEXT_FILE_BODY,
        'arg_separator': '',

        # Delta in y to determine line breaks from the SVG
        'line_tolerance': 0.2,
    }

    def __init__(self, language, raw_code_string, **kwargs):
        digest_config(self, kwargs, locals())
        lexer = pygments.lexers.get_lexer_by_name(language)
        code = pygments.highlight(raw_code_string, lexer, LatexFormatter())
        super().__init__(code, **kwargs)
        self.raw_code_string = raw_code_string
        self.latex_code_string = code

        # The original LaTeX string has newlines in it, which makes it easy
        # to separate. The first and last lines are boilerplate from
        # Pygments, so discard them.
        self.tex_strings = self.latex_code_string.splitlines()
        self.tex_strings = self.tex_strings[1:-1]

        # If the last line is empty it's okay, just trim it off too.
        if len(self.tex_strings[-1].strip()) == 0:
            self.tex_strings = self.tex_strings[:-1]

        self.break_up_by_lines()

    # Pygments has full control over the generated TeX, so let's not muck
    # with it!
    def modify_special_strings(self, tex):
        return tex

    # Pick apart the code into individual lines, with the string that
    # generated them. This is much like TexMobject.break_up_by_substrings().
    # TODO: doesn't handle blank lines in the middle of the source...
    def break_up_by_lines(self):
        # The submobjects have no association with the original input,
        # but they do have x,y coords. So we can break lines by changes in Y.
        # The lines are presented in-order in the SVG, too.
        new_submobjects = []
        current_line_y = self.submobjects[0].get_center(
        )[1] - self.line_tolerance * 2
        line_group = None

        for o in self.submobjects:
            y = o.get_center()[1]
            if abs(y - current_line_y) > self.line_tolerance:
                if line_group:
                    new_submobjects.append(line_group)
                current_line_y = y
                line_group = VGroup()
            line_group.add(o)

        new_submobjects.append(line_group)  # Pickup the last group

        if len(new_submobjects) != len(self.tex_strings):
            warnings.warn(
                '%s: split SVG into %d lines, but there are %d lines in the '
                'original LaTeX from Pygments! See %s' %
                (self.name, len(new_submobjects), len(
                    self.tex_strings), self.file_path))
        self.submobjects = new_submobjects
        return self

    # The SVG is nicely colored for us, so don't try to adjust it further
    # after we've gone to all the work to import those colors from the SVG.
    # TODO: factor this better with the superclass.
    def init_colors(self):
        self.set_fill(
            # color=self.fill_color or self.color,
            opacity=self.fill_opacity,)
        self.set_stroke(
            # color=self.stroke_color or self.color,
            width=self.stroke_width,
            opacity=self.stroke_opacity,
        )
        self.set_background_stroke(
            color=self.background_stroke_color,
            width=self.background_stroke_width,
            opacity=self.background_stroke_opacity,
        )
        self.set_sheen(
            factor=self.sheen_factor,
            direction=self.sheen_direction,
        )
        return self

    def get_lines(self, lines):
        """
        Line numbers start at 1
        """
        if isinstance(lines, tuple):
            return self[lines[0] - 1:lines[1] - 1]
        else:
            return self[lines - 1]

    def get_lines_highlight_rect(self, lines, color=YELLOW, buff=SMALL_BUFF):
        code_lines = VGroup(self.get_lines(lines))
        left_x = self.get_left()[0]
        right_x = code_lines.get_right()[0]

        r = LevelRect(
            width=right_x - left_x + 2 * buff,
            height=code_lines.get_height() + 2 * buff,
            stroke_width=0,
            stroke_opacity=0,
            fill_color=color,
            fill_opacity=0.2,
            corner_radius=0.1,
        )
        r.move_to(code_lines, aligned_edge=RIGHT).shift(RIGHT * buff)
        return r


# TODO: delete soon
class CodeBlockOld(VGroup):
    """
    A block of code with line highlighting.

    Hold a (possibly multiline) snippet of code in a given language,
    with support for highlighting lines and stepping between them, animating
    the highlight.
    """

    CONFIG = {
        'height': 1,
    }

    def __init__(self, language, raw_code_string, line_offset=0, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)
        self.callsite_highlight = None
        self.line_offset = line_offset
        code_string = CodeTextString(language, raw_code_string)
        highlight_rect = code_string.get_line_highlight_rect(1).set_opacity(0)
        hrg = VGroup(highlight_rect)
        self.add(code_string, hrg)

    def code_string(self):
        return self[0]

    def __highlight_rect_group(self):
        return self[1]

    def highlight_rect(self):
        return self.__highlight_rect_group()[0]

    def highlight_lines(self, lines, color=YELLOW):
        r = self.code_string().get_line_highlight_rect(lines, color=color)
        self.highlight_rect().become(r)
        return self

    def fade_out_highlight(self):
        self.highlight_rect().set_opacity(0)

    # Move it without changing it
    def move_highlight_rect(self, line):
        self.highlight_rect().move_to(
            self.code_string().get_line_highlight_rect(line))

    # Returns a from and to highlight rect, each of which are independent of
    # the code block
    def setup_for_call(self, callee, lines):
        hr_from = self.highlight_rect().copy()
        self.callsite_highlight = self.highlight_rect().copy().set_color(WHITE)
        self.highlight_rect().set_opacity(0)
        hr_to = callee.code_string().get_line_highlight_rect(lines)
        return hr_from, hr_to

    def highlight_caller(self):
        self.highlight_rect().become(self.callsite_highlight)

    def complete_callee(self, hr, scene):
        scene.remove(hr)
        self.__highlight_rect_group().remove(self.highlight_rect())
        self.__highlight_rect_group().add(hr)

    # Returns a from and to highlight rect, each of which are independent of the code block
    def setup_for_return(self, returnee):
        hr_to = returnee.highlight_rect().copy().set_color(YELLOW)
        hr_from = self.highlight_rect().copy()
        self.__highlight_rect_group().remove(self.highlight_rect())
        self.__highlight_rect_group().add(
            self.code_string().get_line_highlight_rect(1).set_opacity(0))
        return hr_from, hr_to

    def highlight_returnee(self):
        self.highlight_rect().set_opacity(0)

    def complete_returnee(self, hr, scene):
        scene.remove(hr)
        self.__highlight_rect_group().remove(self.highlight_rect())
        self.__highlight_rect_group().add(hr)


class CodeBlock(VGroup):
    """
    A block of code with line highlighting.

    Hold a (possibly multiline) snippet of code in a given language,
    with support for highlighting lines and stepping between them, animating
    the highlight.
    """

    CONFIG = {
        'code_scale': 0.75,
        'add_labels': False,
        'label_color': GREY,
        'label_scale': 0.4,
        'annotation_color': BLUE,
        'annotation_scale': 0.6,
        'annotation_buff': MED_LARGE_BUFF,
    }

    def __init__(self, language, raw_code_string, line_offset=0, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)
        code_string = CodeTextString(language, raw_code_string)
        code_string.scale(self.code_scale)
        self.add(code_string)  # Index 0

        if isinstance(line_offset, CodeBlock):
            self.line_offset = len(line_offset.get_code().tex_strings)
        else:
            self.line_offset = line_offset

        if self.add_labels:
            labels = VGroup()
            for n in range(len(code_string.tex_strings)):
                l = TexMobject(str(n + 1 + self.line_offset),
                               color=self.label_color).scale(self.label_scale)
                loc = code_string.get_lines(n + 1)
                l.next_to(loc[0][0], LEFT).next_to(code_string,
                                                   LEFT,
                                                   coor_mask=X_AXIS)
                labels.add(l)
            self.add(labels)  # Index 1

        self.highlighted_lines = 1 + line_offset
        hr = self._get_hidden_highlight(self.highlighted_lines)
        self.add(hr)
        self.hr_index = self.submobjects.index(hr)

        self.annotation_indexes = {}

    def _get_hidden_highlight(self, lines):
        r = self.get_code().get_lines_highlight_rect(
            self._adjusted_lines(lines), buff=0.0).set_opacity(0.0)
        return r

    def align_data(self, other):
        # This ensures that after a transform our data fields get updated.
        super().align_data(other)
        if isinstance(other, CodeBlock):
            self.line_offset = other.line_offset
            self.hr_index = other.hr_index
            self.highlighted_lines = other.highlighted_lines
            self.annotation_indexes = other.annotation_indexes

    def _tracked_remove(self, mob):
        """
        Whenever we remove something from self we have to re-index things
        like annotations and highlight rects.
        """
        mi = self.submobjects.index(mob)
        self.remove(mob)

        def adjusted_index(i):
            return i if i < mi else i - 1

        self.hr_index = adjusted_index(self.hr_index)
        for line, index in self.annotation_indexes.items():
            self.annotation_indexes[line] = adjusted_index(index)

    def get_code(self):
        return self[0]

    def get_labels(self):
        if self.add_labels:
            return self[1]
        return None

    def get_current_highlight(self):
        return self[self.hr_index]

    def get_highlighted_lines(self):
        return self.highlighted_lines

    def _adjusted_lines(self, lines):
        if isinstance(lines, tuple):
            return lines[0] - self.line_offset, lines[1] - self.line_offset
        else:
            return lines - self.line_offset

    def get_lines(self, lines):
        return self.get_code().get_lines(self._adjusted_lines(lines))

    def highlight_lines(self, lines, color=YELLOW):
        r = self.get_code().get_lines_highlight_rect(
            self._adjusted_lines(lines),
            color=color,
            buff=SMALL_BUFF * self.code_scale)
        current_hr = self.get_current_highlight()
        current_hr.become(r)
        self.highlighted_lines = lines
        return self

    def remove_highlight(self):
        r = self._get_hidden_highlight(self.highlighted_lines)
        current_hr = self.get_current_highlight()
        current_hr.become(r)
        return self

    # Move the hidden rect and resize correctly
    def move_hidden_highlight(self, lines):
        r = self._get_hidden_highlight(lines)
        current_hr = self.get_current_highlight()
        current_hr.become(r)
        self.highlighted_lines = lines
        return self

    def fade_labels(self):
        if self.add_labels:
            self.get_labels().set_opacity(0)
        return self

    def show_labels(self):
        if self.add_labels:
            self.get_labels().set_opacity(1)
        return self

    # Calls and returns
    #
    # Setup calls or returns, animations to show them, and post-xfer cleanup
    def _pre_call_ret(self, dst_code, dst_lines):
        """
        Shared parts of preparing calls and returns

        Rects provided are not owned by either code block.
        """
        srcr = self.get_current_highlight()
        if self != dst_code:
            srcr = srcr.copy()
        dstr = dst_code.get_code().get_lines_highlight_rect(
            dst_code._adjusted_lines(dst_lines),
            color=YELLOW,
            buff=SMALL_BUFF * self.code_scale)
        xfer_info = {
            'src_rect': srcr,
            'dst_rect': dstr,
            'exaggerate_arc': 1.0,
            'dst_code': dst_code,
        }

        d = (srcr.get_center()[1] - dstr.get_center()[1]) / srcr.get_height()
        if abs(d) < 3:
            xfer_info['exaggerate_arc'] = 1.5

        return xfer_info

    def pre_call(self, dst_code, dst_lines):
        """
        Setup a call, leaving a white highlight at the source
        """
        xfer_info = self._pre_call_ret(dst_code, dst_lines)

        if self != dst_code:
            self.generate_target()
            self.target.get_current_highlight().set_color(WHITE)
            self.remove_highlight()
        else:
            self.generate_target()

        xfer_info['mtt_code'] = self
        return xfer_info

    def pre_return(self, dst_code, dst_lines):
        """
        Setup a return, removing any highlight at the dest
        """
        xfer_info = self._pre_call_ret(dst_code, dst_lines)

        if self != dst_code:
            self.remove_highlight()
            dst_code.generate_target()
            dst_code.target.remove_highlight()
        else:
            dst_code.generate_target()

        xfer_info['mtt_code'] = dst_code
        return xfer_info

    @staticmethod
    def get_control_transfer_animations(xfer_info, path_arc=np.pi):
        """
        Animations for a call or return, with an arc path for the highlight
        """
        return [
            MoveToTarget(xfer_info['mtt_code']),
            ReplacementTransform(
                xfer_info['src_rect'],
                xfer_info['dst_rect'],
                path_arc=path_arc * xfer_info['exaggerate_arc'],
            )
        ]

    @staticmethod
    def get_control_transfer_clockwise(xfer_info):
        return CodeBlock.get_control_transfer_animations(xfer_info,
                                                         path_arc=-np.pi)

    @staticmethod
    def get_control_transfer_counterclockwise(xfer_info):
        return CodeBlock.get_control_transfer_animations(xfer_info,
                                                         path_arc=np.pi)

    def post_control_transfer(self, xfer_info, scene):
        """
        Cleanup after a call or return.

        This needs to be called before the next animation or wait to ensure
        that the destination rects are properly owned by the dest code and
        the scene.
        """
        assert (self == xfer_info['dst_code'])
        cr = self.get_current_highlight()
        self._tracked_remove(cr)
        scene.remove(cr)
        dstr = xfer_info['dst_rect']
        self.add(dstr)
        self.hr_index = self.submobjects.index(dstr)
        scene.remove(dstr)
        scene.add(self)

    # Annotations
    def set_annotation(self, line, text):
        """
        Add an annotation to the right of a line of text.
        """
        if text is None:
            t = VectorizedPoint()
        else:
            if text is Mobject:
                t = text
            else:
                t = TextMobject('\\textit{%s}' % text)
            t.set_color(self.annotation_color).scale(self.annotation_scale)
        loc = self.get_lines(line)
        t.next_to(loc[0][0], RIGHT)
        t.next_to(loc, RIGHT, buff=self.annotation_buff, coor_mask=X_AXIS)

        if line in self.annotation_indexes:
            ot = self[self.annotation_indexes[line]]
            ot.become(t)
        else:
            self.add(t)
            self.annotation_indexes[line] = self.submobjects.index(t)
        return self

    def prep_annotations(self, *lines):
        """
        Call for the lines where annotations will be added before adding one
        via an animation.
        """
        for l in lines:
            if l not in self.annotation_indexes:
                loc = self.get_lines(l)
                p = VectorizedPoint(loc.get_right())
                self.add(p)
                self.annotation_indexes[l] = self.submobjects.index(p)
        return self

    def get_annotation(self, line):
        if line in self.annotation_indexes:
            return self[self.annotation_indexes[line]]
        return None
