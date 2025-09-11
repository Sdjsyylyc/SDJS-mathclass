from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints, Ellipse

class Yuanzhuiquxian02(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-6, 6],
            y_range=[-6, 6],
            x_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        axes.move_to(ORIGIN)
        self.add(axes)

        k_tracker = ValueTracker(-PI/3)

        circ = CustomCircle((-1,0), 4)
        circ_graph = circ.plot_in(axes)
        a_dot = circ.get_center_dot(axes)
        a_label = MathTex(f"A", color=WHITE).next_to(a_dot, DOWN)
        b_dot = Dot(color=WHITE).move_to(axes.c2p(1,0))
        b_label = MathTex(f"B", color=WHITE).next_to(b_dot, DOWN)

        def get_cde():
            k = np.tan(k_tracker.get_value())
            m = k**2
            xc = (m-1-2*np.sqrt(3*m+4))/(m+1)
            xd = (m-1+2*np.sqrt(3*m+4))/(m+1)
            yc = k*(xc-1)
            yd = k*(xd-1)
            if yc != 0:
                ye = (yc*yd)/(yc-yd)
                xe = yc/(yc-yd)*(xd+1)-1
            else:
                ye = 0
                xe = 2
            
            c_dot = Dot(color=WHITE).move_to(axes.c2p(xc, yc))
            c_label = MathTex(f"C", color=WHITE).next_to(c_dot, LEFT)
            d_dot = Dot(color=WHITE).move_to(axes.c2p(xd, yd))
            d_label = MathTex(f"D", color=WHITE).next_to(d_dot, RIGHT)
            e_dot = Dot(color=WHITE).move_to(axes.c2p(xe, ye))
            e_label = MathTex(f"E", color=WHITE).next_to(e_dot, DOWN)
            
            return VGroup(c_dot, d_dot, e_dot, c_label, d_label, e_label)
        
        l_line = LinearFunctionPointSlope((1, 0), k_tracker)
        l_line_graph = always_redraw(lambda: l_line.plot_in(axes))
        cde_group = always_redraw(get_cde)
        abc_triangle = always_redraw(lambda: Polygon(a_dot.get_center(), cde_group[0].get_center(), cde_group[1].get_center(), color=RED))
        bde_triangle = always_redraw(lambda: Polygon(b_dot.get_center(), cde_group[1].get_center(), cde_group[2].get_center(), color=ORANGE))

        elli = Ellipse(a=2, b=np.sqrt(3))
        elli_graph = elli.plot_in(axes, color=GREEN)
        
        self.play(Create(circ_graph), Create(a_dot), Create(a_label), Create(b_dot), Create(b_label))
        self.play(Create(l_line_graph))
        self.play(Create(cde_group))
        self.wait(2)

        self.play(Create(abc_triangle))
        self.wait(1)
        self.play(Create(bde_triangle))
        self.wait(2)

        self.play(k_tracker.animate.set_value(PI/3), run_time=4)
        self.play(k_tracker.animate.set_value(-PI/3), run_time=4)
        self.wait(2)

        ac_highlight = Line(color=YELLOW).put_start_and_end_on(a_dot.get_center(), cde_group[0].get_center())
        ad_highlight = Line(color=YELLOW).put_start_and_end_on(a_dot.get_center(), cde_group[1].get_center())
        eb_highlight = Line(color=YELLOW).put_start_and_end_on(cde_group[2].get_center(), b_dot.get_center())
        ed_highlight = Line(color=YELLOW).put_start_and_end_on(cde_group[2].get_center(), cde_group[1].get_center())

        self.play(Create(ac_highlight), Create(ad_highlight))
        self.play(FadeOut(ac_highlight), FadeOut(ad_highlight))
        self.wait(1)
        self.play(Create(eb_highlight), Create(ed_highlight))
        self.play(FadeOut(eb_highlight), FadeOut(ed_highlight))
        self.wait(2)

        ae_highlight = always_redraw(lambda: Line(color=GREEN).put_start_and_end_on(a_dot.get_center(), cde_group[2].get_center()))
        be_highlight = always_redraw(lambda: Line(color=GREEN).put_start_and_end_on(b_dot.get_center(), cde_group[2].get_center()))
        self.play(Create(ae_highlight), Create(be_highlight))
        self.wait(2)

        self.play(k_tracker.animate.set_value(PI/3), run_time=6)
        self.wait(3)
        self.play(Create(elli_graph))
        self.wait(2)
        self.play(k_tracker.animate.set_value(-PI/3), run_time=6)
        self.wait(3)

