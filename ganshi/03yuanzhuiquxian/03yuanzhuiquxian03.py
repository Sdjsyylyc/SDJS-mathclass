from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints, Ellipse, Parabola

class Yuanzhuiquxian03(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            x_length=7,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        axes.move_to(ORIGIN)
        self.add(axes)

        a_tracker = ValueTracker(2)
        b_tracker = ValueTracker(2)
        p_tracker = ValueTracker(PI/3)

        ellipse = Ellipse(a=a_tracker, b=b_tracker)
        ellipse_graph = always_redraw(lambda: ellipse.plot_in(axes, color=BLUE, stroke_width=2, stroke_opacity=1))
        circle_graph = ellipse.plot_in(axes, color=BLUE, stroke_width=2, stroke_opacity=0.5)
        self.add(ellipse_graph)
        self.wait()

        ellipse_func = ellipse.get_parametric_function()
        p_point = always_redraw(lambda: Dot(color=ORANGE).move_to(axes.coords_to_point(ellipse_func(p_tracker.get_value())[0], ellipse_func(p_tracker.get_value())[1])))
        p_label = always_redraw(lambda: MathTex("M", color=ORANGE).next_to(p_point, UP))
        self.play(Create(p_point), Create(p_label))
        self.wait()
        
        m_point = always_redraw(lambda: Dot(color=YELLOW).move_to(axes.c2p(-a_tracker.get_value(), 0)))
        n_point = always_redraw(lambda: Dot(color=YELLOW).move_to(axes.c2p(a_tracker.get_value(), 0)))
        m_label = always_redraw(lambda: MathTex("A", color=YELLOW).next_to(m_point, DOWN))
        n_label = always_redraw(lambda: MathTex("B", color=YELLOW).next_to(n_point, DOWN))
        self.play(Create(m_point), Create(m_label), Create(n_point), Create(n_label))
        self.wait(2)

        mp_line = always_redraw(lambda: Line(m_point.get_center(), p_point.get_center(), color=ORANGE))
        np_line = always_redraw(lambda: Line(n_point.get_center(), p_point.get_center(), color=ORANGE))
        fixed_mp_line = Line(m_point.get_center(), p_point.get_center(), color=ORANGE, stroke_opacity=0.5)
        fixed_np_line = Line(n_point.get_center(), p_point.get_center(), color=ORANGE, stroke_opacity=0.5)
        k1_label = always_redraw(lambda: MathTex("k_1", color=ORANGE).move_to(mp_line.get_center()+0.5*UP))
        k2_label = always_redraw(lambda: MathTex("k_2", color=ORANGE).move_to(np_line.get_center()+0.5*UP))
        self.play(Create(mp_line), Create(np_line), Create(k1_label), Create(k2_label))
        self.wait(2)


        def create_right_angle():
            p_pos = p_point.get_center()
            m_pos = m_point.get_center()
            n_pos = n_point.get_center()
            
            mp_vec = (m_pos - p_pos)
            np_vec = (n_pos - p_pos)
            
            mp_len = np.linalg.norm(mp_vec)
            np_len = np.linalg.norm(np_vec)
            
            if mp_len > 0.001 and np_len > 0.001:
                mp_unit = mp_vec / mp_len
                np_unit = np_vec / np_len
                
                line_len = 0.3
                line1 = Line(p_pos, p_pos + line_len * mp_unit, color=ORANGE)
                line2 = Line(p_pos, p_pos + line_len * np_unit, color=ORANGE)
                
                try:
                    right_angle = RightAngle(line1, line2, length=0.2, color=ORANGE)
                    return right_angle
                except:
                    return VGroup()
            else:
                return VGroup()

        rec_angle = always_redraw(create_right_angle)
        self.play(Create(rec_angle))
        self.wait(2)

        k_value_text = always_redraw(lambda: MathTex(f"k_1k_2 = {-b_tracker.get_value()**2/a_tracker.get_value()**2:.2f}", color=ORANGE).to_corner(UR, buff=0.5))
        ph_line = always_redraw(lambda: DashedLine(p_point.get_center(), axes.c2p(ellipse_func(p_tracker.get_value())[0], 0), color=ORANGE))
        mh_line = always_redraw(lambda: DashedLine(m_point.get_center(), axes.c2p(ellipse_func(p_tracker.get_value())[0], 0), color=ORANGE))
        nh_line = always_redraw(lambda: DashedLine(n_point.get_center(), axes.c2p(ellipse_func(p_tracker.get_value())[0], 0), color=ORANGE))
        self.play(Create(k_value_text), Create(ph_line), Create(mh_line), Create(nh_line))
        self.wait()

        self.play(p_tracker.animate.set_value(PI/3+2*PI), run_time=5)
        self.wait()

        next_opacity = ValueTracker(0)
        a_line = always_redraw(lambda: Line(color=YELLOW, stroke_opacity=next_opacity.get_value()).put_start_and_end_on(axes.c2p(a_tracker.get_value(), 0), axes.c2p(0, 0)))
        a_label = always_redraw(lambda: MathTex("a", color=YELLOW, fill_opacity=next_opacity.get_value()).next_to(a_line, DOWN))
        b_line = always_redraw(lambda: Line(color=YELLOW, stroke_opacity=next_opacity.get_value()).put_start_and_end_on(axes.c2p(0, b_tracker.get_value()), axes.c2p(0, 0)))
        b_label = always_redraw(lambda: MathTex("b", color=YELLOW, fill_opacity=next_opacity.get_value()).next_to(b_line, LEFT))
        k1n_label = always_redraw(lambda: MathTex("k_1", color=ORANGE, fill_opacity=next_opacity.get_value()).move_to(mp_line.get_center()+0.5*UP))
        k2n_label = always_redraw(lambda: MathTex("k_2", color=ORANGE, fill_opacity=next_opacity.get_value()).move_to(np_line.get_center()+0.5*UP))
        self.add(circle_graph, fixed_mp_line, fixed_np_line, k1n_label, k2n_label, a_line, a_label, b_line, b_label)
        self.play(FadeOut(rec_angle), FadeOut(k1_label), FadeOut(k2_label), b_tracker.animate.set_value(1.5), next_opacity.animate.set_value(np.sqrt(2)),
                  run_time=4)
        self.wait()

        self.play(p_tracker.animate.set_value(PI/3+4*PI), run_time=5)
        self.wait(4)

