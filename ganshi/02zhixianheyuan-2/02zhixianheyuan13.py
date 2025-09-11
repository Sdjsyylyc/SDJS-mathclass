from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints

class ZhiXianHeYuan13(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            x_length=7,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        axes.move_to(ORIGIN)
        self.add(axes)

        circ = CustomCircle((1,0), 2)
        circ_graph = circ.plot_in(axes)
        circ_center_dot = circ.get_center_dot(axes)
        circ_center_label = MathTex("C", color=WHITE).next_to(circ_center_dot, DOWN)
        self.play(Create(circ_graph), Create(circ_center_dot), Create(circ_center_label))
        self.wait(1)

        m_tracker = ValueTracker(1)
        m_slider = SliderComponent("m", m_tracker, -3, 3).to_corner(UR, buff=0.5)
        def get_l():
            m = m_tracker.get_value()
            if m == 0:
                l_line = LinearFunctionTwoPoints((-1,0), (0,float("inf")))
            else:
                l_line = LinearFunctionTwoPoints((-1,0), (0,1/m))
            return l_line.plot_in(axes)
        l_line = always_redraw(get_l)
        self.play(Create(m_slider), Create(l_line))
        self.wait(1)

        a_dot = Dot(color=GREEN).move_to(axes.c2p(-1,0))
        a_label = MathTex("A", color=GREEN).next_to(a_dot, DOWN)
        b_dot = always_redraw(lambda: Dot(color=GREEN).move_to(axes.c2p((4*m_tracker.get_value()**2)/(m_tracker.get_value()**2+1)-1, 4*m_tracker.get_value()/(m_tracker.get_value()**2+1))))
        b_label = always_redraw(lambda: MathTex("B", color=GREEN).next_to(b_dot, RIGHT))
        ab_line = always_redraw(lambda: Line(color=GREEN).put_start_and_end_on(a_dot.get_center(), b_dot.get_center()))
        self.play(Create(a_dot), Create(a_label), Create(b_dot), Create(b_label), Create(ab_line))
        self.wait(2)

        ca_line = always_redraw(lambda: Line(color=RED).put_start_and_end_on(circ_center_dot.get_center(), a_dot.get_center()))
        cb_line = always_redraw(lambda: Line(color=RED).put_start_and_end_on(circ_center_dot.get_center(), b_dot.get_center()))
        abc_area = always_redraw(lambda: Polygon(a_dot.get_center(), b_dot.get_center(), circ_center_dot.get_center(), color=RED, fill_opacity=0.5))
        self.play(Create(ca_line), Create(cb_line), Create(abc_area))
        self.wait(2)

        up_line = axes.plot(lambda x: 8/5, color=GRAY)
        down_line = axes.plot(lambda x: -8/5, color=GRAY)
        self.play(Create(up_line), Create(down_line))
        self.wait(2)

        self.play(m_tracker.animate.set_value(2), run_time=4)
        self.wait(2)
        self.play(m_tracker.animate.set_value(1/2), run_time=4)
        self.wait(2)
        self.play(m_tracker.animate.set_value(-1/2), run_time=4)
        self.wait(2)
        self.play(m_tracker.animate.set_value(-2), run_time=4)
        self.wait(2)
