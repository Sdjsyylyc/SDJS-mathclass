from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints

class ZhiXianHeYuan15(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-7, 7],
            y_range=[-6, 5],
            x_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        axes.move_to(ORIGIN)
        self.add(axes)

        circ = CustomCircle((0,1/2), 6)
        circ_graph = circ.plot_in(axes)
        circ_center_dot = circ.get_center_dot(axes)

        r_tracker = ValueTracker(4)
        
        p_dot = always_redraw(lambda: Dot(color=RED).move_to(axes.c2p(np.sqrt(3)/2, 0)))
        p_label = always_redraw(lambda: MathTex("P", color=RED).next_to(p_dot, UP))

        p_circ = CustomCircle((np.sqrt(3)/2, 0), r_tracker)
        p_circ_graph = always_redraw(lambda: p_circ.plot_in(axes, color=RED))

        def get_cross():
            r = r_tracker.get_value()
            if r < 5 or r > 7:
                return VGroup()
            t1 = (r**2-37)
            delta = np.sqrt(-t1**2+144)
            x1 = (-np.sqrt(3)*t1+delta)/4
            x2 = (-np.sqrt(3)*t1-delta)/4
            y1 = np.sqrt(3)*x1+r**2-36-1/2
            y2 = np.sqrt(3)*x2+r**2-36-1/2
            a_dot = Dot(color=BLUE).move_to(axes.c2p(x1,y1))
            a_label = MathTex("A", color=BLUE).next_to(a_dot, RIGHT)
            b_dot = Dot(color=BLUE).move_to(axes.c2p(x2,y2))
            b_label = MathTex("B", color=BLUE).next_to(b_dot, LEFT)
            ap_line = Line(a_dot, p_dot, color=BLUE)
            bp_line = Line(b_dot, p_dot, color=BLUE)
            ab_line = Line(a_dot, b_dot, color=BLUE)
            abp_area = Polygon(a_dot.get_center(), b_dot.get_center(), p_dot.get_center(), color=BLUE, fill_opacity=0.5)
            return VGroup(a_dot, a_label, b_dot, b_label, ap_line, bp_line, ab_line, abp_area)
        
        cross_dots = always_redraw(get_cross)
        self.play(Create(circ_graph), Create(circ_center_dot), Create(p_dot), Create(p_label), Create(p_circ_graph))
        self.play(Create(cross_dots))
        self.wait(2)

        self.play(r_tracker.animate.set_value(7.5), run_time=6)
        self.wait(3)

        self.play(r_tracker.animate.set_value(np.sqrt(45)), run_time=6)
        fixed_cross_dots = get_cross()
        self.add(fixed_cross_dots)
        self.remove(cross_dots)
        self.play(fixed_cross_dots.animate.set_color(GOLD))
        self.play(fixed_cross_dots.animate.set_color(BLUE))
        self.wait(3)