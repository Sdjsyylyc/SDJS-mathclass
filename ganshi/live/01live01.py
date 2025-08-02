from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints

class OmegaIllusion(MovingCameraScene):
    def construct(self):
        axes = CustomAxes(
            x_range=[0, 10, PI],
            y_range=[-2.5, 2.5, 1],
            x_length=8,
            y_length=5,
            axis_config={"tip_length": 0.2},
            origin_point=1.4*LEFT+DOWN
        )

        pi1_dot = Dot(color=WHITE, radius=0.02).move_to(axes.c2p(PI, 0))
        pi2_dot = Dot(color=WHITE, radius=0.02).move_to(axes.c2p(2*PI, 0))
        pi3_dot = Dot(color=WHITE, radius=0.02).move_to(axes.c2p(3*PI, 0))
        pi1_label = MathTex(r"\pi", color=WHITE, font_size=30).next_to(pi1_dot, DOWN)
        pi2_label = MathTex(r"2\pi", color=WHITE, font_size=30).next_to(pi2_dot, DOWN)
        pi3_label = MathTex(r"3\pi", color=WHITE, font_size=30).next_to(pi3_dot, DOWN)
        self.add(pi1_dot, pi2_dot, pi3_dot, pi1_label, pi2_label, pi3_label)

        unit_len = axes.get_y_unit()

        left_pos = 4.4*LEFT+DOWN

        left_axes = CustomAxes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            axis_config={"tip_length": 0.2},
            origin_point=left_pos
        )

        self.add(axes, left_axes)

        t_tracker = ValueTracker(PI/3)
        r_tracker = ValueTracker(1)
        omega_tracker = ValueTracker(1)
        phi_tracker = ValueTracker(0)

        unit_circ = CustomCircle((0,0), r_tracker)
        unit_circ_graph = always_redraw(lambda: unit_circ.plot_in(left_axes))
        unit_circ_center_dot = unit_circ.get_center_dot(left_axes)
        self.play(Create(unit_circ_graph), Create(unit_circ_center_dot))
        self.wait(1)

        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.move_to(left_pos).scale(0.6))
        self.wait(1)

        p_dot = always_redraw(lambda: unit_circ.get_radius_dot(left_axes, omega_tracker.get_value()*t_tracker.get_value()+phi_tracker.get_value(), color=RED))
        p_dot_label = always_redraw(lambda: MathTex(r"P(\cos\theta, \sin\theta)", color=RED, font_size=20).next_to(p_dot, RIGHT))
        p_line = always_redraw(lambda: Line(color=RED).put_start_and_end_on(left_axes.c2p(0,0), 
                                                                            left_axes.c2p(2*np.cos(omega_tracker.get_value()*t_tracker.get_value()+phi_tracker.get_value()),
                                                                                           2*np.sin(omega_tracker.get_value()*t_tracker.get_value()+phi_tracker.get_value()))))
        self.play(Create(p_dot), Create(p_dot_label), Create(p_line))
        self.wait(1)

        x_line = always_redraw(lambda: DashedLine(color=BLUE).put_start_and_end_on(left_axes.c2p(0,r_tracker.get_value()*np.sin(omega_tracker.get_value()*t_tracker.get_value()+phi_tracker.get_value())), 
                                                                            left_axes.c2p(r_tracker.get_value()*np.cos(omega_tracker.get_value()*t_tracker.get_value()+phi_tracker.get_value()),
                                                                                           r_tracker.get_value()*np.sin(omega_tracker.get_value()*t_tracker.get_value()+phi_tracker.get_value()))))
        y_line = always_redraw(lambda: DashedLine(color=GREEN).put_start_and_end_on(left_axes.c2p(r_tracker.get_value()*np.cos(omega_tracker.get_value()*t_tracker.get_value()+phi_tracker.get_value()),0), 
                                                                            left_axes.c2p(r_tracker.get_value()*np.cos(omega_tracker.get_value()*t_tracker.get_value()+phi_tracker.get_value()),
                                                                                           r_tracker.get_value()*np.sin(omega_tracker.get_value()*t_tracker.get_value()+phi_tracker.get_value()))))
        fixed_x_line = DashedLine(color=BLUE_A).put_start_and_end_on(x_line.get_start(), x_line.get_end()).set_opacity(0)
        fixed_y_line = DashedLine(color=GREEN_A).put_start_and_end_on(y_line.get_start(), y_line.get_end()).set_opacity(0)
        self.play(Create(x_line), Create(y_line), Create(fixed_x_line), Create(fixed_y_line))
        self.wait(2)
        self.add(fixed_x_line, fixed_y_line)
        self.play(fixed_x_line.animate.set_opacity(1), run_time=1)
        self.play(fixed_x_line.animate.set_opacity(0), run_time=1)
        self.wait(2)
        self.play(fixed_y_line.animate.set_opacity(1), run_time=1)
        self.play(fixed_y_line.animate.set_opacity(0), run_time=1)
        self.wait(3)
        self.play(fixed_y_line.animate.set_opacity(1), run_time=1)
        self.play(fixed_y_line.animate.set_opacity(0), run_time=1)
        self.remove(fixed_x_line, fixed_y_line)
        self.wait(2)

        dot_opacity_tracker = ValueTracker(0)
        sin1_graph = always_redraw(lambda: axes.plot(lambda x: np.sin(x), [0, t_tracker.get_value()], color=GREEN))
        fixed_sin1_graph = axes.plot(lambda x: np.sin(x), [0, 2*PI], color=GREEN).set_stroke(opacity=0.3)
        sin1_dot = always_redraw(lambda: Dot(color=RED, fill_opacity=dot_opacity_tracker.get_value()).move_to(axes.c2p(t_tracker.get_value(), np.sin(t_tracker.get_value()))))
        sin1_v_line = always_redraw(lambda: DashedLine(color=GREEN).put_start_and_end_on(axes.c2p(t_tracker.get_value(), 0), sin1_dot.get_center()).set_opacity(dot_opacity_tracker.get_value()))
        sin1_h_line = always_redraw(lambda: DashedLine(color=RED).put_start_and_end_on(p_dot.get_center(), sin1_dot.get_center()).set_opacity(dot_opacity_tracker.get_value()))

        self.add(sin1_dot, sin1_v_line, sin1_h_line)
        self.play(Restore(self.camera.frame), t_tracker.animate.set_value(0), dot_opacity_tracker.animate.set_value(1), FadeOut(p_dot_label))
        self.wait(2)
        self.add(sin1_graph)
        self.play(t_tracker.animate.set_value(2*PI), run_time=6, rate_func=linear)
        self.wait(3)
        self.add(fixed_sin1_graph)
        self.play(FadeOut(sin1_graph), t_tracker.animate.set_value(0), dot_opacity_tracker.animate.set_value(0))
        self.remove(sin1_dot, sin1_v_line, sin1_h_line)
        self.wait(2)

        sin2_graph = always_redraw(lambda: axes.plot(lambda x: np.sin(2*x), [0, t_tracker.get_value()], color=BLUE))
        fixed_sin2_graph = axes.plot(lambda x: np.sin(2*x), [0, 2*PI], color=BLUE).set_stroke(opacity=0.3)
        sin2_dot = always_redraw(lambda: Dot(color=RED, fill_opacity=dot_opacity_tracker.get_value()).move_to(axes.c2p(t_tracker.get_value(), np.sin(2*t_tracker.get_value()))))
        sin2_v_line = always_redraw(lambda: DashedLine(color=GREEN).put_start_and_end_on(axes.c2p(t_tracker.get_value(), 0), sin2_dot.get_center()).set_opacity(dot_opacity_tracker.get_value()))
        sin2_h_line = always_redraw(lambda: DashedLine(color=RED).put_start_and_end_on(p_dot.get_center(), sin2_dot.get_center()).set_opacity(dot_opacity_tracker.get_value()))

        omega_tracker.set_value(2)
        self.add(sin2_dot, sin2_v_line, sin2_h_line)
        self.play(dot_opacity_tracker.animate.set_value(1))
        self.wait(2)
        self.add(sin2_graph)
        self.play(t_tracker.animate.set_value(2*PI), run_time=6, rate_func=linear)
        self.wait(3)
        self.add(fixed_sin2_graph)
        self.play(FadeOut(sin2_graph), t_tracker.animate.set_value(0), dot_opacity_tracker.animate.set_value(0))
        self.remove(sin2_dot, sin2_v_line, sin2_h_line)
        self.wait(2)

        sin3_graph = always_redraw(lambda: axes.plot(lambda x: np.sin(2/3*x), [0, t_tracker.get_value()], color=YELLOW))
        fixed_sin3_graph = axes.plot(lambda x: np.sin(2/3*x), [0, 3*PI], color=YELLOW).set_stroke(opacity=0.3)
        sin3_dot = always_redraw(lambda: Dot(color=RED, fill_opacity=dot_opacity_tracker.get_value()).move_to(axes.c2p(t_tracker.get_value(), np.sin(2/3*t_tracker.get_value()))))
        sin3_v_line = always_redraw(lambda: DashedLine(color=GREEN).put_start_and_end_on(axes.c2p(t_tracker.get_value(), 0), sin3_dot.get_center()).set_opacity(dot_opacity_tracker.get_value()))
        sin3_h_line = always_redraw(lambda: DashedLine(color=RED).put_start_and_end_on(p_dot.get_center(), sin3_dot.get_center()).set_opacity(dot_opacity_tracker.get_value()))
        
        omega_tracker.set_value(2/3)
        self.add(sin3_dot, sin3_v_line, sin3_h_line)
        self.play(dot_opacity_tracker.animate.set_value(1))
        self.wait(2)
        self.add(sin3_graph)
        self.play(t_tracker.animate.set_value(3*PI), run_time=9, rate_func=linear)
        self.wait(3)
        self.add(fixed_sin3_graph)
        self.play(FadeOut(sin3_graph), t_tracker.animate.set_value(0), dot_opacity_tracker.animate.set_value(0))
        self.remove(sin3_dot, sin3_v_line, sin3_h_line)
        self.wait(2)

        omega_tracker.set_value(1)
        omega_slider = SliderComponent(
            r"\omega",
            omega_tracker,
            0,
            4.
        ).to_corner(UR, buff=0.5)
        sin_scale_graph = always_redraw(lambda: axes.plot(lambda x: r_tracker.get_value()*np.sin(omega_tracker.get_value()*x+phi_tracker.get_value()), [0, 2*PI], color=GREEN))
        self.play(FadeOut(fixed_sin1_graph), FadeOut(fixed_sin2_graph), FadeOut(fixed_sin3_graph), Create(omega_slider), FadeIn(sin_scale_graph))
        self.wait(2)
        self.play(omega_tracker.animate.set_value(3), run_time=6)
        self.wait(2)
        self.play(omega_tracker.animate.set_value(2), run_time=6)
        self.wait(2)

        t_formula = MathTex(r"t = \frac{s}{v} \rightarrow T = \frac{2\pi}{\omega}", font_size=40).to_edge(UP, buff=0.5)
        self.play(Write(t_formula))
        self.wait(5)
        self.play(FadeOut(t_formula))





        func_formula = MathTex(r"f(x) = ","A",r"\sin(","\omega","x + ",r"\phi",")", font_size=40).set_color_by_tex_to_color_map({
            "A": GREEN,
            "\omega": BLUE,
            "\phi": YELLOW
        }).to_corner(UL, buff=0.5)
        self.play(Write(func_formula))

        r_slider = SliderComponent(
            r"A",
            r_tracker,
            0,
            2.
        ).next_to(omega_slider, DOWN, buff=0.2)

        up_line = always_redraw(lambda: DashedLine(8*LEFT+UP*unit_len*r_tracker.get_value(), 8*RIGHT+UP*unit_len*r_tracker.get_value(), color=ORANGE).shift(DOWN))
        down_line = always_redraw(lambda: DashedLine(8*LEFT+DOWN*unit_len*r_tracker.get_value(), 8*RIGHT+DOWN*unit_len*r_tracker.get_value(), color=ORANGE).shift(DOWN))
        self.play(Create(up_line), Create(down_line), Create(r_slider), omega_tracker.animate.set_value(1))
        self.wait(2)

        self.play(r_tracker.animate.set_value(1.5), run_time=6)
        self.wait(2)
        self.play(r_tracker.animate.set_value(0.5), run_time=6)
        self.wait(4)

        self.play(FadeOut(up_line), FadeOut(down_line), r_tracker.animate.set_value(1))
        self.wait(2)

        phi_slider = SliderComponent(
            r"\phi",
            phi_tracker,
            0,
            2*PI
        ).next_to(r_slider, DOWN, buff=0.2)

        sin_scale_dot = always_redraw(lambda: Dot(color=RED, fill_opacity=dot_opacity_tracker.get_value()).move_to(axes.c2p(0, r_tracker.get_value()*np.sin(phi_tracker.get_value()))))
        sin_scale_v_line = always_redraw(lambda: DashedLine(color=GREEN).put_start_and_end_on(axes.c2p(0, 0), sin_scale_dot.get_center()).set_opacity(dot_opacity_tracker.get_value()))
        sin_scale_h_line = always_redraw(lambda: DashedLine(color=RED).put_start_and_end_on(p_dot.get_center(), sin_scale_dot.get_center()).set_opacity(dot_opacity_tracker.get_value()))

        self.add(sin_scale_dot, sin_scale_v_line, sin_scale_h_line)
        self.play(Create(phi_slider), dot_opacity_tracker.animate.set_value(1))
        self.wait(1)
        self.play(phi_tracker.animate.set_value(PI/3*2), run_time=3)
        self.play(phi_tracker.animate.set_value(-PI/2), run_time=3)
        self.play(phi_tracker.animate.set_value(PI/4), run_time=3)
        self.wait(2)
        self.play(phi_tracker.animate.set_value(PI/3), run_time=6)
        self.wait(4)

        self.play(phi_tracker.animate.set_value(0), run_time=2)
        self.wait(4)

        new_func_formula = MathTex(r"f(x) = ",r"\frac{5}{3}",r"\sin(","2","x + ",r"\frac{\pi}{3}",")", font_size=40).set_color_by_tex_to_color_map({
            r"\frac{5}{3}": GREEN,
            "2": BLUE,
            r"\frac{\pi}{3}": YELLOW
        }).to_corner(UL, buff=0.5)
        self.play(Transform(func_formula, new_func_formula))
        self.wait(3)
        self.play(new_func_formula.animate.set_color_by_tex(r"\frac{5}{3}", GREEN_A), run_time=1)
        self.play(new_func_formula.animate.set_color_by_tex(r"\frac{5}{3}", GREEN), run_time=1)
        self.wait(3)
        self.play(new_func_formula.animate.set_color_by_tex_to_color_map({r"2": BLUE_A}), run_time=1)
        self.play(new_func_formula.animate.set_color_by_tex_to_color_map({r"2": BLUE}), run_time=1)
        self.wait(3)
        self.play(new_func_formula.animate.set_color_by_tex(r"\frac{\pi}{3}", WHITE), run_time=1)
        self.play(new_func_formula.animate.set_color_by_tex(r"\frac{\pi}{3}", YELLOW), run_time=1)
        self.wait(4)

        self.play(r_tracker.animate.set_value(5/3), run_time=4)
        self.wait(3)
        self.play(phi_tracker.animate.set_value(PI/3), run_time=4)
        self.wait(3)
        self.play(omega_tracker.animate.set_value(2), run_time=4)
        self.wait(5)
        


        



