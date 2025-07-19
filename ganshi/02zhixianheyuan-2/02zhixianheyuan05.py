from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle

class Xianyuyuan05(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-7, 7, 0.5],
            y_range=[-7, 7, 0.5],
            x_length=8,
            y_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )

        self.add(axes)

        l_line = LinearFunctionPointSlope((0,2), np.atan(1.732))
        l_graph = l_line.plot_in(axes, [-7, 7], [-7, 7], color=WHITE, stroke_width=2, stroke_opacity=1)
        ld1_line = LinearFunctionPointSlope((0,2+2), np.atan(1.732)+PI)
        ld1_graph = ld1_line.plot_in(axes, [-7, 7], [-7, 7], color=GREEN, stroke_width=2, stroke_opacity=1)
        ld2_line = LinearFunctionPointSlope((0,2-2), np.atan(1.732)-PI)
        ld2_graph = ld2_line.plot_in(axes, [-7, 7], [-7, 7], color=GREEN, stroke_width=2, stroke_opacity=1)
        d_line = Line(color=RED).put_start_and_end_on(axes.c2p(-0.866,0.5+2), axes.c2p(0.866,-0.5+2))
        self.play(Create(l_graph))
        self.wait(2)
        self.play(Create(ld1_graph), Create(ld2_graph), Create(d_line))
        self.wait(2)

        r_tracker = ValueTracker(2)
        r_slider = SliderComponent(
            "r",
            r_tracker,
            0,
            4,
        ).to_corner(UR, buff=0.5)
        circ = CustomCircle((0,-2), r_tracker)
        circ_graph = always_redraw(lambda: circ.plot_in(axes, color=WHITE, stroke_width=2, stroke_opacity=1))
        circ_center_dot = always_redraw(lambda: circ.get_center_dot(axes, color=WHITE, radius=0.05))
        self.play(Create(circ_graph), Create(circ_center_dot), FadeOut(d_line), Create(r_slider))
        self.wait(2)

        def get_cross_dot():
            r = r_tracker.get_value()
            if r < 1:
                return VGroup()
            elif r < 3:
                dot1 = Dot(color=BLUE).move_to(axes.c2p((-1.732-np.sqrt(r*r-1))/2, (-3-1.732*np.sqrt(r*r-1))/2))
                dot2 = Dot(color=BLUE).move_to(axes.c2p((-1.732+np.sqrt(r*r-1))/2, (-3+1.732*np.sqrt(r*r-1))/2))
                return VGroup(dot1, dot2)
            else:
                dot1 = Dot(color=BLUE).move_to(axes.c2p((-1.732-np.sqrt(r*r-1))/2, (-3-1.732*np.sqrt(r*r-1))/2))
                dot2 = Dot(color=BLUE).move_to(axes.c2p((-1.732+np.sqrt(r*r-1))/2, (-3+1.732*np.sqrt(r*r-1))/2))
                dot3 = Dot(color=BLUE).move_to(axes.c2p((-1.732*3-np.sqrt(r*r-9))/2, (-3*3-1.732*np.sqrt(r*r-9))/2+4))
                dot4 = Dot(color=BLUE).move_to(axes.c2p((-1.732*3+np.sqrt(r*r-9))/2, (-3*3+1.732*np.sqrt(r*r-9))/2+4))
                return VGroup(dot1, dot2, dot3, dot4)

        cross_dot = always_redraw(get_cross_dot)
        self.play(Create(cross_dot))
        self.wait(2)

        self.play(r_tracker.animate.set_value(1), run_time=6)
        collision_effect = CollisionEffect(axes.c2p((-1.732)/2, (-3)/2))
        self.add(collision_effect.get_lines())
        self.play(collision_effect.get_animation())
        self.remove(collision_effect.get_lines())
        self.wait(3)

        self.play(r_tracker.animate.set_value(4), run_time=4)
        self.wait(3)
        self.play(r_tracker.animate.set_value(3), run_time=4)
        collision_effect = CollisionEffect(axes.c2p((-1.732*3)/2, (-3*3)/2+4))
        self.add(collision_effect.get_lines())
        self.play(collision_effect.get_animation())
        self.remove(collision_effect.get_lines())
        self.wait(3)
