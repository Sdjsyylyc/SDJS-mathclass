from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints

class Xianyuyuan07(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-4, 4, 0.5],
            y_range=[-3, 5, 0.5],
            x_length=8,
            y_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
            origin_point=DOWN
        )

        b_tracker = ValueTracker(0)
        l_line = LinearFunctionPointSlope((0,b_tracker), np.atan(1.732))
        l_line_graph = always_redraw(lambda: l_line.plot_in(axes, [-4, 4], [-4, 4], color=WHITE, stroke_width=2, stroke_opacity=1))
        circ = CustomCircle((0,1), 1)
        circ_graph = always_redraw(lambda: circ.plot_in(axes, color=WHITE, stroke_width=2, stroke_opacity=1))
        circ_center_dot = always_redraw(lambda: circ.get_center_dot(axes, color=WHITE, radius=0.05))
        a_dot = always_redraw(lambda: Dot(color=BLUE).move_to(axes.c2p(0, b_tracker.get_value())))
        a_dot_label = always_redraw(lambda: MathTex(r"A", color=BLUE).next_to(a_dot, RIGHT))
        b_dot = Dot(color=BLUE).move_to(axes.c2p(-0.866, 1.5))
        b_dot_label = always_redraw(lambda: MathTex(r"B", color=BLUE).next_to(b_dot, DOWN))
        collision_effect = CollisionEffect(axes.c2p(-0.866, 1.5))

        self.add(axes)
        self.play(Create(circ_graph), Create(circ_center_dot))
        self.wait(2)

        self.play(Create(l_line_graph), Create(a_dot), Create(a_dot_label))
        self.wait(2)

        self.play(b_tracker.animate.set_value(3), run_time=6)
        self.add(collision_effect.get_lines())
        self.play(collision_effect.get_animation(), Create(b_dot), Create(b_dot_label))
        self.remove(collision_effect.get_lines())
        self.wait(1)

        ab_line = Line(color=BLUE).put_start_and_end_on(axes.c2p(0, b_tracker.get_value()), axes.c2p(-0.866, 1.5))
        r_line = Line(color=RED).put_start_and_end_on(axes.c2p(-0.866, 1.5), axes.c2p(0, 1))
        self.play(Create(ab_line), Create(r_line))
        self.wait(2)

