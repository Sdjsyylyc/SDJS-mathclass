from manim import *
import numpy as np
import sys
import os
import math
from scipy.optimize import fsolve, brentq
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints, Ellipse, Parabola

class Yuanzhuiquxian02(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-3, 3],
            y_range=[-2.5, 2.5],
            x_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        axes.move_to(ORIGIN)
        o_dot = Dot(color=WHITE).move_to(axes.c2p(0, 0))
        o_label = MathTex(r"O").next_to(o_dot, DOWN+LEFT)
        self.add(axes, o_dot, o_label)

        elli = Ellipse(2, np.sqrt(2))
        elli_graph = elli.plot_in(axes)
        self.play(Create(elli_graph))

        c_dot = Dot(color=WHITE).move_to(axes.c2p(0, 1))
        c_label = MathTex(r"C", color=WHITE).next_to(c_dot, LEFT)
        self.play(Create(c_dot), Create(c_label))

        k_tracker = ValueTracker(PI/3)

        l_line = LinearFunctionPointSlope((0, 1), k_tracker)
        l_line_graph = always_redraw(lambda: l_line.plot_in(axes))
        self.play(Create(l_line_graph))

        def get_ad():
            k = np.tan(k_tracker.get_value())
            delta = np.sqrt(8*k*k+2)
            xa = (-2*k+delta)/(2*k*k+1)
            xd = (-2*k-delta)/(2*k*k+1)
            ya = k*xa+1
            yd = k*xd+1
            a_dot = Dot(color=WHITE).move_to(axes.c2p(xa, ya))
            a_label = MathTex(r"A", color=WHITE).next_to(a_dot, UP)
            d_dot = Dot(color=WHITE).move_to(axes.c2p(xd, yd))
            d_label = MathTex(r"D", color=WHITE).next_to(d_dot, LEFT)
            return VGroup(a_dot, a_label, d_dot, d_label)
        
        def get_ab():
            k = np.tan(k_tracker.get_value())
            delta = np.sqrt(8*k*k+2)
            xa = (-2*k+delta)/(2*k*k+1)
            xb = -(-2*k-delta)/(2*k*k+1)
            ya = k*xa+1
            yb = k*(-xb)+1
            b_dot = Dot(color=WHITE).move_to(axes.c2p(xb, yb))
            b_label = MathTex(r"B", color=WHITE).next_to(b_dot, RIGHT)
            l = LinearFunctionTwoPoints((xa, ya), (xb, yb))
            l_graph = l.plot_in(axes)
            return VGroup(b_dot, b_label, l_graph)
            
        ad_group = always_redraw(get_ad)
        self.play(Create(ad_group))
        self.wait(2)

        ab_group = always_redraw(get_ab)
        self.play(Create(ab_group))
        t_dot = Dot(color=BLUE).move_to(axes.c2p(0, 2))
        t_label = MathTex(r"T", color=BLUE).next_to(t_dot, LEFT)
        self.play(Create(t_dot), Create(t_label))
        self.wait(2)

        bd_line = always_redraw(lambda: Line(color=RED).put_start_and_end_on(ad_group[2].get_center(), ab_group[0].get_center()))
        self.play(Create(bd_line))
        self.wait(2)

        self.play(k_tracker.animate.set_value(PI/9), run_time=5)
        self.wait(1)
        self.play(k_tracker.animate.set_value(-PI/4), run_time=6)
        self.wait(3)

