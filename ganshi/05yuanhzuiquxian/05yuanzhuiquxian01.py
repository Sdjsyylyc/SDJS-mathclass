from manim import *
import numpy as np
import sys
import os
import math
from scipy.optimize import fsolve, brentq
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints, Ellipse, Parabola

class Yuanzhuiquxian01(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-3, 3],
            y_range=[-2, 2],
            x_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        axes.move_to(ORIGIN)
        o_dot = Dot(color=WHITE).move_to(axes.c2p(0, 0))
        o_label = MathTex(r"O").next_to(o_dot, DOWN+LEFT)
        self.add(axes, o_dot, o_label)

        elli = Ellipse(2, np.sqrt(3))
        elli_graph = elli.plot_in(axes)
        elli_func = elli.get_parametric_function()
        self.play(Create(elli_graph))

        pos_tracker = ValueTracker(PI/3)
        delta_pos_tracker = ValueTracker(PI/6)
        ka_tracker = ValueTracker().add_updater(lambda m: m.set_value(PI/2 if elli_func(pos_tracker.get_value())[0]==0 else np.arctan(elli_func(pos_tracker.get_value())[1]/elli_func(pos_tracker.get_value())[0])))
        k1_tracker = ValueTracker().add_updater(lambda m: m.set_value(ka_tracker.get_value()-delta_pos_tracker.get_value()))
        k2_tracker = ValueTracker().add_updater(lambda m: m.set_value(ka_tracker.get_value()+delta_pos_tracker.get_value()))
        r_tracker = ValueTracker().add_updater(lambda m: m.set_value((np.sin(delta_pos_tracker.get_value())*np.sqrt(elli_func(pos_tracker.get_value())[0]**2+elli_func(pos_tracker.get_value())[1]**2))))
        self.add(pos_tracker, delta_pos_tracker, r_tracker, ka_tracker, k1_tracker, k2_tracker)

        a_dot = always_redraw(lambda: Dot(color=WHITE).move_to(axes.c2p(*elli_func(pos_tracker.get_value()))))
        a_label = always_redraw(lambda: MathTex(r"A", color=WHITE).next_to(a_dot, UP))
        self.play(Create(a_dot), Create(a_label))

        l1_line_graph = always_redraw(lambda: LinearFunctionPointSlope(elli_func(pos_tracker.get_value()), k1_tracker).plot_in(axes))
        l2_line_graph = always_redraw(lambda: LinearFunctionPointSlope(elli_func(pos_tracker.get_value()), k2_tracker).plot_in(axes))
        self.play(Create(l1_line_graph), Create(l2_line_graph))

        def get_bc():
            xa, ya = elli_func(pos_tracker.get_value())
            k1 = np.tan(k1_tracker.get_value())
            k2 = np.tan(k2_tracker.get_value())
            xb = -8*k1*(ya-k1*xa)/(4*k1**2+3) - xa
            xc = -8*k2*(ya-k2*xa)/(4*k2**2+3) - xa
            yb = k1*(xb-xa) + ya
            yc = k2*(xc-xa) + ya
            
            b_dot = Dot(color=WHITE).move_to(axes.c2p(xb, yb))
            c_dot = Dot(color=WHITE).move_to(axes.c2p(xc, yc))
            b_label = MathTex(r"B", color=WHITE).next_to(b_dot, UP)
            c_label = MathTex(r"C", color=WHITE).next_to(c_dot, UP)
            bc_line = Line().put_start_and_end_on(b_dot.get_center(), c_dot.get_center())
            return VGroup(b_dot, c_dot, b_label, c_label, bc_line)

        def delta_func(delta):
            xa, ya = elli_func(pos_tracker.get_value())
            k1 = np.tan(ka_tracker.get_value() - delta)
            k2 = np.tan(ka_tracker.get_value() + delta)
            r = np.sin(delta)*np.sqrt(xa**2+ya**2)
            xb = -8*k1*(ya-k1*xa)/(4*k1**2+3) - xa
            xc = -8*k2*(ya-k2*xa)/(4*k2**2+3) - xa
            yb = k1*(xb-xa) + ya
            yc = k2*(xc-xa) + ya
            
            k = np.arctan((yb-yc)/(xb-xc))
            d = np.abs(yb-np.tan(k)*xb)*np.cos(k)
            return r - d

        def get_delta():
            delta = brentq(delta_func, PI/12, PI/3)
            return delta


        bc_group = always_redraw(get_bc)
        self.play(Create(bc_group))

        circ = CustomCircle((0,0), r_tracker)
        circ_graph = always_redraw(lambda: circ.plot_in(axes, color=RED))
        self.play(Create(circ_graph))
        self.wait(2)

        self.play(delta_pos_tracker.animate.set_value(get_delta()), run_time=5)
        self.wait(3)

        self.play(pos_tracker.animate.set_value(PI), run_time=4)
        self.wait(2)
        self.play(delta_pos_tracker.animate.set_value(get_delta()), run_time=5)
        self.wait(3)

        self.play(pos_tracker.animate.set_value(7*PI/4), run_time=4)
        self.wait(2)
        self.play(delta_pos_tracker.animate.set_value(get_delta()), run_time=5)
        self.wait(3)


