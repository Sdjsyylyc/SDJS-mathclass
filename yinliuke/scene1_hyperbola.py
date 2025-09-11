from manim import *
from manim.utils.color.BS381 import ORANGE_BROWN
import numpy as np

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import CustomAxes, Hyperbola

class Scene1Hyperbola(MovingCameraScene):
    def construct(self):
        self.camera.frame_width = 8
        self.camera.frame_height = 8
        self.camera.background_color = WHITE
        self.camera.frame.save_state()
        self.camera.frame.scale(0.3)
        axes = CustomAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            axis_config={"color": BLACK, "stroke_width": 2, "tip_length": 0.2},
        )

        hyperbola = Hyperbola(a=2, b=2)
        hyperbola_right_func = hyperbola.get_parametric_function()
        hyperbola_left_func = hyperbola.get_parametric_function(direction='left')

        t_limit = 1.32
        t_tracker = ValueTracker(-t_limit)
        hyperbola_right = always_redraw(lambda: ParametricFunction(
            lambda t: axes.coords_to_point(*hyperbola_right_func(t)),
            t_range=[-t_limit, t_tracker.get_value()],
            color=ORANGE,
            stroke_width=6
        ))
        hyperbola_left = always_redraw(lambda: ParametricFunction(
            lambda t: axes.coords_to_point(*hyperbola_left_func(t)),
            t_range=[-t_limit, t_tracker.get_value()],
            color=ORANGE,
            stroke_width=6
        ))

        focus_right = hyperbola.get_foci_dots(axes, color=RED)[1]
        focus_left = hyperbola.get_foci_dots(axes, color=RED)[0]

        dot_radius_tracker = ValueTracker(0)
        p_dot = always_redraw(lambda: Dot(axes.coords_to_point(*hyperbola_right_func(t_tracker.get_value())), color=ORANGE_BROWN, radius=dot_radius_tracker.get_value()))
        q_dot = always_redraw(lambda: Dot(axes.coords_to_point(*hyperbola_left_func(t_tracker.get_value())), color=ORANGE_BROWN, radius=dot_radius_tracker.get_value()))

        self.camera.frame.move_to(axes.c2p(*hyperbola_right_func(t_tracker.get_value())))
        self.add(t_tracker, self.camera.frame)
        # camera_updater = lambda f: f.move_to(axes.c2p(*hyperbola_right_func(t_tracker.get_value())))
        # self.camera.frame.add_updater(camera_updater)
        # self.add(axes)
        self.add(hyperbola_right, hyperbola_left)
        self.add(focus_right, focus_left)
        self.add(p_dot, q_dot)
        self.play(dot_radius_tracker.animate.set_value(0.1))

        def get_right_phase_segments():
            p = p_dot.get_center()
            r = focus_right.get_center()
            l = focus_left.get_center()
            right_len = np.linalg.norm(p - r)
            vec_left = l - p
            left_len = np.linalg.norm(vec_left)
            if left_len == 0:
                split_point = p
            else:
                unit_vec = vec_left / max(left_len, 1e-8)
                yellow_len = min(right_len, left_len)
                split_point = p + unit_vec * yellow_len
            # print(right_len, left_len, split_point)
            return split_point

        line_width_tracker = ValueTracker(0)
        pf1_line = always_redraw(lambda: Line(p_dot.get_center(), focus_right.get_center(), color=GRAY, stroke_width=4*line_width_tracker.get_value()))
        pf2_line = always_redraw(lambda: Line(p_dot.get_center(), focus_left.get_center(), color=GRAY, stroke_width=4*line_width_tracker.get_value()))
        f2s_line = always_redraw(lambda: Line(focus_left.get_center(), get_right_phase_segments(), color=RED, stroke_width=6*line_width_tracker.get_value()))
        self.add(pf1_line, pf2_line, f2s_line)
        self.play(AnimationGroup(AnimationGroup(line_width_tracker.animate.set_value(1), run_time=4, rate_func=rate_functions.ease_out_cubic), AnimationGroup(t_tracker.animate.set_value(t_limit), run_time=4), lag_ratio=0), AnimationGroup(Restore(self.camera.frame), rate_func=rate_functions.ease_out_cubic), run_time=4)


        # self.camera.frame.remove_updater(camera_updater)
        # self.play(Restore(self.camera.frame))
        self.play(AnimationGroup(AnimationGroup(AnimationGroup(FadeOut(focus_right), FadeOut(focus_left), FadeOut(pf1_line), FadeOut(pf2_line), FadeOut(f2s_line)), AnimationGroup(FadeOut(p_dot), FadeOut(q_dot)), run_time=1.5, lag_ratio=0.5)))

        self.wait(2)


