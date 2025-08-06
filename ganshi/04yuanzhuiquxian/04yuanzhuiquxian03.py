from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints, Ellipse

class Yuanzhuiquxian03(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-5, 5],
            y_range=[-4, 4],
            x_length=9,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        axes.move_to(ORIGIN)
        o_dot = Dot(color=WHITE).move_to(axes.c2p(0, 0))
        o_label = MathTex(r"O").next_to(o_dot, DOWN+LEFT, buff=0.2)
        self.add(axes, o_dot, o_label)

        a_tracker = ValueTracker(4)
        c_tracker = ValueTracker(1)
        k_tracker = ValueTracker(PI/6)
        e_value = always_redraw(lambda: MathTex(f"e = {1/a_tracker.get_value():.2f}", color=WHITE).to_corner(UR, buff=0.5))
        elli_graph = always_redraw(lambda: Ellipse(a=a_tracker.get_value(), b=np.sqrt(a_tracker.get_value()**2-c_tracker.get_value()**2)).plot_in(axes))
        f_dots = always_redraw(lambda: Ellipse(a=a_tracker.get_value(), b=np.sqrt(a_tracker.get_value()**2-c_tracker.get_value()**2)).get_foci_dots(axes))
        f1_label = always_redraw(lambda: MathTex(r"F_1", color=WHITE).next_to(f_dots[0], DOWN))
        f2_label = always_redraw(lambda: MathTex(r"F_2", color=WHITE).next_to(f_dots[1], DOWN))
        self.play(Create(elli_graph), Create(f_dots), Create(f1_label), Create(f2_label), Create(e_value))

        circ1 = CustomCircle((0,0), 1)
        circ1_graph = always_redraw(lambda: circ1.plot_in(axes, color=GREEN))
        circ2 = CustomCircle((-1,0), 2)
        circ2_graph = always_redraw(lambda: circ2.plot_in(axes, color=BLUE))
        l_line = LinearFunctionPointSlope((-1,0), k_tracker)
        l_line_graph = always_redraw(lambda: l_line.plot_in(axes, color=GRAY))
        p_dot = always_redraw(lambda: Dot(color=BLUE).move_to(circ2.get_radius_dot(axes, 2*k_tracker.get_value())))
        p_label = always_redraw(lambda: MathTex(r"P", color=BLUE).next_to(p_dot, UP))
        m_dot = always_redraw(lambda: Dot(color=GREEN).move_to(circ1.get_radius_dot(axes, 2*k_tracker.get_value())))
        m_label = always_redraw(lambda: MathTex(r"M", color=GREEN).next_to(m_dot, DOWN))
        pf2_line = always_redraw(lambda: Line(color=WHITE, stroke_width=2).put_start_and_end_on(p_dot.get_center(), f_dots[1].get_center()))
        mf2_line = always_redraw(lambda: Line(color=WHITE, stroke_opacity=0).put_start_and_end_on(m_dot.get_center(), f_dots[1].get_center()))
        mf1_line = always_redraw(lambda: Line(color=WHITE, stroke_opacity=0).put_start_and_end_on(m_dot.get_center(), f_dots[0].get_center()))
        f1mf2_recangle = always_redraw(lambda: RightAngle(mf1_line, mf2_line, color=WHITE, length=0.2))

        self.play(Create(l_line_graph))
        self.play(Create(p_dot), Create(p_label), Create(pf2_line))
        self.wait(2)

        self.play(Create(m_dot), Create(m_label))
        self.wait(2)

        self.add(mf2_line, mf1_line)

        self.play(Create(f1mf2_recangle))
        self.play(k_tracker.animate.set_value(PI/6+PI),run_time=5)
        self.play(Create(circ1_graph))
        self.play(Create(circ2_graph))
        self.wait(2)

        self.play(k_tracker.animate.set_value(PI/6), run_time=5)
        self.play(FadeOut(p_dot), FadeOut(p_label), FadeOut(m_dot), FadeOut(m_label), FadeOut(pf2_line), FadeOut(f1mf2_recangle), FadeOut(l_line_graph))
        self.wait(3)

        self.play(a_tracker.animate.set_value(2), run_time=3)
        self.wait(2)

        self.play(a_tracker.animate.set_value(3), run_time=6)
        self.wait(3)