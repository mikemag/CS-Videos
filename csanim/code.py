from manimlib.imports import *

import pygments.lexers
from pygments.formatters import LatexFormatter


# TODO: requires the mods to SVGMobject to respect fill colors.
class CodeTextString(SingleStringTexMobject):
    """
    A snippet of code in a given language, possibly multiple lines.

    The code will be formatted with Pygments based on the language given. Each line
    is split apart and available using normal indexing.

    Supports getting highlighting rectangles for lines or groups of lines.
    """

    CONFIG = {
        'alignment': '',
        # TODO: could use a different template, or generate it once given a Pygments style.
        # - Also, can get the extra style code from LatexFormatter().get_style_defs()
        'template_tex_file_body': TEMPLATE_TEXT_FILE_BODY,
        'arg_separator': '',
        'line_tolerance':
        0.2,  # Delta in y to determine line breaks from the SVG
    }

    def __init__(self, language, raw_code_string, **kwargs):
        digest_config(self, kwargs, locals())
        lexer = pygments.lexers.get_lexer_by_name(language)
        code = pygments.highlight(raw_code_string, lexer, LatexFormatter())
        super().__init__(code, **kwargs)
        self.raw_code_string = raw_code_string
        self.latex_code_string = code

        # The original LaTeX string has newlines in it, which makes it easy to separate.
        # The first and last lines are boilerplate from Pygments, so discard them.
        self.tex_strings = self.latex_code_string.splitlines()
        self.tex_strings = self.tex_strings[1:-1]

        # If the last line is empty it's okay, just trim it off too.
        if len(self.tex_strings[-1].strip()) == 0:
            self.tex_strings = self.tex_strings[:-1]

        self.break_up_by_lines()

    # Pygments has full control over the generated TeX, so let's not muck with it!
    def modify_special_strings(self, tex):
        return tex

    # Pick apart the code into individual lines, with the string that generated them.
    # This is much like TexMobject.break_up_by_substrings().
    # TODO: doesn't handle blank lines in the middle of the source...
    def break_up_by_lines(self):
        # The submobjects have no association with the original input, but they do have x,y coords.
        # So we can break lines by changes in Y. The lines are presented in-order in the SVG, too.
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
                '%s: split SVG into %d lines, but there are %d lines in the original '
                'LaTeX from Pygments! See %s' %
                (self.name, len(new_submobjects), len(
                    self.tex_strings), self.file_path))
        self.submobjects = new_submobjects
        return self

    # The SVG is nicely colored for us, so don't try to adjust it further after we've gone to
    # all the work to import those colors from the SVG.
    # TODO: factor this better with the superclass.
    def init_colors(self):
        self.set_fill(
            # color=self.fill_color or self.color,
            opacity=self.fill_opacity, )
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

    # Line numbers start at 1
    def get_line(self, line_no):
        return self[line_no - 1]

    def get_lines(self, start, end):
        return self[start - 1:end]

    def __get_highlight_rect(self, left_x, right_x, lines_obj, color):
        buff = SMALL_BUFF  # mmmfixme: pass in as an arg, or make it based on the overall line height so it scales properly with smaller text
        # r = RoundedRectangle(width=right_x - left_x + 2 * buff,
        r = Rectangle(
            width=right_x - left_x + 2 * buff,
            height=lines_obj.get_height() + 2 * buff,
            stroke_width=0,
            stroke_opacity=0,
            fill_color=color,
            fill_opacity=0.2,
            corner_radius=0.1,
        )
        r.move_to(lines_obj, aligned_edge=RIGHT).shift(RIGHT * buff)
        return r

    def get_line_highlight_rect(self, lines, color=YELLOW):
        if isinstance(lines, tuple):
            code_line = VGroup(self[lines[0] - 1:lines[1]])
        else:
            code_line = self.get_line(lines)
        left_x = self.get_left()[0]
        right_x = code_line.get_right()[0]
        return self.__get_highlight_rect(left_x, right_x, code_line, color)


class CodeBlock(VGroup):
    """
    A block of code with line highlighting.

    Hold a (possibly multiline) snippet of code in a given language, with support
    for highlighting lines and stepping between them, animating the highlight.
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

    # Returns a from and to highlight rect, each of which are independent of the code block
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
