from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle

class Xianyuyuan04(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-1, 5, 0.5],
            y_range=[-3, 3, 0.5],
            x_length=8,
            y_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
            origin_point=LEFT*2
        )

        theta_tracker = ValueTracker(0)
        opacity_tracker = ValueTracker(0)
        theta_slider = SliderComponent(
            r"\theta",
            theta_tracker,
            0,
            2*PI,
        ).to_edge(UP+RIGHT, buff=0.5)
        unit_circle = CustomCircle((0,0), 1)
        unit_circle_graph = always_redraw(lambda: unit_circle.plot_in(axes, stroke_opacity=opacity_tracker.get_value()))
        self.add(unit_circle_graph, axes)
        p_dot = always_redraw(lambda: unit_circle.get_radius_dot(axes, angle=theta_tracker.get_value()))
        p_label = always_redraw(lambda: MathTex(r"P").next_to(p_dot, RIGHT, buff=0.1))
        self.play(Create(theta_slider), Create(p_dot), Create(p_label))
        self.wait(2)
        self.play(theta_tracker.animate.set_value(PI*2), run_time=4)
        self.wait(2)
        self.play(theta_tracker.animate.set_value(0), opacity_tracker.animate.set_value(1), run_time=4)
        self.wait(2)

        k_tracker = ValueTracker(PI/4)
        k_slider = SliderComponent(
            r"\frac1m",
            k_tracker,
            -PI/2,
            PI/2,
        ).next_to(theta_slider, DOWN, buff=0.5)
        l_line = LinearFunctionPointSlope((2, 0), k_tracker)
        l_line_graph = always_redraw(lambda: l_line.plot_in(axes, [-1, 5], [-3, 3], color=GREEN))
        fix_dot = Dot(color=WHITE, radius=0.05).move_to(axes.c2p(2, 0))
        self.play(Create(k_slider), Create(l_line_graph), Create(fix_dot))
        self.wait(2)

        d_dot = always_redraw(lambda: Dot(color=RED, radius=0.1).move_to(axes.c2p(
            (1/np.tan(k_tracker.get_value())*np.cos(theta_tracker.get_value())+2*np.tan(k_tracker.get_value())+np.sin(theta_tracker.get_value()))/(np.tan(k_tracker.get_value())+1/np.tan(k_tracker.get_value())),
            (np.cos(theta_tracker.get_value())+np.tan(k_tracker.get_value())*np.sin(theta_tracker.get_value())-2)/(np.tan(k_tracker.get_value())+1/np.tan(k_tracker.get_value()))
        )))
        d_line = always_redraw(lambda: Line(color=RED).put_start_and_end_on(d_dot.get_center(), p_dot.get_center()))
        self.play(Create(d_dot), Create(d_line))
        self.wait(2)

        self.play(theta_tracker.animate.set_value(PI/3+PI/2), run_time=4)
        self.wait(2)

        self.play(k_tracker.animate.set_value(PI/3), run_time=4)
        self.wait(2)

        self.play(k_tracker.animate.set_value(PI/2), run_time=4)
        self.wait(2)

        self.play(theta_tracker.animate.set_value(PI), run_time=4)
        self.wait(3)