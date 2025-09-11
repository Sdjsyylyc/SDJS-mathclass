from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle

class Xianyuyuan03(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-1, 5, 0.5],
            y_range=[-3, 3, 0.5],
            x_length=8,
            y_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
            origin_point=LEFT,
        )

        self.add(axes)

        circ = CustomCircle((2,0), np.sqrt(5))
        circ_graph = circ.plot_in(axes)
        circ_center = circ.get_center_dot(axes)
        fixed_dot = Dot(color=WHITE, radius=0.1).move_to(axes.c2p(0,-2))
        self.play(Create(circ_graph), Create(circ_center))
        self.wait(2)

        tang_line1 = LinearFunctionPointSlope((0,-2), np.atan(-4-np.sqrt(15)))
        tang_line2 = LinearFunctionPointSlope((0,-2), np.atan(-4+np.sqrt(15)))

        tang_line1_graph = tang_line1.plot_in(axes, [-1, 5], [-3, 3], color=GREEN)
        tang_line2_graph = tang_line2.plot_in(axes, [-1, 5], [-3, 3], color=GREEN)

        self.play(Create(tang_line1_graph), Create(tang_line2_graph), Create(fixed_dot))
        self.wait(2)

        a_line = Line(color=BLUE).put_start_and_end_on(axes.c2p(0,-2), axes.c2p(2,0))
        tang_dot1 = circ.get_radius_dot(axes, angle=PI-np.atan(1/(-4-np.sqrt(15))))
        tang_dot2 = circ.get_radius_dot(axes, angle=PI-np.atan(1/(-4+np.sqrt(15))))
        r1_line = Line(color=RED).put_start_and_end_on(tang_dot1.get_center(), axes.c2p(2,0))
        r2_line = Line(color=RED).put_start_and_end_on(tang_dot2.get_center(), axes.c2p(2,0))
        self.play(Create(a_line), Create(tang_dot1), Create(tang_dot2), Create(r1_line), Create(r2_line))
        self.wait(2)

        alpha_angle = Arc(start_angle=-np.atan(1/(-4-np.sqrt(15)))+PI/2, angle=np.atan(1/(-4+np.sqrt(15)))+3*np.atan(1/(-4-np.sqrt(15))), arc_center=axes.c2p(0,-2), color=GREEN)
        self.play(Create(alpha_angle))
        self.wait(2)