from manim import *
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__))))))
from modules import CustomAxes, SliderComponent, LinearFunctionPointSlope, CollisionEffect

class Exp1(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"tip_width": 0.1},
            x_length=7,
            y_length=7,
        )
        self.play(Create(axes))
        self.wait(1)

        line_formula = MathTex(r"a",r"x",r"+",r"y",r"+",r"1",r"=",r"0", color=WHITE, font_size=36).set_color_by_tex("a", YELLOW)
        line_formula.to_edge(UP+LEFT, buff=0.5)
        self.play(Write(line_formula))
        self.wait(2)

        self.play(Transform(line_formula, MathTex(r"y=",r"-",r"a",r"x",r"-",r"1", color=WHITE, font_size=36).set_color_by_tex("a", YELLOW).to_edge(UP+LEFT, buff=0.5)))
        self.wait(2)

        a_tracker = ValueTracker(0)
        a_slider = SliderComponent("a", a_tracker, -PI/2, PI/2).to_edge(UP+RIGHT, buff=0.5)
        a_value = always_redraw(lambda: MathTex(r"a=",f"{np.tan(a_tracker.get_value()):.2f}", color=YELLOW, font_size=36).set_color_by_tex("a=", WHITE).next_to(a_slider, DOWN, buff=0.5))
        l_line = LinearFunctionPointSlope((0, -1), a_tracker)
        l_graph = always_redraw(lambda: l_line.plot_in(axes, [-5, 5], y_range=[-5, 5]))
        fix_dot = Dot(color=GREEN).move_to(axes.c2p(0, -1))
        self.play(Create(a_slider), Create(l_graph), Create(fix_dot), Create(a_value))
        self.wait(2)

        self.play(a_tracker.animate.set_value(PI/3), run_time=2)
        self.play(a_tracker.animate.set_value(-PI/3), run_time=2)
        self.wait(2)

        a_dot = Dot(color=BLUE).move_to(axes.c2p(2, 3))
        b_dot = Dot(color=BLUE).move_to(axes.c2p(-3, 2))
        ab_line = Line(a_dot, b_dot, color=BLUE)
        self.play(a_tracker.animate.set_value(0), Create(a_dot), Create(b_dot), Create(ab_line))
        self.wait(1)

        self.play(a_tracker.animate.set_value(np.atan(2)), run_time=5)
        a_collision = CollisionEffect(a_dot.get_center(), inner_radius=0.1)
        self.add(a_collision.get_lines())
        self.play(a_collision.get_animation())
        self.remove(a_collision.get_lines())
        self.wait(3)
        
        self.play(a_tracker.animate.set_value(np.atan(-1)+PI), run_time=5)
        b_collision = CollisionEffect(b_dot.get_center(), inner_radius=0.1)
        self.add(b_collision.get_lines())
        self.play(b_collision.get_animation())
        self.remove(b_collision.get_lines())
        self.wait(3)
