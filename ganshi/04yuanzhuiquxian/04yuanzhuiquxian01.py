from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction, CustomCircle, LinearFunctionTwoPoints, Ellipse, Parabola

class Yuanzhuiquxian01(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-6, 6],
            y_range=[-4, 4],
            x_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        axes.move_to(RIGHT)
        o_dot = Dot(color=WHITE).move_to(axes.c2p(0, 0))
        o_label = MathTex(r"O").next_to(o_dot, DOWN+LEFT)
        self.add(axes, o_dot, o_label)

        elli = Ellipse(a=np.sqrt(18), b=np.sqrt(6))
        elli_graph = elli.plot_in(axes)

        circ = CustomCircle((0,0), np.sqrt(6))
        circ_graph = circ.plot_in(axes)

        self.play(Create(elli_graph), Create(circ_graph))

        l_line = LinearFunctionTwoPoints((0, 2*np.sqrt(3)), (2*np.sqrt(3), 0))
        l_line_graph = l_line.plot_in(axes)

        self.play(Create(l_line_graph))

        xp = 1.5*(np.sqrt(3)-1)
        yp = 2*np.sqrt(3) - xp
        xq = 1.5*(np.sqrt(3)+1)
        yq = 2*np.sqrt(3) - xq
        p_dot = Dot().move_to(axes.c2p(xp, yp))
        p_label = MathTex(r"P").next_to(p_dot, UP)
        q_dot = Dot().move_to(axes.c2p(xq, yq))
        q_label = MathTex(r"Q").next_to(q_dot, RIGHT)

        self.play(Create(p_dot), Create(p_label), Create(q_dot), Create(q_label))

        a_dot = Dot(color=GREEN).move_to(axes.c2p(np.sqrt(3), np.sqrt(3)))
        a_label = MathTex(r"A", color=GREEN).next_to(a_dot, LEFT)
        b_dot = Dot(color=GREEN).move_to(axes.c2p(2*np.sqrt(3), 0))
        b_label = MathTex(r"B", color=GREEN).next_to(b_dot, DOWN)
        self.play(Create(a_dot), Create(a_label), Create(b_dot), Create(b_label))

        ao_line = Line(color=GREEN).put_start_and_end_on(a_dot.get_center(), o_dot.get_center())
        ab_line = Line(color=GREEN).put_start_and_end_on(a_dot.get_center(), b_dot.get_center())
        oab_recangle = RightAngle(ao_line, ab_line, color=GREEN, length=0.2)
        self.play(Create(ao_line), Create(ab_line), Create(oab_recangle))
        self.wait(2)
        
        m_dot = Dot(color=BLUE).move_to(axes.c2p(1.5*np.sqrt(3), 0.5*np.sqrt(3)))
        m_label = MathTex(r"M", color=BLUE).next_to(m_dot, UP)
        om_line = Line(color=BLUE).put_start_and_end_on(o_dot.get_center(), m_dot.get_center())
        self.play(Create(m_dot), Create(m_label), Create(om_line))
        self.wait(2)

        ob_line = Line(color=WHITE).put_start_and_end_on(o_dot.get_center(), b_dot.get_center())
        oa_line = Line(color=GREEN).put_start_and_end_on(o_dot.get_center(), a_dot.get_center())
        aob_angle = Angle(ob_line, oa_line, color=GREEN, radius=0.3)
        aom_angle = Angle(om_line, oa_line, color=ORANGE, radius=0.4)
        bom_angle = Angle(ob_line, om_line, color=BLUE, radius=0.5)
        koa_formula = MathTex(r"\tan(\angle AOB) = k_{OA} = -\frac{1}{k}", color=GREEN, font_size=24).to_corner(UL, buff=0.5)
        aom_formula = MathTex(r"\tan(\angle AOM) = \frac{1}{2}\tan(\angle AOB)", color=ORANGE, font_size=24).next_to(koa_formula, DOWN, buff=0.2).to_edge(LEFT)
        kom_formula = MathTex(r"k_{OM} = \tan(\angle BOM) = \tan(\angle AOM - \angle AOB)", color=BLUE, font_size=24).next_to(aom_formula, DOWN, buff=0.2).to_edge(LEFT)
        ma_highlight = Line(color=YELLOW).put_start_and_end_on(a_dot.get_center(), m_dot.get_center())
        mb_highlight = Line(color=YELLOW).put_start_and_end_on(b_dot.get_center(), m_dot.get_center())
        self.play(Create(aob_angle), Create(koa_formula))
        self.wait(2)
        self.play(Create(ma_highlight), Create(mb_highlight))
        self.play(FadeOut(ma_highlight), FadeOut(mb_highlight), Create(aom_angle), Create(aom_formula))
        self.wait(2)
        self.play(Create(bom_angle), Create(kom_formula))
        self.wait(3)

        formula1 = MathTex(r"k_{OM} = \frac{\frac{1}{k}-\frac1{2k}}{1+\frac1{2k}^2}", color=WHITE, font_size=24).to_corner(UL, buff=0.5)
        formula2 = MathTex(r"k_{OM}k = -\frac13", color=WHITE, font_size=24).next_to(formula1, DOWN, buff=0.2).to_edge(LEFT)
        self.play(FadeOut(koa_formula), FadeOut(aom_formula), FadeOut(kom_formula), Write(formula1))
        self.wait(3)
        self.play(Write(formula2))
        self.wait(3)

        ans_formula = MathTex(r"k = -1", color=WHITE, font_size=24).to_corner(UL, buff=0.5)
        self.play(FadeOut(formula1), FadeOut(formula2), Write(ans_formula))
        self.wait(3)



