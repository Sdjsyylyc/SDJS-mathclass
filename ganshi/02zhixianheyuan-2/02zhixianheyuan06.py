from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints

class Xianyuyuan06(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-14, 14, 0.5],
            y_range=[-14, 14, 0.5],
            x_length=8,
            y_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )

        r_tracker = ValueTracker(1)
        a_tracker = ValueTracker(2)
        b_tracker = ValueTracker(2)
        circ = CustomCircle((0,0), r_tracker)
        circ_graph = always_redraw(lambda: circ.plot_in(axes, color=WHITE, stroke_width=2, stroke_opacity=1))
        a_dot = always_redraw(lambda: Dot(color=BLUE).move_to(axes.c2p(a_tracker.get_value(), b_tracker.get_value())))
        a_dot_label = always_redraw(lambda: MathTex(r"A", color=BLUE).next_to(a_dot, UP))
        def get_l_line():
            a = a_tracker.get_value()
            b = b_tracker.get_value()
            r2 = r_tracker.get_value()*r_tracker.get_value()
            if a == 0:
                x = float('inf')
            else:
                x = r2/a
            if b == 0:
                y = float('inf')
            else:
                y = r2/b
            l_line = LinearFunctionTwoPoints((x, 0), (0, y))
            return l_line.plot_in(axes, [-14, 14], [-14, 14], color=WHITE, stroke_width=2, stroke_opacity=1)
        l_line = always_redraw(get_l_line)

        self.play(Create(axes), Create(circ_graph), Create(a_dot), Create(a_dot_label), Create(l_line))
        self.wait(2)

        self.play(a_tracker.animate.set_value(3), b_tracker.animate.set_value(4), run_time=4)
        self.wait(2)
        self.play(r_tracker.animate.set_value(5), run_time=6)
        self.wait(3)

        self.play(a_tracker.animate.set_value(5), b_tracker.animate.set_value(0), run_time=3)
        self.wait(1)
        self.play(a_tracker.animate.set_value(4), b_tracker.animate.set_value(-3), run_time=3)
        self.wait(1)

        self.play(a_tracker.animate.set_value(2), b_tracker.animate.set_value(2), run_time=6)
        self.wait(3)
        self.play(a_tracker.animate.set_value(4), b_tracker.animate.set_value(4), run_time=6)
        self.wait(3)