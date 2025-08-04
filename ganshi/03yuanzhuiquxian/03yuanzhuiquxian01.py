from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints, Ellipse

class Yuanzhuiquxian01(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-2, 2],
            y_range=[-2, 2],
            x_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        axes.move_to(ORIGIN)
        self.add(axes)

        elli1 = Ellipse(a=np.sqrt(2), b=1)
        elli1_graph = elli1.plot_in(axes)
        elli1_func = elli1.get_parametric_function()

        b_tracker = ValueTracker(1)

        elli2 = Ellipse(a=np.sqrt(2), b=b_tracker)
        elli2_graph = always_redraw(lambda: elli2.plot_in(axes, color=RED))

        m_tracker = ValueTracker(PI/3)

        m_dot = always_redraw(lambda: Dot(color=BLUE).move_to(axes.c2p(elli1_func(m_tracker.get_value())[0], elli1_func(m_tracker.get_value())[1])))
        m_label = always_redraw(lambda: MathTex(f"M", color=BLUE).next_to(m_dot, RIGHT))
        m_line = always_redraw(lambda: Line(color=BLUE).put_start_and_end_on(m_dot.get_center(), axes.c2p(elli1_func(m_tracker.get_value())[0], 0)))
        p_dot = always_redraw(lambda: Dot(color=RED).move_to(axes.c2p(elli1_func(m_tracker.get_value())[0], np.sqrt(2)*elli1_func(m_tracker.get_value())[1])))
        p_label = always_redraw(lambda: MathTex(f"P", color=RED).next_to(p_dot, RIGHT))
        p_line = always_redraw(lambda: Line(color=RED).put_start_and_end_on(p_dot.get_center(), axes.c2p(elli1_func(m_tracker.get_value())[0], 0)))

        self.add(elli2_graph)
        self.play(Create(elli1_graph), Create(m_dot), Create(m_label))
        self.play(Create(m_line))
        self.wait(2)

        self.play(Create(p_dot), Create(p_label), Create(p_line))
        self.wait(2)

        self.play(m_tracker.animate.set_value(2*PI+PI/3), run_time=5)
        self.wait(2)

        self.play(b_tracker.animate.set_value(np.sqrt(2)), run_time=5)
        self.wait(2)

        self.play(m_tracker.animate.set_value(4*PI+PI/3), run_time=6)
        self.wait(3)

