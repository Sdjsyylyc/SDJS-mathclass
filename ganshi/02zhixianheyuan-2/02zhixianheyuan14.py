from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints

class ZhiXianHeYuan14(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-6, 2],
            y_range=[-4, 4],
            x_length=7,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        axes.move_to(ORIGIN)
        self.add(axes)

        circ = CustomCircle((-3,-2), 1)
        circ_graph = circ.plot_in(axes, color=RED)
        circ_center_dot = circ.get_center_dot(axes, color=RED)

        a_tracker = ValueTracker(1)
        a_slider = SliderComponent("a", a_tracker, -2, 2).to_corner(UR, buff=0.5)
        
        a_dot = Dot(color=BLUE).move_to(axes.c2p(-2,3))
        a_label = MathTex("A", color=BLUE).next_to(a_dot, UP)

        a1_dot = always_redraw(lambda: Dot(color=BLUE).move_to(axes.c2p(-2, a_tracker.get_value()*2-3))) 
        a1_label = always_redraw(lambda: MathTex("A_1", color=BLUE).next_to(a1_dot, DOWN))

        b_dot = always_redraw(lambda: Dot(color=GREEN).move_to(axes.c2p(0,a_tracker.get_value())))
        b_label = always_redraw(lambda: MathTex("B", color=GREEN).next_to(b_dot, RIGHT))

        l_line = LinearFunctionTwoPoints((-2,3), (0,a_tracker))
        l_line_graph = always_redraw(lambda: l_line.plot_in(axes))

        ab1_line_graph = always_redraw(lambda: LinearFunctionTwoPoints((-2,2*a_tracker.get_value()-3), (0,a_tracker)).plot_in(axes))

        y_line = LinearFunctionPointSlope((0, a_tracker), 0)
        y_line_graph = always_redraw(lambda: y_line.plot_in(axes, color=GRAY))

        self.play(Create(circ_graph), Create(circ_center_dot), Create(a_dot), Create(a_label), Create(b_dot), Create(b_label), Create(a_slider))
        self.wait(2)

        self.play(a_tracker.animate.set_value(-1))
        self.play(a_tracker.animate.set_value(2))
        self.play(a_tracker.animate.set_value(1))
        self.wait(2)

        self.play(Create(l_line_graph), Create(y_line_graph), Create(a1_dot), Create(a1_label))
        self.play(Create(ab1_line_graph))
        self.wait(2)

        self.play(a_tracker.animate.set_value(0))
        self.play(a_tracker.animate.set_value(2))
        self.play(a_tracker.animate.set_value(1))
        self.wait(3)

        self.play(a_tracker.animate.set_value(3/2), run_time=4)
        self.wait(3)

        self.play(a_tracker.animate.set_value(1/3), run_time=4)
        self.wait(3)
