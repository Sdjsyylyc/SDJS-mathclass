from manim import *
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__))))))
from modules import CustomAxes, SliderComponent, LinearFunctionPointSlope, CollisionEffect, CustomCircle

class TraceExp1(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-5, 5, 1],
            y_range=[-3, 7, 1],
            axis_config={"tip_width": 0.1},
            x_length=7,
            y_length=7,
            origin_point=DOWN*2,
        )

        circle_formula = MathTex(r"C: x^2+y^2+6x-4y+9=0", color=WHITE, font_size=36).to_edge(UP+LEFT, buff=0.5)
        self.play(Write(circle_formula), Create(axes))
        self.wait(2)

        self.play(Transform(circle_formula, MathTex(r"C: (x+3)^2+(y-2)^2=4", color=WHITE, font_size=36).to_edge(UP+LEFT, buff=0.5)))
        self.wait(2)

        c1 = CustomCircle((-3, 2), 2)
        c1_graph = c1.plot_in(axes, color=WHITE)
        c1_center_dot = c1.get_center_dot(axes, color=WHITE)
        c2 = CustomCircle((0, 1), 1)
        c2_graph = c2.plot_in(axes, color=RED)
        c2_center_dot = c2.get_center_dot(axes, color=RED)
        self.play(Create(c1_graph), Create(c1_center_dot))
        self.wait(2)

        pos_tracker = ValueTracker(0)
        a_dot = always_redraw(lambda: c1.get_radius_dot(axes, pos_tracker.get_value(), color=WHITE))
        a_label = always_redraw(lambda: MathTex(r"A", color=WHITE, font_size=36).next_to(a_dot, UP, buff=0.5))
        b_dot = Dot(color=WHITE).move_to(axes.coords_to_point(3, 0))
        b_label = MathTex(r"B", color=WHITE, font_size=36).next_to(b_dot, UP, buff=0.5)
        ab_line = always_redraw(lambda: Line(color=WHITE, stroke_width=2).put_start_and_end_on(a_dot.get_center(), b_dot.get_center()))
        m_dot = always_redraw(lambda: c2.get_radius_dot(axes, pos_tracker.get_value(), color=RED))
        m_label = always_redraw(lambda: MathTex(r"M", color=RED, font_size=36).next_to(m_dot, UP, buff=0.5))
        self.play(Create(a_dot), Create(a_label), Create(b_dot), Create(b_label), Create(ab_line))
        self.wait(2)
        self.play(Create(m_dot), Create(m_label))
        self.wait(2)

        self.play(pos_tracker.animate.set_value(PI*2), run_time=4)
        self.wait(2)

        self.play(Create(c2_graph), Create(c2_center_dot))
        self.wait(2)

        self.play(pos_tracker.animate.set_value(PI*4), run_time=4)
        self.wait(2)