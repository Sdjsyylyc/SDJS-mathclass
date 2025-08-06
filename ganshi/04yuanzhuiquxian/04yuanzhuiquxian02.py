from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints, Ellipse

class Yuanzhuiquxian02(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-3, 3],
            y_range=[-2, 2],
            x_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        axes.move_to(ORIGIN)
        o_dot = Dot(color=WHITE).move_to(axes.c2p(0, 0))
        o_label = MathTex(r"O").next_to(o_dot, DOWN+LEFT)
        self.add(axes, o_dot, o_label)

        a_tracker = ValueTracker(2.5)
        b_tracker = ValueTracker(1)
        pos_tracker = ValueTracker(PI/3)
        elli = Ellipse(a=a_tracker, b=b_tracker)
        elli_graph = always_redraw(lambda: elli.plot_in(axes))
        elli_func = elli.get_parametric_function()
        f_dots = always_redraw(lambda: elli.get_foci_dots(axes))
        f1_label = always_redraw(lambda: MathTex(r"F_1", color=WHITE).next_to(f_dots[0], DOWN))
        f2_label = always_redraw(lambda: MathTex(r"F_2", color=WHITE).next_to(f_dots[1], DOWN))
        self.play(Create(elli_graph), Create(f_dots), Create(f1_label), Create(f2_label))

        a_dot = always_redraw(lambda: Dot(color=WHITE).move_to(axes.c2p(*elli_func(pos_tracker.get_value()))))
        a_label = always_redraw(lambda: MathTex(r"A", color=WHITE).next_to(a_dot, UP))
        b_dot = always_redraw(lambda: Dot(color=WHITE).move_to(axes.c2p(*elli_func(pos_tracker.get_value()+PI))))
        b_label = always_redraw(lambda: MathTex(r"B", color=WHITE).next_to(b_dot, DOWN))
        self.play(Create(a_dot), Create(a_label), Create(b_dot), Create(b_label))

        af1_line = always_redraw(lambda: Line(color=WHITE).put_start_and_end_on(a_dot.get_center(), f_dots[0].get_center()))
        bf1_line = always_redraw(lambda: Line(color=WHITE).put_start_and_end_on(b_dot.get_center(), f_dots[0].get_center()))
        ab_line = always_redraw(lambda: Line(color=GRAY).put_start_and_end_on(a_dot.get_center(), b_dot.get_center()))
        af2_line = always_redraw(lambda: Line(color=GRAY).put_start_and_end_on(a_dot.get_center(), f_dots[1].get_center()))
        bf2_line = always_redraw(lambda: Line(color=GRAY).put_start_and_end_on(b_dot.get_center(), f_dots[1].get_center()))
        self.play(Create(af1_line), Create(bf1_line), Create(ab_line), Create(af2_line), Create(bf2_line))
        self.wait(2)

        abf1_triangle = always_redraw(lambda: Polygon(a_dot.get_center(), f_dots[0].get_center(), b_dot.get_center(), color=GREEN, fill_opacity=0.5))
        af1f2_triangle = always_redraw(lambda: Polygon(a_dot.get_center(), f_dots[0].get_center(), f_dots[1].get_center(), color=GREEN, fill_opacity=0.5))
        self.play(Create(abf1_triangle))
        self.wait(3)

        self.play(Transform(abf1_triangle, af1f2_triangle), run_time=5)
        self.remove(abf1_triangle)
        self.add(af1f2_triangle)
        self.wait(3)

        color_tracker = ValueTracker(0)
        area_formula = MathTex(r"S_{AF_1F_2} = bc = 2", color=WHITE, font_size=24).to_corner(UR, buff=0.5)
        c_line = always_redraw(lambda: Line(color=(1-color_tracker.get_value())*BLUE+color_tracker.get_value()*YELLOW).put_start_and_end_on(o_dot.get_center(), f_dots[1].get_center()))
        b_line = always_redraw(lambda: Line(color=(1-color_tracker.get_value())*GREEN+color_tracker.get_value()*YELLOW).put_start_and_end_on(o_dot.get_center(), axes.c2p(0, b_tracker.get_value())))
        c_line_label = always_redraw(lambda: MathTex(r"c", color=(1-color_tracker.get_value())*BLUE+color_tracker.get_value()*YELLOW).next_to(c_line, DOWN))
        b_line_label = always_redraw(lambda: MathTex(r"b", color=(1-color_tracker.get_value())*GREEN+color_tracker.get_value()*YELLOW).next_to(b_line, LEFT))
        self.play(pos_tracker.animate.set_value(PI/2), run_time=4)
        self.play(Create(c_line), Create(c_line_label), Create(b_line), Create(b_line_label))
        self.play(Write(area_formula))
        self.wait(3)

        self.play(a_tracker.animate.set_value(2), b_tracker.animate.set_value(np.sqrt(2)), color_tracker.animate.set_value(1), run_time=5)
        self.wait(3)
