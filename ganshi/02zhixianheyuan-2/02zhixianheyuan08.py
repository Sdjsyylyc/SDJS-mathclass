from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints

class Xianyuyuan08(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-9, 9, 0.5],
            y_range=[-9, 9, 0.5],
            x_length=8,
            y_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )

        l_line = LinearFunctionPointSlope((-8,0), np.atan(1/np.sqrt(3)))
        l_line_graph = always_redraw(lambda: l_line.plot_in(axes, [-9, 9], [-9, 9], color=WHITE, stroke_width=2, stroke_opacity=1))
        
        r_tracker = ValueTracker(1)
        r_slider = SliderComponent(
            "r",
            r_tracker,
            0,
            8,
        ).to_corner(UR, buff=0.5)
        circ = CustomCircle((0,0), r_tracker)
        circ_graph = always_redraw(lambda: circ.plot_in(axes, color=WHITE, stroke_width=2, stroke_opacity=1))

        def get_cross_dot_and_line():
            r = r_tracker.get_value()
            if r < 4:
                return VGroup()
            else:
                delta = np.sqrt(r*r-16)
                dot1 = Dot(color=BLUE).move_to(axes.c2p(-2+np.sqrt(3)*delta/2, 2*np.sqrt(3)+delta/2))
                dot1_label = always_redraw(lambda: MathTex(r"A", color=BLUE).next_to(dot1, UP))
                dot2 = Dot(color=BLUE).move_to(axes.c2p(-2-np.sqrt(3)*delta/2, 2*np.sqrt(3)-delta/2))
                dot2_label = always_redraw(lambda: MathTex(r"B", color=BLUE).next_to(dot2, UP))
                line1 = Line(color=BLUE).put_start_and_end_on(dot1.get_center(), dot2.get_center())
                return VGroup(dot1, dot1_label, dot2, dot2_label, line1)
        cross_dot = always_redraw(get_cross_dot_and_line)

        self.add(axes)
        self.play(Create(l_line_graph))
        self.wait(2)
        self.play(Create(circ_graph), Create(cross_dot), Create(r_slider))
        self.wait(2)

        def get_ab_value():
            r = r_tracker.get_value()
            if r < 4:
                return MathTex(r"AB = 0", color=WHITE, font_size=30).next_to(r_slider, DOWN)
            else:
                return MathTex(r"AB = ",f"{2*np.sqrt(r*r-16):.2f}", color=BLUE, font_size=30).set_color_by_tex("AB = ", WHITE).next_to(r_slider, DOWN)

        ab_value = always_redraw(get_ab_value)

        self.play(Create(ab_value))
        self.wait(1)
        self.play(r_tracker.animate.set_value(7), run_time=4)
        self.wait(2)
        self.play(r_tracker.animate.set_value(5), run_time=6)
        self.wait(3)
        