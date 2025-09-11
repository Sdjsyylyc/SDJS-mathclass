from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints

class ZhiXianHeYuan16(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-2, 14],
            y_range=[-2, 14],
            x_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        axes.move_to(ORIGIN)
        self.add(axes)

        circ = CustomCircle((6,7), 5)
        circ_graph = circ.plot_in(axes)
        m_dot = circ.get_center_dot(axes)
        m_label = MathTex("M", color=WHITE).next_to(m_dot, UP)
        a_dot = Dot(color=WHITE).move_to(axes.c2p(2,4))
        a_label = MathTex("A", color=WHITE).next_to(a_dot, DOWN)

        t_tracker = ValueTracker(2)
        t_slider = SliderComponent("t", t_tracker, -13, 13).to_corner(UR, buff=0.5)
        t_dot = always_redraw(lambda: Dot(color=BLUE).move_to(axes.c2p(t_tracker.get_value(), 0)))
        t_label = always_redraw(lambda: MathTex("T", color=BLUE).next_to(t_dot, DOWN))

        at_vec = always_redraw(lambda: Arrow(color=BLUE).put_start_and_end_on(a_dot.get_center(), t_dot.get_center()))

        def get_qp():
            t = t_tracker.get_value()
            theta = -np.arctan((2-t)/4)
            at_len = np.sqrt((2-t)**2+16)
            delta = np.arcsin(at_len/10)

            q_dot = circ.get_radius_dot(axes, theta+delta, color=BLUE)
            q_label = MathTex("Q", color=BLUE).next_to(q_dot, UP)
            p_dot = circ.get_radius_dot(axes, theta-delta, color=BLUE)
            p_label = MathTex("P", color=BLUE).next_to(p_dot, DOWN)
            qp_vec = Arrow(color=BLUE).put_start_and_end_on(q_dot.get_center(), p_dot.get_center())
            return VGroup(q_dot, q_label, p_dot, p_label, qp_vec)
        
        qp_group = always_redraw(get_qp)
        self.play(Create(circ_graph), Create(m_dot), Create(m_label), Create(a_dot), Create(a_label), Create(t_dot), Create(t_label), Create(at_vec))
        self.play(Create(qp_group), Create(t_slider))
        self.wait(3)

        self.play(t_tracker.animate.set_value(2+2*np.sqrt(21)), run_time=6)
        self.wait(3)
        self.play(t_tracker.animate.set_value(2-2*np.sqrt(21)), run_time=6)
        self.wait(3)
        
