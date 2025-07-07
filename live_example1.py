from manim import *
import numpy as np
from modules import *

class LiveExample1(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-PI/3, 1.5*PI],
            y_range=[-2, 2],
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
        func_label = always_redraw(lambda: MathTex(r"f(x) = \sin(", r"\omega", r"x + \phi)", color=BLUE).set_color_by_tex(r"\omega", YELLOW).to_edge(UP+LEFT))

        func_graph = always_redraw(lambda: axes.plot(func, color=BLUE))
        self.play(Create(func_graph), Create(pi_line), Create(pi_dot), Create(pi_label), Create(func_label), Create(omega_slider))

        ex1_dot = always_redraw(lambda: Dot(axes.c2p((PI/2-bias_tracker.get_value())/omega_tracker.get_value(), func((PI/2-bias_tracker.get_value())/omega_tracker.get_value())), color=GREEN))
        ex2_dot = always_redraw(lambda: Dot(axes.c2p((3*PI/2-bias_tracker.get_value())/omega_tracker.get_value(), func((3*PI/2-bias_tracker.get_value())/omega_tracker.get_value())), color=GREEN))
        ex3_dot = always_redraw(lambda: Dot(axes.c2p((5*PI/2-bias_tracker.get_value())/omega_tracker.get_value(), func((5*PI/2-bias_tracker.get_value())/omega_tracker.get_value())), color=GREEN))
        ex4_dot = always_redraw(lambda: Dot(axes.c2p((7*PI/2-bias_tracker.get_value())/omega_tracker.get_value(), func((7*PI/2-bias_tracker.get_value())/omega_tracker.get_value())), color=GREEN))

        self.play(Create(ex1_dot), Create(ex2_dot), Create(ex3_dot), Create(ex4_dot))
        self.wait(2)

        self.play(omega_tracker.animate.set_value(13/6), run_time=4)
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
        self.wait(2)
        self.play(omega_tracker.animate.set_value(19/6), run_time=4)
        collision_effect = CollisionEffect(
            center_point=ex4_dot.get_center(),
            inner_radius=0.1,
            outer_radius=0.24,
            color=YELLOW,
            stroke_width=2,
        )
        self.add(collision_effect.get_lines())
        self.play(collision_effect.get_animation())
        self.remove(collision_effect.get_lines())
        self.wait(2)