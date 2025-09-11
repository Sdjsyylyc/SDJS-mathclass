from manim import *
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__))))))
from modules import CustomAxes, SliderComponent, LinearFunctionPointSlope, CollisionEffect, CustomCircle

class TraceGeneral(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-10, 5, 1],
            y_range=[-10, 5, 1],
            axis_config={"tip_width": 0.1},
            x_length=7,
            y_length=7,
            origin_point=(UP+RIGHT),
        )
        self.play(Create(axes))
        self.wait(1)

        c1 = CustomCircle((-5, -5), 4)
        c2 = CustomCircle((1, 1), 1)
        c0 = CustomCircle((-7, -7), 5)
        c1_graph = c1.plot_in(axes, color=BLUE)
        c2_graph = c2.plot_in(axes, color=GREEN)
        self.play(Create(c1_graph), Create(c2_graph))
        self.wait(1)

        pos_tracker = ValueTracker(0)
        c1_dot = always_redraw(lambda: c1.get_radius_dot(axes, pos_tracker.get_value(), color=BLUE))
        c2_dot = always_redraw(lambda: c2.get_radius_dot(axes, pos_tracker.get_value(), color=GREEN))
        c0_dot = always_redraw(lambda: c0.get_radius_dot(axes, pos_tracker.get_value(), color=RED).set_fill(opacity=0))
        center_dot = always_redraw(lambda: Dot(axes.coords_to_point(3, 3), color=WHITE, radius=0.05))

        c3 = CustomCircle((-3, -3), 3)
        c4 = CustomCircle((-1, -1), 2)
        c3_graph = c3.plot_in(axes, color=GRAY)
        c4_graph = c4.plot_in(axes, color=GRAY)
        c3_dot = always_redraw(lambda: c3.get_radius_dot(axes, pos_tracker.get_value(), color=GRAY))
        c4_dot = always_redraw(lambda: c4.get_radius_dot(axes, pos_tracker.get_value(), color=GRAY))
        
        l_line = always_redraw(lambda: Line(color=WHITE, stroke_width=2).put_start_and_end_on(c0_dot.get_center(), center_dot.get_center()))
        self.play(Create(c1_dot), Create(c2_dot), Create(l_line), Create(c0_dot))
        self.wait(1)

        self.play(pos_tracker.animate.set_value(2*PI), run_time=4)
        self.wait(2)
        self.play(Create(c3_dot), Create(c4_dot))
        self.play(pos_tracker.animate.set_value(4*PI), run_time=6, rate_func=linear)
        self.wait(2)
        self.play(Create(c3_graph), Create(c4_graph))
        self.wait(1)
        self.play(pos_tracker.animate.set_value(6*PI), run_time=6, rate_func=linear)
        self.wait(2)
        