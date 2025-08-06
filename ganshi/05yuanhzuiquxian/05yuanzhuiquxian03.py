from manim import *
import numpy as np
import sys
import os
import math
from scipy.optimize import fsolve, brentq
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints, Ellipse, Parabola

class Yuanzhuiquxian03(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-5, 5],
            y_range=[-5, 5],
            x_length=7,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        axes.move_to(ORIGIN)
        o_dot = Dot(color=WHITE).move_to(axes.c2p(0, 0))
        o_label = MathTex(r"O").next_to(o_dot, DOWN+LEFT)
        self.add(axes, o_dot, o_label)

        a_tracker = ValueTracker(3)
        b_tracker = ValueTracker(2).add_updater(lambda m: m.set_value(np.sqrt(13-a_tracker.get_value()**2)))
        elli = Ellipse(a_tracker, b_tracker)
        elli_graph = always_redraw(lambda: elli.plot_in(axes))
        self.play(Create(elli_graph))
        self.add(a_tracker, b_tracker)

        circ = CustomCircle((0,0), np.sqrt(13))
        circ_graph = circ.plot_in(axes, color=BLUE)
        circ_func = circ.get_parametric_function()
        self.play(Create(circ_graph))

        pos_tracker = ValueTracker(0)
        # p_dot = always_redraw(lambda: Dot(color=WHITE).move_to(axes.c2p(*circ_func(pos_tracker.get_value()))))
        # p_label = always_redraw(lambda: MathTex(r"P", color=WHITE).next_to(p_dot, RIGHT))
        # self.play(Create(p_dot), Create(p_label))

        def get_tang_line():
            x0, y0 = circ_func(pos_tracker.get_value())
            a = a_tracker.get_value()
            b = b_tracker.get_value()
            delta = np.sqrt(a**2*y0*y0+b**2*x0*x0-a**2*b**2)
            k1 = (x0*y0 + delta)/(x0*x0-a**2)
            k2 = (x0*y0 - delta)/(x0*x0-a**2)
            l1 = LinearFunctionPointSlope((x0, y0), np.arctan(k1)).plot_in(axes, color=GREEN)
            l2 = LinearFunctionPointSlope((x0, y0), np.arctan(k2)).plot_in(axes, color=GREEN)
            l3 = LinearFunctionPointSlope((-x0, -y0), np.arctan(k1)).plot_in(axes, color=GREEN)
            l4 = LinearFunctionPointSlope((-x0, -y0), np.arctan(k2)).plot_in(axes, color=GREEN)
            return VGroup(l1, l2, l3, l4)
        
        tang_line = always_redraw(get_tang_line)
        self.play(Create(tang_line))
        self.wait(2)

        self.play(pos_tracker.animate.set_value(PI/2), run_time=6)
        self.wait(3)

        self.play(a_tracker.animate.set_value(1), run_time=6)
        self.wait(3)

        
        
        
        
        
        