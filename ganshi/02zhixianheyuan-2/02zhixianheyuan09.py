from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints

class Xianyuyuan09(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-4, 4, 0.5],
            y_range=[-4, 4, 0.5],
            x_length=8,
            y_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        
        k_tracker = ValueTracker(0)
        k_slider = SliderComponent(
            "k",
            k_tracker,
            -PI/2,
            PI/2,
        ).to_corner(UR, buff=0.5)
        m_tracker = ValueTracker(3)
        m_slider = SliderComponent(
            "m",
            m_tracker,
            0,
            4,
        ).next_to(k_slider, DOWN, buff=0.1)
        y_dot = always_redraw(lambda: Dot(color=GREEN, radius=0.04).move_to(axes.c2p(0, m_tracker.get_value())))
        l_line = LinearFunctionPointSlope((0,m_tracker), k_tracker)
        l_line_graph = always_redraw(lambda: l_line.plot_in(axes, [-4, 4], [-4, 4], color=WHITE, stroke_width=2, stroke_opacity=1))
        
        circ = CustomCircle((0,0), 2)
        circ_graph = always_redraw(lambda: circ.plot_in(axes, color=WHITE, stroke_width=2, stroke_opacity=1))

        def get_cross_dot_and_line():
            k = np.tan(k_tracker.get_value())
            m = m_tracker.get_value()
            if abs(m) > 2:
                return VGroup()
            else:
                delta = np.sqrt(4*k**2-m**2+4)
                x1 = (-k*m+delta)/(1+k**2)
                x2 = (-k*m-delta)/(1+k**2)
                dot1 = Dot(color=BLUE).move_to(axes.c2p(x1, k*x1+m))
                dot1_label = always_redraw(lambda: MathTex(r"M", color=BLUE).next_to(dot1, UP))
                dot2 = Dot(color=BLUE).move_to(axes.c2p(x2, k*x2+m))
                dot2_label = always_redraw(lambda: MathTex(r"N", color=BLUE).next_to(dot2, UP))
                line1 = Line(color=BLUE).put_start_and_end_on(dot1.get_center(), dot2.get_center())
                return VGroup(dot1, dot1_label, dot2, dot2_label, line1)
        cross_dot = always_redraw(get_cross_dot_and_line)

        self.add(axes)
        self.play(Create(circ_graph))
        self.wait(2)
        self.play(Create(l_line_graph), Create(cross_dot), Create(k_slider), Create(m_slider), Create(y_dot))
        self.wait(2)

        def get_mn_value():
            m = m_tracker.get_value()
            k = np.tan(k_tracker.get_value())
            if abs(m) > 2:
                return MathTex(r"MN = 0", color=WHITE, font_size=30).next_to(m_slider, DOWN)
            else:
                return MathTex(r"MN = ", f"{2*np.sqrt(4*k**2-m**2+4)/np.sqrt(1+k**2):.2f}", color=BLUE, font_size=30).set_color_by_tex("MN = ", WHITE).next_to(m_slider, DOWN)

        mn_value = always_redraw(get_mn_value)
        self.play(Create(mn_value))
        self.wait(1)

        self.play(m_tracker.animate.set_value(1), run_time=4)
        self.wait(2)
        self.play(k_tracker.animate.set_value(PI/4), run_time=4)
        self.play(k_tracker.animate.set_value(-PI/4), run_time=4)
        self.play(k_tracker.animate.set_value(0), run_time=4)
        self.wait(3)

        self.play(m_tracker.animate.set_value(np.sqrt(3)), run_time=6)
        self.wait(3)