from manim import *
from manim.utils.color.BS381 import ORANGE_BROWN
import numpy as np

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import CustomAxes, Ellipse

class Scene1Ellipse(MovingCameraScene):
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

        ellipse = Ellipse(a=2*np.sqrt(2), b=2)
        ellipse_func = ellipse.get_parametric_function()

        t_tracker = ValueTracker(PI/2)
        ellipse_graph = always_redraw(lambda: ParametricFunction(
            lambda t: axes.coords_to_point(*ellipse_func(t)),
            t_range=[PI/2, t_tracker.get_value()],
            color=ORANGE,
            stroke_width=6
        ))

        focus_right = ellipse.get_foci_dots(axes, color=RED)[1]
        focus_left = ellipse.get_foci_dots(axes, color=RED)[0]

        dot_radius_tracker = ValueTracker(0)
        p_dot = always_redraw(lambda: Dot(axes.coords_to_point(*ellipse_func(t_tracker.get_value())), color=ORANGE_BROWN, radius=dot_radius_tracker.get_value()))

        self.camera.frame.move_to(axes.c2p(*ellipse_func(t_tracker.get_value())))
        self.add(t_tracker, self.camera.frame)
        # camera_updater = lambda f: f.move_to(axes.c2p(*hyperbola_right_func(t_tracker.get_value())))
        # self.camera.frame.add_updater(camera_updater)
        # self.add(axes)
        self.add(ellipse_graph)
        self.add(focus_right, focus_left)
        self.add(p_dot)
        self.play(dot_radius_tracker.animate.set_value(0.1))

        line_width_tracker = ValueTracker(0)
        pf1_line = always_redraw(lambda: Line(p_dot.get_center(), focus_right.get_center(), color=GRAY, stroke_width=4*line_width_tracker.get_value()))
        pf2_line = always_redraw(lambda: Line(p_dot.get_center(), focus_left.get_center(), color=GRAY, stroke_width=4*line_width_tracker.get_value()))
        circle1 = always_redraw(lambda: Circle(radius=np.linalg.norm(focus_right.get_center() - p_dot.get_center()), color=GRAY_A, stroke_width=2*line_width_tracker.get_value()).move_to(p_dot.get_center()))
        circle2 = always_redraw(lambda: Circle(radius=4*np.sqrt(2), color=GRAY_A, stroke_width=2*line_width_tracker.get_value()).move_to(focus_left.get_center()))
        self.add(pf1_line, pf2_line, circle1, circle2)
        self.play(AnimationGroup(AnimationGroup(line_width_tracker.animate.set_value(1), run_time=4, rate_func=rate_functions.ease_out_cubic), AnimationGroup(t_tracker.animate.set_value(PI/2+2*PI), run_time=4), lag_ratio=0), AnimationGroup(Restore(self.camera.frame), rate_func=rate_functions.ease_out_cubic), run_time=4)


        # self.camera.frame.remove_updater(camera_updater)
        # self.play(Restore(self.camera.frame))
        self.play(AnimationGroup(AnimationGroup(AnimationGroup(FadeOut(focus_right), FadeOut(focus_left), FadeOut(pf1_line), FadeOut(pf2_line), FadeOut(circle1), FadeOut(circle2)), AnimationGroup(FadeOut(p_dot)), run_time=1.5, lag_ratio=0.5)))

        self.wait(2)

        self.camera.get_image().save("scene1_ellipse.png")


