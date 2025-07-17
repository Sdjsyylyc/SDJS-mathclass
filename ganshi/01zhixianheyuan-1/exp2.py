from manim import *
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__))))))
from modules import CustomAxes, SliderComponent, LinearFunctionPointSlope, CollisionEffect

class Exp2(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-4, 6, 1],
            y_range=[-3, 7, 1],
            axis_config={"tip_width": 0.1},
            x_length=7,
            y_length=7,
            origin_point=2*DOWN+RIGHT
        )
        self.play(Create(axes))
        self.wait(1)

        l_formula = MathTex(r"(2",r"m",r"+",r"1",r")",r"x",r"+",r"(",r"m",r"+",r"1",r")",r"y",r"-",r"7",r"m",r"-",r"4",r"=",r"0", color=WHITE, font_size=36).set_color_by_tex("m", YELLOW).to_edge(UP+LEFT, buff=0.5)
        self.play(Write(l_formula))
        self.wait(2)
        self.play(Transform(l_formula, MathTex(r"m",r"(",r"2",r"x",r"+",r"y",r"-",r"7",r")",r"+",r"(",r"x",r"+",r"y",r"-",r"4",r")",r"=",r"0", color=WHITE, font_size=36).set_color_by_tex("m", YELLOW).to_edge(UP+LEFT, buff=0.5)))
        self.wait(2)

        l1_formula = MathTex(r"l_1:",r"2",r"x",r"+",r"y",r"-",r"7",r"=",r"0", color=BLUE, font_size=36).next_to(l_formula, DOWN, buff=0.5)
        l1_graph = axes.plot(lambda x: -2*x+7, color=BLUE)
        l2_formula = MathTex(r"l_2:",r"x",r"+",r"y",r"-",r"4",r"=",r"0", color=GREEN, font_size=36).next_to(l1_formula, DOWN, buff=0.5)
        l2_graph = axes.plot(lambda x: -x+4, color=GREEN)
        cross_point_dot = Dot(color=RED).move_to(axes.c2p(3, 1))
        cross_point_label = MathTex(r"P(3,1)", color=RED, font_size=36).next_to(cross_point_dot, DOWN, buff=0.1)
        self.play(Write(l1_formula), Create(l1_graph))
        self.wait(1)
        self.play(Write(l2_formula), Create(l2_graph))
        self.wait(1)
        self.play(Create(cross_point_dot), Create(cross_point_label))
        self.wait(3)

        self.play(FadeOut(l1_formula), FadeOut(l1_graph), FadeOut(l2_formula), FadeOut(l2_graph))
        self.wait(1)


        k_tracker = ValueTracker(0)
        k_slider = SliderComponent("k", k_tracker, -PI/2, PI/2).to_edge(UP+RIGHT, buff=0.5)
        l_line = LinearFunctionPointSlope((3, 1), k_tracker)
        l_graph = always_redraw(lambda: 
                                l_line.plot_in(axes, [-4, 6], [-3, 7], color=WHITE)
                                )
        k_formula = MathTex(r"k=\frac{2m+1}{m+1}\ne2", color=WHITE, font_size=36).next_to(l_formula, DOWN, buff=0.5)
        self.play(Create(k_slider), Create(l_graph), Create(k_formula))
        self.wait(2)

        self.play(k_tracker.animate.set_value(PI/3), run_time=2)
        self.play(k_tracker.animate.set_value(-PI/3), run_time=2)
        self.play(k_tracker.animate.set_value(0), run_time=2)

        c_circle_graph = Circle(radius=axes.get_x_unit()*4, color=RED).move_to(axes.c2p(1, 2))
        c_circle_center_dot = Dot(color=RED).move_to(axes.c2p(1, 2))
        self.play(Create(c_circle_graph), Create(c_circle_center_dot))
        self.wait(2)
        
        self.play(k_tracker.animate.set_value(PI*2), run_time=4)
        self.wait(3)

        self.play(k_tracker.animate.set_value(np.atan(2)), run_time=4)
        cp_line = Line(c_circle_center_dot, cross_point_dot, color=RED)
        self.play(Create(cp_line))
        self.wait(3)