from manim import *
from manim.utils.color.BS381 import ORANGE_BROWN
import numpy as np

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import CustomAxes, Parabola

class Scene1Parabola(MovingCameraScene):
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
            origin_point=LEFT,
            axis_config={"color": BLACK, "stroke_width": 2, "tip_length": 0.2},
        )

        parabola = Parabola(p=2)
        parabola_func = parabola.get_parametric_function()

        t_limit = 4
        t_tracker = ValueTracker(-t_limit)
        parabola_graph = always_redraw(lambda: ParametricFunction(
            lambda t: axes.coords_to_point(*parabola_func(t)),
            t_range=[-t_limit, t_tracker.get_value()],
            color=ORANGE,
            stroke_width=6
        ))

        focus_dot = parabola.get_focus_dot(axes, color=RED)
        directrix_line = parabola.get_directrix_line(axes, color=RED)

        dot_radius_tracker = ValueTracker(0)
        p_dot = always_redraw(lambda: Dot(axes.coords_to_point(*parabola_func(t_tracker.get_value())), color=ORANGE_BROWN, radius=dot_radius_tracker.get_value()))

        self.camera.frame.move_to(axes.c2p(*parabola_func(t_tracker.get_value())))
        self.add(t_tracker, self.camera.frame)
        # camera_updater = lambda f: f.move_to(axes.c2p(*hyperbola_right_func(t_tracker.get_value())))
        # self.camera.frame.add_updater(camera_updater)
        # self.add(axes)
        self.add(parabola_graph)
        self.add(focus_dot, directrix_line)
        self.add(p_dot)
        self.play(dot_radius_tracker.animate.set_value(0.1))

        line_width_tracker = ValueTracker(0)
        pf1_line = always_redraw(lambda: Line(p_dot.get_center(), focus_dot.get_center(), color=GRAY, stroke_width=4*line_width_tracker.get_value()))
        f2s_line = always_redraw(lambda: Line(p_dot.get_center(), np.array([directrix_line.get_center()[0], p_dot.get_center()[1], 0]), color=GRAY, stroke_width=6*line_width_tracker.get_value()))
        circle = always_redraw(lambda: Circle(radius=np.linalg.norm(focus_dot.get_center() - p_dot.get_center()), color=GRAY_A, stroke_width=2*line_width_tracker.get_value()).move_to(p_dot.get_center()))
        self.add(pf1_line, f2s_line, circle)
        self.play(AnimationGroup(AnimationGroup(line_width_tracker.animate.set_value(1), run_time=4, rate_func=rate_functions.ease_out_cubic), AnimationGroup(t_tracker.animate.set_value(t_limit), run_time=4), lag_ratio=0), AnimationGroup(Restore(self.camera.frame), rate_func=rate_functions.ease_out_cubic), run_time=4)


        # self.camera.frame.remove_updater(camera_updater)
        # self.play(Restore(self.camera.frame))
        self.play(AnimationGroup(AnimationGroup(AnimationGroup(FadeOut(focus_dot), FadeOut(directrix_line), FadeOut(pf1_line), FadeOut(f2s_line), FadeOut(circle)), AnimationGroup(FadeOut(p_dot)), run_time=1.5, lag_ratio=0.5)))

        self.wait(2)

        self.camera.get_image().save("scene1_parabola.png")


