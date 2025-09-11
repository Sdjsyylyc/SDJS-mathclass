from manim import *
from modules.custom_axes import CustomAxes
from modules.slider_component import SliderComponent
from modules.function_definitions import *
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
        self.play(Create(axes))
        self.wait()

        a_tracker = ValueTracker(2.5)
        b_tracker = ValueTracker(2.5)
        p_tracker = ValueTracker(PI/2)
        
        m_point = always_redraw(lambda: Dot(color=YELLOW).move_to(axes.c2p(-a_tracker.get_value(), 0)))
        n_point = always_redraw(lambda: Dot(color=YELLOW).move_to(axes.c2p(a_tracker.get_value(), 0)))
        m_label = always_redraw(lambda: MathTex("M", color=YELLOW).next_to(m_point, DOWN))
        n_label = always_redraw(lambda: MathTex("N", color=YELLOW).next_to(n_point, DOWN))
        self.play(Create(m_point), Create(m_label), Create(n_point), Create(n_label))
        self.wait()

        ellipse = Ellipse(a=a_tracker, b=b_tracker)
        ellipse_graph = always_redraw(lambda: ellipse.plot_in(axes, color=BLUE, stroke_width=2, stroke_opacity=1))
        circle_graph = ellipse.plot_in(axes, color=BLUE, stroke_width=2, stroke_opacity=0.5)
        self.play(Create(ellipse_graph))
        self.wait()

        ellipse_func = ellipse.get_parametric_function()
        p_point = always_redraw(lambda: Dot(color=ORANGE).move_to(axes.coords_to_point(ellipse_func(p_tracker.get_value())[0], ellipse_func(p_tracker.get_value())[1])))
        p_label = always_redraw(lambda: MathTex("P", color=ORANGE).next_to(p_point, DOWN))
        self.play(Create(p_point), Create(p_label))
        self.wait()

        mp_line = always_redraw(lambda: Line(m_point.get_center(), p_point.get_center(), color=ORANGE))
        np_line = always_redraw(lambda: Line(n_point.get_center(), p_point.get_center(), color=ORANGE))
        k1_label = always_redraw(lambda: MathTex("k_1", color=ORANGE).move_to(mp_line.get_center()+0.5*UP))
        k2_label = always_redraw(lambda: MathTex("k_2", color=ORANGE).move_to(np_line.get_center()+0.5*UP))
        self.play(Create(mp_line), Create(np_line), Create(k1_label), Create(k2_label))
        self.wait()

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
        self.wait()

        k_value_text = always_redraw(
            lambda: VGroup(MathTex("k_1k_2 = "), DecimalNumber(-(b_tracker.get_value()/a_tracker.get_value())**2, num_decimal_places=2)).arrange(RIGHT).to_edge(UP+RIGHT, buff=0.5)
        )
        ph_line = always_redraw(lambda: DashedLine(p_point.get_center(), axes.c2p(ellipse_func(p_tracker.get_value())[0], 0), color=ORANGE))
        mh_line = always_redraw(lambda: DashedLine(m_point.get_center(), axes.c2p(ellipse_func(p_tracker.get_value())[0], 0), color=ORANGE))
        nh_line = always_redraw(lambda: DashedLine(n_point.get_center(), axes.c2p(ellipse_func(p_tracker.get_value())[0], 0), color=ORANGE))
        self.play(Create(k_value_text), Create(ph_line), Create(mh_line), Create(nh_line))
        self.wait()

        self.play(p_tracker.animate.set_value(PI/3+2*PI), run_time=5)
        self.wait()

        self.add(circle_graph)
        self.play(FadeOut(rec_angle), b_tracker.animate.set_value(1.5), run_time=4)
        self.wait()

        self.play(p_tracker.animate.set_value(PI/3+4*PI), run_time=5)
        self.wait(4)

        self.play(FadeOut(circle_graph), b_tracker.animate.set_value(2.5),
                  FadeOut(m_label), FadeOut(n_label), FadeOut(m_point), FadeOut(n_point),
                  FadeOut(mp_line), FadeOut(np_line),
                  FadeOut(k1_label), FadeOut(k2_label),
                  FadeOut(ph_line), FadeOut(mh_line), FadeOut(nh_line),
                  run_time=2)
        
        o_point = Dot(color=WHITE).move_to(axes.c2p(0, 0))
        o_label = MathTex("O", color=WHITE).next_to(o_point, DOWN+RIGHT)
        self.play(Create(o_point), Create(o_label))
        self.wait()
        op_line = always_redraw(lambda: Line(o_point.get_center(), p_point.get_center(), color=ORANGE))
        tangent_line = always_redraw(lambda: ellipse.get_tangent_line(axes, p_tracker.get_value(), color=ORANGE, stroke_width=2, length=4))
        k1_label = always_redraw(lambda: MathTex("k_1", color=ORANGE).move_to(op_line.get_center()+0.5*UP))
        k2_label = always_redraw(lambda: MathTex("k_2", color=ORANGE).move_to(tangent_line.get_center()+0.5*UP))
        self.play(Create(op_line), Create(tangent_line), Create(k1_label), Create(k2_label))
        self.wait()
        self.play(p_tracker.animate.set_value(PI/3+6*PI), run_time=5)
        self.wait(4)
        
        self.add(circle_graph)
        self.play(b_tracker.animate.set_value(1.5), run_time=4)
        self.wait()
        self.play(p_tracker.animate.set_value(PI/3+8*PI), run_time=5)
        self.wait(4)

