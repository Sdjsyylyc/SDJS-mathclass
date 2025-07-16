from manim import *
import numpy as np
from modules import *

class LiveExample2(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-2, 2],
            y_range=[-2, 2],
            x_length=6,
            y_length=6,
            origin_point=ORIGIN,
            axis_config={"include_tip": True, "tip_length": 0.15}
        )

        o_dot = always_redraw(lambda: Dot(color=WHITE).move_to(axes.c2p(0, 0)))
        o_label = always_redraw(lambda: MathTex(r"O", color=WHITE).next_to(o_dot, UP+RIGHT))

        unit_length = axes.get_x_unit()

        self.play(Create(axes), Create(o_dot), Create(o_label))
        
        ppos_tracker = ValueTracker(PI/3)
        p_dot = always_redraw(lambda: Dot(color=RED).move_to(np.sqrt(2)*axes.c2p(np.cos(ppos_tracker.get_value()), np.sin(ppos_tracker.get_value()))))
        p_label = always_redraw(lambda: MathTex(r"P", color=RED).next_to(p_dot, UP+RIGHT))
        a_dot = always_redraw(lambda: Dot(color=BLUE).move_to(axes.c2p(np.cos(ppos_tracker.get_value()+PI/4), np.sin(ppos_tracker.get_value()+PI/4))))
        a_label = always_redraw(lambda: MathTex(r"A", color=BLUE).next_to(a_dot, UP+RIGHT))

        d_tracker = ValueTracker(1/2)
        b_dot = always_redraw(lambda: Dot(color=GREEN).move_to(axes.c2p(np.cos(ppos_tracker.get_value()-np.acos(d_tracker.get_value()/np.sqrt(2))+np.acos(d_tracker.get_value())),
                                                                        np.sin(ppos_tracker.get_value()-np.acos(d_tracker.get_value()/np.sqrt(2))+np.acos(d_tracker.get_value())))))
        b_label = always_redraw(lambda: MathTex(r"B", color=GREEN).next_to(b_dot, UP+RIGHT))
        c_dot = always_redraw(lambda: Dot(color=GREEN).move_to(axes.c2p(np.cos(ppos_tracker.get_value()-np.acos(d_tracker.get_value()/np.sqrt(2))-np.acos(d_tracker.get_value())),
                                                                        np.sin(ppos_tracker.get_value()-np.acos(d_tracker.get_value()/np.sqrt(2))-np.acos(d_tracker.get_value())))))
        c_label = always_redraw(lambda: MathTex(r"C", color=GREEN).next_to(c_dot, UP+RIGHT))
        d_dot = always_redraw(lambda: Dot(color=PURPLE).move_to(d_tracker.get_value()*axes.c2p(np.cos(ppos_tracker.get_value()-np.acos(d_tracker.get_value()/np.sqrt(2))),
                                                                        np.sin(ppos_tracker.get_value()-np.acos(d_tracker.get_value()/np.sqrt(2))))))
        d_label = always_redraw(lambda: MathTex(r"D", color=PURPLE).next_to(d_dot, UP+RIGHT))

        pa_vec = always_redraw(lambda: Arrow(color=RED).put_start_and_end_on(p_dot.get_center(), a_dot.get_center()))
        pc_line = always_redraw(lambda: Line(color=RED).put_start_and_end_on(p_dot.get_center(), c_dot.get_center()))
        odp_triangle = always_redraw(lambda: Polygon(o_dot.get_center(), d_dot.get_center(), p_dot.get_center(), color=YELLOW))
        # odp_angle = always_redraw(lambda: RightAngle(dp_line, od_line, color=YELLOW))

        inner_circle = CustomCircle(center=[0,0], radius=1)
        inner_circle_graph = inner_circle.plot_in(axes, color=RED)
        outer_circle = CustomCircle(center=[0,0], radius=np.sqrt(2))
        outer_circle_graph = outer_circle.plot_in(axes, color=BLUE)
        trace_circle_graph = always_redraw(lambda: Circle(radius=np.sqrt(2)/2*unit_length, color=GREEN).move_to(np.sqrt(2)/2*axes.c2p(np.cos(ppos_tracker.get_value()), np.sin(ppos_tracker.get_value()))))

        self.play(Create(inner_circle_graph), Create(outer_circle_graph), Create(p_dot), Create(p_label))
        self.wait(2)

        self.play(Create(a_dot), Create(a_label), Create(pa_vec))
        self.wait(2)

        self.play(Create(b_dot), Create(b_label), Create(pc_line), Create(c_dot), Create(c_label), Create(d_dot), Create(d_label))
        self.wait(2)

        self.play(ppos_tracker.animate.set_value(PI/3+2*PI), run_time=4)
        self.wait(1)
        self.play(d_tracker.animate.set_value(0.1), run_time=4)
        self.play(d_tracker.animate.set_value(0.9), run_time=4)
        self.play(d_tracker.animate.set_value(0.5), run_time=4)
        self.wait(2)

        self.play(Create(odp_triangle))
        self.play(Create(trace_circle_graph))

        self.play(ppos_tracker.animate.set_value(PI/3), run_time=4)
        self.wait(2)
        self.play(d_tracker.animate.set_value(0.9), run_time=4)
        self.play(d_tracker.animate.set_value(-0.9), run_time=4)
        self.wait(1)
        
        self.play(d_tracker.animate.set_value(-0.5), run_time=4)
        self.wait(2)

