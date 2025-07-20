from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints

class ZhiXianHeYuan11(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-5, 1],
            y_range=[-5, 1],
            x_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        axes.move_to(ORIGIN)

        self.add(axes)

        l_line = LinearFunctionTwoPoints((-3/2,0),(0,3))
        l_line_graph = l_line.plot_in(axes)
        self.play(Create(l_line_graph))

        a_dot = Dot(color=GREEN).move_to(axes.c2p(-2, -1))
        a_label = MathTex("A", color=GREEN).next_to(a_dot, UP)
        self.play(Create(a_dot), Create(a_label))
        self.wait(2)

        circ = CustomCircle((0,-2), np.sqrt(5))
        circ_graph = circ.plot_in(axes)
        circ_center_dot = circ.get_center_dot(axes)
        ac_line = LinearFunctionPointSlope((-2, -1), np.atan(-1/2))
        ac_line_graph = ac_line.plot_in(axes, color=RED)
        self.play(Create(ac_line_graph))
        self.wait(1)
        self.play(Create(circ_center_dot))
        self.wait(2)
        self.play(Create(circ_graph))
        self.wait(2)