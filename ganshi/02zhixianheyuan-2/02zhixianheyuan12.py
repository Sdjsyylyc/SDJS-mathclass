from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints

class ZhiXianHeYuan12(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[0, 10],
            y_range=[-2, 10],
            x_length=6,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        axes.move_to(ORIGIN)

        self.add(axes)

        l_line = LinearFunctionPointSlope((0,0), np.atan(2))
        l_line_graph = l_line.plot_in(axes)
        self.play(Create(l_line_graph))
        self.wait(1)

        b_dot = Dot().move_to(axes.c2p(5, 0))
        b_label = MathTex("B").next_to(b_dot, DOWN)
        self.play(Create(b_dot), Create(b_label))
        self.wait(1)

        xa_tracker = ValueTracker(0)
        xa_slider = SliderComponent("x_A", xa_tracker, 0, 5).to_corner(UR, buff=0.5)
        a_dot = always_redraw(lambda: Dot(color=GREEN).move_to(axes.c2p(xa_tracker.get_value(), 2*xa_tracker.get_value())))
        a_label = always_redraw(lambda: MathTex("A", color=GREEN).next_to(a_dot, UP))
        self.play(Create(xa_slider), Create(a_dot), Create(a_label))
        self.wait(1)

        ab_line = always_redraw(lambda: Line(a_dot.get_center(), b_dot.get_center(), color=GREEN))
        c_dot = always_redraw(lambda: Dot(color=RED).move_to((a_dot.get_center()+b_dot.get_center())/2))
        c_label = always_redraw(lambda: MathTex("C", color=RED).next_to(c_dot, DOWN))
        c_circ = always_redraw(lambda: Circle(radius=np.linalg.norm(a_dot.get_center()-b_dot.get_center())/2, color=RED).move_to(c_dot))
        self.play(Create(ab_line), Create(c_dot), Create(c_label))
        self.wait(2)
        self.play(Create(c_circ))
        self.wait(2)

        d_dot = Dot(color=BLUE).move_to(axes.c2p(1, 2))
        d_label = MathTex("D", color=BLUE).next_to(d_dot, LEFT)
        self.play(Create(d_dot), Create(d_label))
        self.wait(1)
        
        self.play(xa_tracker.animate.set_value(5), run_time=3)
        self.wait(1)
        self.play(xa_tracker.animate.set_value(2), run_time=3)
        self.wait(1)

        ad_line = always_redraw(lambda: Line(color=BLUE).put_start_and_end_on(d_dot.get_center(), a_dot.get_center()))
        bd_line = always_redraw(lambda: Line(color=BLUE).put_start_and_end_on(d_dot.get_center(), b_dot.get_center()))
        rec_angle1 = RightAngle(bd_line, ad_line, 0.3, color=BLUE)
        self.play(Create(ad_line), Create(bd_line), Create(rec_angle1))
        self.wait(1)
        self.play(xa_tracker.animate.set_value(5), run_time=2)
        self.play(xa_tracker.animate.set_value(2), run_time=2)
        self.wait(2)

        dc_line = always_redraw(lambda: Line(color=RED).put_start_and_end_on(d_dot.get_center(), c_dot.get_center()))
        self.play(Create(dc_line))
        self.wait(1)
        self.play(xa_tracker.animate.set_value(3), run_time=6)
        cd_line = Line(color=YELLOW).put_start_and_end_on(c_dot.get_center(), d_dot.get_center())
        ca_line = Line(color=YELLOW).put_start_and_end_on(c_dot.get_center(), a_dot.get_center())
        rec_angle2 = RightAngle(cd_line, ca_line, 0.2, color=YELLOW)
        self.play(Create(cd_line), Create(ca_line))
        self.play(Create(rec_angle2))
        self.wait(3)

