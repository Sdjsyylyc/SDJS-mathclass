from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints

class ZhiXianHeYuan10(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-8, 2],
            y_range=[-2, 8],
            x_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        axes.move_to(ORIGIN)
        # axes.shift(-axes.get_center())

        self.add(axes)

        l_line = LinearFunctionTwoPoints((-6,0),(0,6))
        l_line_graph = l_line.plot_in(axes)
        self.play(Create(l_line_graph))

        a_dot = Dot(color=GREEN).move_to(axes.c2p(-6, 0))
        a_label = MathTex("A", color=GREEN).next_to(a_dot, DOWN)
        b_dot = Dot(color=GREEN).move_to(axes.c2p(0, 6))
        b_label = MathTex("B", color=GREEN).next_to(b_dot, RIGHT)
        ab_line = Line(a_dot, b_dot, color=GREEN)
        self.play(Create(a_dot), Create(a_label), Create(b_dot), Create(b_label), Create(ab_line))
        self.wait(2)

        r_tracker = ValueTracker(1)
        r_slider = SliderComponent("r", r_tracker, 0, 5).to_corner(UR, buff=0.5)
        circ = CustomCircle((-1,3), r_tracker)
        circ_graph = always_redraw(lambda: circ.plot_in(axes))
        circ_center_dot = circ.get_center_dot(axes)
        self.play(Create(circ_graph), Create(circ_center_dot), Create(r_slider))
        self.wait(2)

        def get_dl():
            r = r_tracker.get_value()
            if r < np.sqrt(2):
                return VGroup()
            else:
                delta = np.sqrt((r**2-2)/2)
                x1 = -2 + delta
                x2 = -2 - delta
                dot1 = Dot(color=BLUE).move_to(axes.c2p(x1, x1+6))
                dot1_label = MathTex("C", color=BLUE).next_to(dot1, UP)
                dot2 = Dot(color=BLUE).move_to(axes.c2p(x2, x2+6))
                dot2_label = MathTex("D", color=BLUE).next_to(dot2, UP)
                line = Line(dot1, dot2, color=BLUE)
                return VGroup(dot1, dot1_label, dot2, dot2_label, line)
        
        dl = always_redraw(get_dl)
        self.add(dl)

        def get_cd_len():
            r = r_tracker.get_value()
            if r < np.sqrt(2):
                return 0
            else:
                return 2*np.sqrt((r**2-2))

        cd_value = always_redraw(lambda: MathTex(r"CD = ", f"{get_cd_len():.2f}", color=BLUE, font_size=30).set_color_by_tex("CD = ", WHITE).next_to(r_slider, DOWN))
        self.play(Create(cd_value))

        self.play(r_tracker.animate.set_value(3), run_time=4)
        self.wait(2)

        self.play(r_tracker.animate.set_value(2), run_time=6)
        self.wait(3)
        