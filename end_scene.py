from manimlib.imports import *


# Some hard numbers on YouTube end screen element sizes from
# https://www.linkedin.com/pulse/tutorial-youtubes-new-end-screens-tara-hunt
#
# All are for a 1280 x 720 video, so scale based on that
#
# End screen element area: 1225 x 518
# Subscribe sphere: 196 x 196
# Popout rectangle: 542 x 230
# Link square: 196 x 196
# Video rect smallest: 410 x 230
# Video rect largest: 575 x 323

class EndScene(Scene):

    def animate_yt_end_screen(self,
                              scale_group,
                              fade_group,
                              end_scale=0.65,
                              show_rects=False,
                              show_elements=False):

        # Show the effective rect where the end screen will be scaled to
        dest_frame = Rectangle(width=FRAME_WIDTH * end_scale,
                               height=FRAME_HEIGHT * end_scale,
                               stroke_width=1)
        dest_frame.to_edge(UR, buff=0)
        if show_rects:
            self.add(dest_frame)
            self.add(self.get_yt_end_screen_elemen_area_rect())

        scale_group.remove(*fade_group)
        scale_group.generate_target()
        scale_group.target.scale(FRAME_WIDTH * end_scale /
                                 (scale_group.get_width() + MED_SMALL_BUFF))
        scale_group.target.move_to(dest_frame)

        ss = self.get_yt_end_screen_sub()
        sub = TextMobject('\\textbf{SUBSCRIBE}').scale(0.75).set_color(YELLOW)
        sub.next_to(ss, DOWN, buff=MED_SMALL_BUFF)

        thanks = TextMobject('Thanks for watching!').scale(1.20)
        thanks.next_to(ss, LEFT, buff=MED_LARGE_BUFF, aligned_edge=DOWN)

        # Need 15 total seconds from here
        self.play(MoveToTarget(scale_group), FadeOut(fade_group))  # 1 sec
        if show_elements:
            self.animate_yt_end_screen_elements()
        self.play(ShowCreation(thanks), FadeInFromDown(sub))  # 1 sec
        self.wait(duration=2)
        self.play(Indicate(sub), run_time=1.0)
        self.wait(duration=10.0)

    def animate_yt_end_screen_elements(self):
        ss = self.get_yt_end_screen_sub()
        esea = self.get_yt_end_screen_elemen_area_rect()
        v1 = self.get_yt_end_screen_element_rect(410, 230)
        v2 = self.get_yt_end_screen_element_rect(410, 230)
        v1.move_to(esea, aligned_edge=UL)
        v2.move_to(esea, aligned_edge=DL)
        self.play(*[FadeIn(o) for o in [v1, v2, ss]])

    @staticmethod
    def get_yt_end_screen_element_rect(width, height):
        return Rectangle(width=FRAME_WIDTH * width / 1280,
                         height=FRAME_HEIGHT * height / 720,
                         stroke_width=1)

    def get_yt_end_screen_elemen_area_rect(self):
        esea = self.get_yt_end_screen_element_rect(1225, 518)
        # Note: the overall placement rect isn't actually centered on YouTube,
        # so adjust up a smidge to match
        esea.shift(UP * 0.08)
        return esea

    def get_yt_end_screen_sub(self):
        esea = self.get_yt_end_screen_elemen_area_rect()
        sr = self.get_yt_end_screen_element_rect(196, 196)
        sr.move_to(esea, aligned_edge=DR).shift(UL * 0.05)
        c = Circle(radius=sr.get_width() / 2,
                   stroke_width=1)
        c.move_to(sr)
        return c
