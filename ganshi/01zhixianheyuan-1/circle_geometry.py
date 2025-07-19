from manim import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import CustomAxes, SliderComponent, LinearFunctionPointSlope, CollisionEffect
import numpy as np

class ConicLocusAnimation(MovingCameraScene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-5, 5, 1], 
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=6,
            origin_point=ORIGIN,
            axis_labels=True,
            x_label="x",
            y_label="y",
        )
        o_point = Dot(color=WHITE).move_to(axes.c2p(0, 0))
        self.add(axes, o_point)

        a_tracker = ValueTracker(2.5)
        b_tracker = ValueTracker(2.5)
        p_tracker = ValueTracker(PI/3)

        ellipse = Ellipse(a=a_tracker, b=b_tracker)
        ellipse_graph = always_redraw(lambda: ellipse.plot_in(axes, color=BLUE, stroke_width=2, stroke_opacity=1))
        circle_graph = ellipse.plot_in(axes, color=BLUE, stroke_width=2, stroke_opacity=0.5)
        self.add(ellipse_graph)
        self.wait()

        ellipse_func = ellipse.get_parametric_function()
        p_point = always_redraw(lambda: Dot(color=ORANGE).move_to(axes.coords_to_point(ellipse_func(p_tracker.get_value())[0], ellipse_func(p_tracker.get_value())[1])))
        p_label = always_redraw(lambda: MathTex("P", color=ORANGE).next_to(p_point, UP))
        self.play(Create(p_point), Create(p_label))
        self.wait()

        t1_point = Dot(color=ORANGE).move_to(axes.c2p(ellipse_func(-PI/4)[0], ellipse_func(-PI/4)[1]))
        t2_point = Dot(color=ORANGE).move_to(axes.c2p(ellipse_func(-3*PI/4)[0], ellipse_func(-3*PI/4)[1]))
        pt1_line = always_redraw(lambda: Line(color=ORANGE).put_start_and_end_on(p_point.get_center(), t1_point.get_center()))
        pt2_line = always_redraw(lambda: Line(color=ORANGE).put_start_and_end_on(p_point.get_center(), t2_point.get_center()))
        ot1_line = always_redraw(lambda: Line(color=ORANGE).put_start_and_end_on(o_point.get_center(), t1_point.get_center()))
        ot2_line = always_redraw(lambda: Line(color=ORANGE).put_start_and_end_on(o_point.get_center(), t2_point.get_center()))
        self.play(Create(t1_point), Create(t2_point), Create(pt1_line), Create(pt2_line), Create(ot1_line), Create(ot2_line))
        self.wait()

        circ_corner = always_redraw(lambda: Angle(pt2_line, pt1_line, radius=0.2, color=ORANGE))
        circ_corner_label = always_redraw(lambda: MathTex("\\theta", color=ORANGE).next_to(circ_corner, DOWN))
        round_corner = always_redraw(lambda: Angle(ot2_line, ot1_line, radius=0.2, color=ORANGE))
        round_corner_label = always_redraw(lambda: MathTex("2\\theta", color=ORANGE).next_to(round_corner, DOWN))
        self.play(Create(circ_corner), Create(circ_corner_label), Create(round_corner), Create(round_corner_label))
        self.wait()

        self.play(p_tracker.animate.set_value(PI/3+PI/2), run_time=3)
        self.play(p_tracker.animate.set_value(PI/3-PI/4), run_time=3)
        self.play(p_tracker.animate.set_value(PI/3),
            FadeOut(t1_point),FadeOut(t2_point),FadeOut(pt1_line),FadeOut(pt2_line),FadeOut(ot1_line),FadeOut(ot2_line),
            FadeOut(circ_corner),FadeOut(circ_corner_label),FadeOut(round_corner),FadeOut(round_corner_label),
            run_time=2)
        self.wait(2)
        
        m_point = always_redraw(lambda: Dot(color=YELLOW).move_to(axes.c2p(-a_tracker.get_value(), 0)))
        n_point = always_redraw(lambda: Dot(color=YELLOW).move_to(axes.c2p(a_tracker.get_value(), 0)))
        m_label = always_redraw(lambda: MathTex("M", color=YELLOW).next_to(m_point, DOWN))
        n_label = always_redraw(lambda: MathTex("N", color=YELLOW).next_to(n_point, DOWN))
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

        k_value_text = MathTex("k_1k_2 = -1", color=ORANGE).to_edge(UP+RIGHT, buff=0.5)
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
        k1n_label = always_redraw(lambda: MathTex("k_1'", color=ORANGE, fill_opacity=next_opacity.get_value()).move_to(mp_line.get_center()+0.5*UP))
        k2n_label = always_redraw(lambda: MathTex("k_2'", color=ORANGE, fill_opacity=next_opacity.get_value()).move_to(np_line.get_center()+0.5*UP))
        self.add(circle_graph, fixed_mp_line, fixed_np_line, k1n_label, k2n_label, a_line, a_label, b_line, b_label)
        self.play(FadeOut(rec_angle), FadeOut(k1_label), FadeOut(k2_label), b_tracker.animate.set_value(1.5), a_tracker.animate.set_value(3), next_opacity.animate.set_value(1),
                  run_time=4)
        self.wait()

        self.play(p_tracker.animate.set_value(PI/3+4*PI), run_time=5)
        self.wait(4)

        self.play(FadeOut(circle_graph), FadeOut(fixed_mp_line), FadeOut(fixed_np_line), b_tracker.animate.set_value(2.5), a_tracker.animate.set_value(2.5),
                  FadeOut(m_label), FadeOut(n_label), FadeOut(m_point), FadeOut(n_point),
                  FadeOut(mp_line), FadeOut(np_line),
                  FadeOut(ph_line), FadeOut(mh_line), FadeOut(nh_line),
                  FadeOut(a_line), FadeOut(a_label), FadeOut(b_line), FadeOut(b_label),
                  FadeOut(k1n_label), FadeOut(k2n_label),
                  run_time=2)

        next_opacity.set_value(0)
        
        o_label = MathTex("O", color=WHITE).next_to(o_point, DOWN+RIGHT)
        self.play(Create(o_label))
        self.wait()
        op_line = always_redraw(lambda: Line(o_point.get_center(), p_point.get_center(), color=ORANGE))
        tangent_line = always_redraw(lambda: ellipse.get_tangent_line(axes, p_tracker.get_value(), color=ORANGE, stroke_width=2, length=4))
        fixed_op_line = Line(o_point.get_center(), p_point.get_center(), color=ORANGE, stroke_opacity=0.5)
        fixed_tangent_line = ellipse.get_tangent_line(axes, p_tracker.get_value(), color=ORANGE, stroke_width=2, length=4, stroke_opacity=0.5)
        k1_label = always_redraw(lambda: MathTex("k_1", color=ORANGE).move_to(op_line.get_center()+0.5*UP))
        k2_label = always_redraw(lambda: MathTex("k_2", color=ORANGE).move_to(tangent_line.get_center()+0.5*UP+0.5*RIGHT))
        self.play(Create(op_line), Create(tangent_line), Create(k1_label), Create(k2_label))
        self.wait()
        self.play(p_tracker.animate.set_value(PI/3+6*PI), run_time=5)
        self.wait(4)
        
        k1n_label = always_redraw(lambda: MathTex("k_1'", color=ORANGE, fill_opacity=next_opacity.get_value()).move_to(op_line.get_center()+0.5*UP))
        k2n_label = always_redraw(lambda: MathTex("k_2'", color=ORANGE, fill_opacity=next_opacity.get_value()).move_to(tangent_line.get_center()+0.5*UP+0.5*RIGHT))
        self.add(circle_graph, fixed_op_line, fixed_tangent_line, k1n_label, k2n_label, a_line, a_label, b_line, b_label)
        self.play(b_tracker.animate.set_value(1.5), a_tracker.animate.set_value(3),
                  FadeOut(k1_label), FadeOut(k2_label), next_opacity.animate.set_value(1),
                  run_time=4)
        self.wait()
        self.play(p_tracker.animate.set_value(PI/3+8*PI), run_time=5)
        self.wait(4)

