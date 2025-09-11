from manim import *
import numpy as np
from modules import *

class LiveExample1(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-PI/3, 2*PI],
            y_range=[-2, 2],
            x_length=12,
            origin_point=4*LEFT+DOWN,
            axis_config={"include_tip": True, "tip_length": 0.15}
        )

        self.play(Create(axes))

        omega_tracker = ValueTracker(1)
        bias_tracker = ValueTracker(PI/3)

        omega_slider = always_redraw(lambda: SliderComponent(
            param_name=r"\omega",
            param_color=YELLOW,
            value_tracker=omega_tracker,
            min_val=0,
            max_val=4,
            track_color=WHITE,
            slider_color=YELLOW,
            use_modulo=False,
        ).to_edge(RIGHT+UP))

        def func(x):
            return np.sin(omega_tracker.get_value()*x + bias_tracker.get_value())
        
        pi_tracker = ValueTracker(PI)
        pi_line = always_redraw(lambda: Line(axes.c2p(pi_tracker.get_value(), -2), axes.c2p(pi_tracker.get_value(), 2), color=RED))
        pi_dot = always_redraw(lambda: Dot(axes.c2p(pi_tracker.get_value(), 0), color=RED))
        pi_label = always_redraw(lambda: MathTex(r"\pi", color=RED).next_to(pi_dot, DOWN+RIGHT))
        func_label = always_redraw(lambda: MathTex(r"f(x) = \sin(", r"\omega", r"x + \frac{\pi}{3})", color=BLUE).set_color_by_tex(r"\omega", YELLOW).to_edge(UP+LEFT))

        func_graph = always_redraw(lambda: axes.plot(func, color=BLUE))
        self.play(Create(func_graph), Create(func_label), Create(omega_slider))

        dot_opacity_tracker = ValueTracker(0)

        ex1_dot = always_redraw(lambda: Dot(axes.c2p((PI/2-bias_tracker.get_value())/omega_tracker.get_value(), func((PI/2-bias_tracker.get_value())/omega_tracker.get_value())), color=GREEN, fill_opacity=dot_opacity_tracker.get_value()))
        ex2_dot = always_redraw(lambda: Dot(axes.c2p((3*PI/2-bias_tracker.get_value())/omega_tracker.get_value(), func((3*PI/2-bias_tracker.get_value())/omega_tracker.get_value())), color=GREEN, fill_opacity=dot_opacity_tracker.get_value()))
        ex3_dot = always_redraw(lambda: Dot(axes.c2p((5*PI/2-bias_tracker.get_value())/omega_tracker.get_value(), func((5*PI/2-bias_tracker.get_value())/omega_tracker.get_value())), color=GREEN, fill_opacity=dot_opacity_tracker.get_value()))
        ex4_dot = always_redraw(lambda: Dot(axes.c2p((7*PI/2-bias_tracker.get_value())/omega_tracker.get_value(), func((7*PI/2-bias_tracker.get_value())/omega_tracker.get_value())), color=GREEN, fill_opacity=dot_opacity_tracker.get_value()))

        zero1_dot = always_redraw(lambda: Dot(axes.c2p((PI-bias_tracker.get_value())/omega_tracker.get_value(), 0), color=GREEN_A, fill_opacity=dot_opacity_tracker.get_value()))
        zero2_dot = always_redraw(lambda: Dot(axes.c2p((2*PI-bias_tracker.get_value())/omega_tracker.get_value(), 0), color=GREEN_A, fill_opacity=dot_opacity_tracker.get_value()))
        zero3_dot = always_redraw(lambda: Dot(axes.c2p((3*PI-bias_tracker.get_value())/omega_tracker.get_value(), 0), color=GREEN_A, fill_opacity=dot_opacity_tracker.get_value()))
        clip_line1 = always_redraw(lambda: DashedLine(axes.c2p((-bias_tracker.get_value())/omega_tracker.get_value(), -2), axes.c2p((-bias_tracker.get_value())/omega_tracker.get_value(), 2), color=GREEN_A))
        clip_line2 = always_redraw(lambda: DashedLine(axes.c2p((2*PI-bias_tracker.get_value())/omega_tracker.get_value(), -2), axes.c2p((2*PI-bias_tracker.get_value())/omega_tracker.get_value(), 2), color=GREEN_A))
        left_range_line = always_redraw(lambda: Line(color=YELLOW).put_start_and_end_on(axes.c2p(0, 0), axes.c2p((-bias_tracker.get_value())/omega_tracker.get_value(), 0)))
        right_range_line = always_redraw(lambda: Line(color=YELLOW).put_start_and_end_on(axes.c2p(0, 0), axes.c2p((2*PI-bias_tracker.get_value())/omega_tracker.get_value(), 0)))
        left_range_label = always_redraw(lambda: MathTex(r"\frac16T", color=GREEN, font_size=25).move_to(axes.c2p((-bias_tracker.get_value())/omega_tracker.get_value()/2, 1.5)))
        right_range_label = always_redraw(lambda: MathTex(r"\frac56T", color=GREEN, font_size=25).move_to(axes.c2p((2*PI-bias_tracker.get_value())/omega_tracker.get_value()/2, 1.5)))

        tmp_width = 0.2
        left_larrow = always_redraw(lambda: Arrow(color=GREEN, stroke_width=1, tip_length=0.1).put_start_and_end_on(axes.c2p((-bias_tracker.get_value())/omega_tracker.get_value()/2, 1.5)+tmp_width*LEFT, axes.c2p(-bias_tracker.get_value()/omega_tracker.get_value(), 1.5)))
        left_rarrow = always_redraw(lambda: Arrow(color=GREEN, stroke_width=1, tip_length=0.1).put_start_and_end_on(axes.c2p((-bias_tracker.get_value())/omega_tracker.get_value()/2, 1.5)+tmp_width*RIGHT, axes.c2p(0, 1.5)))
        right_larrow = always_redraw(lambda: Arrow(color=GREEN, stroke_width=1, tip_length=0.1).put_start_and_end_on(axes.c2p((2*PI-bias_tracker.get_value())/omega_tracker.get_value()/2, 1.5)+tmp_width*LEFT, axes.c2p(0, 1.5)))
        right_rarrow = always_redraw(lambda: Arrow(color=GREEN, stroke_width=1, tip_length=0.1).put_start_and_end_on(axes.c2p((2*PI-bias_tracker.get_value())/omega_tracker.get_value()/2, 1.5)+tmp_width*RIGHT, axes.c2p((2*PI-bias_tracker.get_value())/omega_tracker.get_value(), 1.5)))

        self.play(Create(clip_line1), Create(clip_line2), Create(left_range_line), Create(right_range_line), Create(left_range_label), Create(right_range_label), Create(left_larrow), Create(left_rarrow), Create(right_larrow), Create(right_rarrow))
        self.wait(2)

        self.play(omega_tracker.animate.set_value(4), run_time=8)
        self.wait(2)

        self.play(omega_tracker.animate.set_value(2), run_time=8)
        self.wait(2)

        self.play(Create(pi_line), Create(pi_dot), Create(pi_label))
        self.add(ex1_dot, ex2_dot, ex3_dot, ex4_dot, zero1_dot, zero2_dot, zero3_dot)
        self.play(dot_opacity_tracker.animate.set_value(1), run_time=2)
        self.wait(2)

        self.play(omega_tracker.animate.set_value(13/6), run_time=10)
        collision_effect = CollisionEffect(
            center_point=ex3_dot.get_center(),
            inner_radius=0.1,
            outer_radius=0.24,
            color=YELLOW,
            stroke_width=2,
        )
        self.add(collision_effect.get_lines())
        self.play(collision_effect.get_animation())
        self.remove(collision_effect.get_lines())

        t_div_4_label = MathTex(r"\frac{T}{4}", color=GREEN, font_size=25).move_to(axes.c2p((2*PI+PI/4-bias_tracker.get_value())/omega_tracker.get_value(), 1.5))
        larrow1 = Arrow(color=GREEN, stroke_width=1, tip_length=0.1).put_start_and_end_on(axes.c2p((2*PI+PI/4-bias_tracker.get_value())/omega_tracker.get_value(), 1.5)+tmp_width*LEFT, axes.c2p((2*PI-bias_tracker.get_value())/omega_tracker.get_value(), 1.5))
        rarrow1 = Arrow(color=GREEN, stroke_width=1, tip_length=0.1).put_start_and_end_on(axes.c2p((2*PI+PI/4-bias_tracker.get_value())/omega_tracker.get_value(), 1.5)+tmp_width*RIGHT, axes.c2p((2*PI+PI/2-bias_tracker.get_value())/omega_tracker.get_value(), 1.5))
        self.play(Create(t_div_4_label), Create(larrow1), Create(rarrow1))
        self.wait(4)
        self.play(
            FadeOut(t_div_4_label),
            FadeOut(larrow1),
            FadeOut(rarrow1),
            omega_tracker.animate.set_value(8/3), run_time=10)
        collision_effect = CollisionEffect(
            center_point=zero3_dot.get_center(),
            inner_radius=0.1,
            outer_radius=0.24,
            color=YELLOW,
            stroke_width=2,
        )
        self.add(collision_effect.get_lines())
        self.play(collision_effect.get_animation())
        self.remove(collision_effect.get_lines())
        
        t_div_2_label = MathTex(r"\frac{T}{2}", color=GREEN, font_size=25).move_to(axes.c2p((2*PI+PI/2-bias_tracker.get_value())/omega_tracker.get_value(), 1.5))
        larrow2 = Arrow(color=GREEN, stroke_width=1, tip_length=0.1).put_start_and_end_on(axes.c2p((2*PI+PI/2-bias_tracker.get_value())/omega_tracker.get_value(), 1.5)+tmp_width*LEFT, axes.c2p((2*PI-bias_tracker.get_value())/omega_tracker.get_value(), 1.5))
        rarrow2 = Arrow(color=GREEN, stroke_width=1, tip_length=0.1).put_start_and_end_on(axes.c2p((2*PI+PI/2-bias_tracker.get_value())/omega_tracker.get_value(), 1.5)+tmp_width*RIGHT, axes.c2p((2*PI+PI-bias_tracker.get_value())/omega_tracker.get_value(), 1.5))
        self.play(Create(t_div_2_label), Create(larrow2), Create(rarrow2))
        self.wait(4)
        self.play(
            FadeOut(t_div_2_label),
            FadeOut(larrow2),
            FadeOut(rarrow2),
            omega_tracker.animate.set_value(13/6), run_time=10)
        self.wait(2)