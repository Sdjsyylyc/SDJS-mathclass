from manim import *
import numpy as np

class TriangleFunctionScene(Scene):
    def construct(self):
        self.tria_func()
        

    def tria_func(self):
        title = Text("初中三角函数", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        angle = ValueTracker(PI/6)
        len_AC = ValueTracker(5)
        start_point_x = ValueTracker(-4)
        start_point_y = ValueTracker(-3)

        def tria_ABC(start_point_x, start_point_y, len_AC, angle):
            point_A = [start_point_x, start_point_y, 0]
            point_B = [start_point_x+len_AC.get_value()*np.cos(angle), start_point_y, 0]
            point_C = [start_point_x+len_AC.get_value()*np.cos(angle), start_point_y+len_AC.get_value()*np.sin(angle), 0]

            triangle = Polygon(point_A, point_B, point_C, color=WHITE, stroke_width=5)
            return triangle
        
        def tria_ABC_label(start_point_x, start_point_y, len_AC, angle):
            point_A = [start_point_x, start_point_y, 0]
            point_B = [start_point_x+len_AC.get_value()*np.cos(angle), start_point_y, 0]
            point_C = [start_point_x+len_AC.get_value()*np.cos(angle), start_point_y+len_AC.get_value()*np.sin(angle), 0]

            label_A = MathTex(r"A", font_size=36, color=WHITE).move_to(point_A+0.5*DOWN)
            label_B = MathTex(r"B", font_size=36, color=WHITE).move_to(point_B+0.5*DOWN)
            label_C = MathTex(r"C", font_size=36, color=WHITE).move_to(point_C+0.5*UP)
            return VGroup(label_A, label_B, label_C)
        
        def line_AB(start_point_x, start_point_y, len_AC, angle):
            point_A = [start_point_x, start_point_y, 0]
            point_B = [start_point_x+len_AC.get_value()*np.cos(angle), start_point_y, 0]
            if angle > PI/2:
                line = Line(point_A, point_B, color=WHITE, stroke_width=5)
            else:
                line = Line(point_A, point_B, color=GREEN, stroke_width=5)
            return line
        
        def line_BC(start_point_x, start_point_y, len_AC, angle):
            point_B = [start_point_x+len_AC.get_value()*np.cos(angle), start_point_y, 0]
            point_C = [start_point_x+len_AC.get_value()*np.cos(angle), start_point_y+len_AC.get_value()*np.sin(angle), 0]
            if angle > PI/2:
                line = Line(point_B, point_C, color=WHITE, stroke_width=5)
            else:
                line = Line(point_B, point_C, color=BLUE, stroke_width=5)
            return line
        
        def line_AC(start_point_x, start_point_y, len_AC, angle):
            point_A = [start_point_x, start_point_y, 0]
            point_C = [start_point_x+len_AC.get_value()*np.cos(angle), start_point_y+len_AC.get_value()*np.sin(angle), 0]
            line = Line(point_A, point_C, color=RED, stroke_width=5)
            return line
            
        triangle = always_redraw(lambda: tria_ABC(start_point_x.get_value(), start_point_y.get_value(), len_AC, angle.get_value()))
        triangle_label = always_redraw(lambda: tria_ABC_label(start_point_x.get_value(), start_point_y.get_value(), len_AC, angle.get_value()))
        angle_marker = always_redraw(lambda: Arc(radius=0.5, angle=angle.get_value(), color=ORANGE, stroke_width=4,
                                                arc_center=start_point_x.get_value()*RIGHT+start_point_y.get_value()*UP))
        angle_label = always_redraw(lambda: MathTex(r"\theta", font_size=36, color=ORANGE).
                                    move_to(start_point_x.get_value()*RIGHT+start_point_y.get_value()*UP
                                    +(np.cos(angle.get_value()/2)*RIGHT+np.sin(angle.get_value()/2)*UP)*0.7))
        lineAB = always_redraw(lambda: line_AB(start_point_x.get_value(), start_point_y.get_value(), len_AC, angle.get_value()))
        markAB = always_redraw(lambda: MathTex(r"c", font_size=36, color=GREEN).move_to(lineAB.get_center()+DOWN*0.5) if angle.get_value() < PI/2 else MathTex(r"?", font_size=36, color=WHITE).move_to(lineAB.get_center()+DOWN*0.5))
        lineBC = always_redraw(lambda: line_BC(start_point_x.get_value(), start_point_y.get_value(), len_AC, angle.get_value()))
        markBC = always_redraw(lambda: MathTex(r"a", font_size=36, color=BLUE).move_to(lineBC.get_center()+RIGHT*0.5) if angle.get_value() < PI/2 else MathTex(r"?", font_size=36, color=WHITE).move_to(lineBC.get_center()+RIGHT*0.5))
        lineAC = always_redraw(lambda: line_AC(start_point_x.get_value(), start_point_y.get_value(), len_AC, angle.get_value()))
        markAC = always_redraw(lambda: MathTex(r"b", font_size=36, color=RED).move_to(lineAC.get_center()+LEFT*0.5))

        lenAC1 = always_redraw(lambda: MathTex(f"{len_AC.get_value():.2f}", font_size=36, color=RED).move_to(4*RIGHT+0.8*UP+0.03*RIGHT))
        lenAC2 = always_redraw(lambda: MathTex(f"{len_AC.get_value():.2f}", font_size=36, color=RED).move_to(4*RIGHT-0.2*UP+0.03*RIGHT))
        lenAB1 = always_redraw(lambda: MathTex(f"{len_AC.get_value()*np.cos(angle.get_value()):.2f}" if angle.get_value() < PI/2 else "?\\,?", font_size=36, color=GREEN).move_to(4*RIGHT+0.2*UP+0.03*RIGHT))
        lenAB2 = always_redraw(lambda: MathTex(f"{len_AC.get_value()*np.cos(angle.get_value()):.2f}" if angle.get_value() < PI/2 else "?\\,?", font_size=36, color=GREEN).move_to(4*RIGHT-1.2*UP+0.03*RIGHT))
        lenBC1 = always_redraw(lambda: MathTex(f"{len_AC.get_value()*np.sin(angle.get_value()):.2f}" if angle.get_value() < PI/2 else "?\\,?", font_size=36, color=BLUE).move_to(4*RIGHT+1.2*UP+0.03*RIGHT))
        lenBC2 = always_redraw(lambda: MathTex(f"{len_AC.get_value()*np.sin(angle.get_value()):.2f}" if angle.get_value() < PI/2 else "?\\,?", font_size=36, color=BLUE).move_to(4*RIGHT-0.8*UP+0.03*RIGHT))

        lineACcopy1 = line_AC(start_point_x.get_value(), start_point_y.get_value(), len_AC, angle.get_value())
        lineACcopy2 = line_AC(start_point_x.get_value(), start_point_y.get_value(), len_AC, angle.get_value())
        lineABcopy1 = line_AB(start_point_x.get_value(), start_point_y.get_value(), len_AC, angle.get_value())
        lineABcopy2 = line_AB(start_point_x.get_value(), start_point_y.get_value(), len_AC, angle.get_value())
        lineBCcopy1 = line_BC(start_point_x.get_value(), start_point_y.get_value(), len_AC, angle.get_value())
        lineBCcopy2 = line_BC(start_point_x.get_value(), start_point_y.get_value(), len_AC, angle.get_value())

        angle_value = always_redraw(lambda: MathTex(f"\\theta={angle.get_value()*180/PI:.2f}^\\circ", font_size=36, color=ORANGE).
                                    move_to(5*LEFT+3*UP))
        sin_value = always_redraw(lambda: MathTex(f"\\sin\\theta=\\frac{{\quad\quad}}{{\quad\quad}}="+(f"{np.sin(angle.get_value()):.2f}" if angle.get_value() < PI/2 else "????"), font_size=36, color=WHITE).
                                  move_to(4*RIGHT+1*UP))
        cos_value = always_redraw(lambda: MathTex(f"\\cos\\theta=\\frac{{\quad\quad}}{{\quad\quad}}="+(f"{np.cos(angle.get_value()):.2f}" if angle.get_value() < PI/2 else "????"), font_size=36, color=WHITE).
                                  move_to(4*RIGHT+0*UP))
        tan_value = always_redraw(lambda: MathTex(f"\\tan\\theta=\\frac{{\quad\quad}}{{\quad\quad}}="+(f"{np.tan(angle.get_value()):.2f}" if angle.get_value() < PI/2 else "????"), font_size=36, color=WHITE).
                                  move_to(4*RIGHT-1*UP))
        self.play(Create(triangle), Create(triangle_label), run_time=2)
        self.play(Create(angle_marker), run_time=0.5)
        self.play(Create(angle_label), Write(angle_value), run_time=0.5)
        self.play(Create(lineAB), Create(markAB), Create(lineBC), Create(markBC), Create(lineAC), Create(markAC), lag_ratio=0.5)
        self.wait(1)
        
        # 添加公式的动效
        self.play(Write(sin_value), Write(cos_value), Write(tan_value), run_time=1)
        self.wait(1)
        
        self.add(lineACcopy1, lineACcopy2, lineABcopy1, lineABcopy2, lineBCcopy1, lineBCcopy2)
        self.play(
            AnimationGroup(
                Transform(lineACcopy1, lenAC1),
                Transform(lineBCcopy1, lenBC1),
                Transform(lineABcopy1, lenAB1),
                Transform(lineACcopy2, lenAC2),
                Transform(lineBCcopy2, lenBC2),
                Transform(lineABcopy2, lenAB2),
                lag_ratio=0.15,
                run_time=2
            )
        )
        self.wait(2)

        self.remove(lineACcopy1, lineACcopy2, lineABcopy1, lineABcopy2, lineBCcopy1, lineBCcopy2)
        self.add(lenAC1, lenAC2, lenAB1, lenAB2, lenBC1, lenBC2)


        self.play(angle.animate.set_value(PI/3), run_time=1)
        self.wait(1)

        self.play(angle.animate.set_value(PI/12), run_time=1)
        self.wait(3)

        new_title = Text("如果角度超过90度？", font_size=36, color=WHITE)
        new_title.to_edge(UP)

        self.play(Transform(title, new_title),
                  angle.animate.set_value(2*PI/3),
                  run_time=1)
        self.wait(3)

        self.play(*[FadeOut(_) for _ in self.mobjects if _ != triangle], angle.animate.set_value(PI/6), run_time=1)

        # 绘制坐标轴和完整的单位圆
        axes = Axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=5,
            y_length=5,
            axis_config={"include_tip": True, "color": WHITE},
        ).move_to(2*LEFT)
        
        # 添加坐标轴标签
        x_label = MathTex("x", color=WHITE).next_to(axes.x_axis, RIGHT)
        y_label = MathTex("y", color=WHITE).next_to(axes.y_axis, UP)
        
        # 创建完整的单位圆（使用参数方程）
        unit_circle = ParametricFunction(
            lambda t: axes.c2p(np.cos(t), np.sin(t)),
            t_range=[0, 2*PI],
            color=WHITE
        )

        radius_line = Line(axes.c2p(0, 0), axes.c2p(1, 0), color=YELLOW, stroke_width=6)
        radius_label = MathTex(r"1", font_size=36, color=YELLOW).move_to(radius_line.get_center()+0.5*DOWN)
        
        self.play(Create(axes), Write(x_label), Write(y_label), Create(unit_circle),
                  len_AC.animate.set_value(axes.c2p(1, 0)[0]-axes.c2p(0, 0)[0]),
                  start_point_x.animate.set_value(axes.c2p(0, 0)[0]), start_point_y.animate.set_value(axes.c2p(0, 0)[1]), run_time=1)
        self.play(Create(radius_line), Create(radius_label), run_time=1)
        self.play(FadeOut(radius_line), FadeOut(radius_label), run_time=1)
        self.wait(1)

        
        radius_line = Line(axes.c2p(0, 0), axes.c2p(np.cos(angle.get_value()), np.sin(angle.get_value())), color=YELLOW, stroke_width=6)
        radius_label = MathTex(r"1", font_size=36, color=YELLOW).move_to(radius_line.get_center()+0.5*UP)
        end_line = always_redraw(lambda: Line(axes.c2p(0, 0), axes.c2p(np.cos(angle.get_value())*2, np.sin(angle.get_value())*2), color=PURPLE_B, stroke_width=6))
        alpha_arc = always_redraw(lambda: Arc(radius=0.5, angle=angle.get_value(), color=RED, stroke_width=3,
                                              arc_center=axes.c2p(0, 0)))
        alpha_label = always_redraw(lambda: MathTex(f"\\alpha", font_size=36, color=RED).
                                    move_to(axes.c2p(np.cos(angle.get_value()/2)*0.5, np.sin(angle.get_value()/2)*0.5)))
        alpha_value = always_redraw(lambda: MathTex(f"\\alpha={angle.get_value()*180/PI:.2f}^\\circ", font_size=36, color=RED).
                                    to_edge(UP+LEFT))
        p_dot = always_redraw(lambda: Dot(color=PURPLE_A).move_to(axes.c2p(np.cos(angle.get_value()), np.sin(angle.get_value()))))
        p_label = always_redraw(lambda: MathTex(r"P(x,y)", font_size=36, color=PURPLE_A).move_to(axes.c2p(np.cos(angle.get_value()), np.sin(angle.get_value()))+RIGHT))
        self.play(Create(radius_line), Create(radius_label), run_time=1)
        self.play(FadeOut(radius_line), FadeOut(radius_label), Create(end_line), run_time=1)
        self.play(Create(alpha_arc), Create(alpha_label), run_time=1)
        self.play(Create(p_dot), Create(p_label), run_time=1)
        self.wait(1)

        lineAB = line_AB(start_point_x.get_value(), start_point_y.get_value(), len_AC, angle.get_value())
        lineAC = line_AC(start_point_x.get_value(), start_point_y.get_value(), len_AC, angle.get_value())
        lineBC = line_BC(start_point_x.get_value(), start_point_y.get_value(), len_AC, angle.get_value())

        sin_text = MathTex(r"\sin\alpha=\frac x1", font_size=36, color=WHITE).move_to(4*RIGHT+1*UP)
        cos_text = MathTex(r"\cos\alpha=\frac y1", font_size=36, color=WHITE).move_to(4*RIGHT+0*UP)
        tan_text = MathTex(r"\tan\alpha=\frac yx", font_size=36, color=WHITE).move_to(4*RIGHT-1*UP)
        self.play(AnimationGroup(Create(lineBC), Create(lineAC), lag_ratio=0.5, run_time=1))
        self.play(Write(sin_text), run_time=1)
        new_text = MathTex(r"x=\sin\alpha", font_size=36, color=GREEN).move_to(4*RIGHT+1*UP)
        self.wait(1)
        self.play(Transform(sin_text, new_text), run_time=1)
        self.play(FadeOut(lineBC), FadeOut(lineAC), run_time=1)
        self.wait(2)

        self.play(AnimationGroup(Create(lineAB), Create(lineAC), lag_ratio=0.5, run_time=1))
        self.play(Write(cos_text), run_time=1)
        new_text = MathTex(r"y=\cos\alpha", font_size=36, color=BLUE).move_to(4*RIGHT+0*UP)
        self.wait(1)
        self.play(Transform(cos_text, new_text), run_time=1)
        self.play(FadeOut(lineAB), FadeOut(lineAC), run_time=1)
        self.wait(2)

        self.play(AnimationGroup(Create(lineBC), Create(lineAB), lag_ratio=0.5, run_time=1))
        self.play(Write(tan_text), run_time=1)
        self.play(FadeOut(lineAB), FadeOut(lineBC), run_time=1)
        self.wait(2)

        x_line = always_redraw(lambda: Line(axes.c2p(np.cos(angle.get_value()), np.sin(angle.get_value())), axes.c2p(np.cos(angle.get_value()), 0), color=GREEN, stroke_width=3))
        y_line = always_redraw(lambda: Line(axes.c2p(np.cos(angle.get_value()), np.sin(angle.get_value())), axes.c2p(0, np.sin(angle.get_value())), color=BLUE, stroke_width=3))
        sin_value = always_redraw(lambda: MathTex(f"x=\\sin\\alpha={np.sin(angle.get_value()):.2f}", font_size=36, color=GREEN).move_to(4*RIGHT+1*UP))
        cos_value = always_redraw(lambda: MathTex(f"y=\\cos\\alpha={np.cos(angle.get_value()):.2f}", font_size=36, color=BLUE).move_to(4*RIGHT+0*UP))
        tan_value = always_redraw(lambda: MathTex(f"\\frac{{y}}{{x}}=\\tan\\alpha={np.tan(angle.get_value()):.2f}", font_size=36, color=WHITE).move_to(4*RIGHT-1*UP))
        self.play(Create(x_line), Create(y_line), FadeOut(triangle), Write(alpha_value),
                  Transform(sin_text, sin_value), Transform(cos_text, cos_value), Transform(tan_text, tan_value), run_time=1)
        self.add(sin_value, cos_value, tan_value)
        self.remove(sin_text, cos_text, tan_text)
        self.wait(1)

        self.play(angle.animate.set_value(PI/3), run_time=1)
        self.wait(1)
        self.play(angle.animate.set_value(PI/12), run_time=1)
        self.wait(2)

        self.play(angle.animate.set_value(2*PI/3), run_time=1)
        self.wait(1)
        self.play(angle.animate.set_value(4*PI/3), run_time=1)
        self.wait(1)
        self.play(angle.animate.set_value(5*PI/3), run_time=1)
        self.wait(3)

        self.play(angle.animate.set_value(2*PI), run_time=1)
        
        # 创建四个象限的扇形，初始时都是透明的
        first_quadrant = always_redraw(lambda: AnnularSector(
            inner_radius=0,
            outer_radius=axes.c2p(1, 0)[0]-axes.c2p(0, 0)[0],
            angle=-(min(PI/2, 2*PI-angle.get_value()) if angle.get_value() > 3*PI/2 else PI/2),
            start_angle=0,
            color=RED_A,
            fill_opacity=0.6,
            arc_center=axes.c2p(0, 0)
        ))
        first_quadrant_label = MathTex(r"\sin\alpha<0\\\cos\alpha>0", font_size=36, color=RED_A).move_to(axes.c2p(1.4, -1.4))
        
        second_quadrant = always_redraw(lambda: AnnularSector(
            inner_radius=0,
            outer_radius=axes.c2p(1, 0)[0]-axes.c2p(0, 0)[0],
            angle=-(min(PI/2, max(0, 2*PI-angle.get_value()-PI/2)) if angle.get_value() > PI else PI/2),
            start_angle=-PI/2,
            color=GREEN_A,
            fill_opacity=0.6,
            arc_center=axes.c2p(0, 0)
        ))
        second_quadrant_label = MathTex(r"\sin\alpha<0\\\cos\alpha<0", font_size=36, color=GREEN_A).move_to(axes.c2p(-1.4, -1.4))
        
        third_quadrant = always_redraw(lambda: AnnularSector(
            inner_radius=0,
            outer_radius=axes.c2p(1, 0)[0]-axes.c2p(0, 0)[0],
            angle=-(min(PI/2, max(0, 2*PI-angle.get_value()-PI)) if angle.get_value() > PI/2 else PI/2),
            start_angle=-PI,
            color=BLUE_A,
            fill_opacity=0.6,
            arc_center=axes.c2p(0, 0)
        ))
        third_quadrant_label = MathTex(r"\sin\alpha<0\\\cos\alpha<0", font_size=36, color=BLUE_A).move_to(axes.c2p(-1.4, 1.4))

        fourth_quadrant = always_redraw(lambda: AnnularSector(
            inner_radius=0,
            outer_radius=axes.c2p(1, 0)[0]-axes.c2p(0, 0)[0],
            angle=-(min(PI/2, max(0, 2*PI-angle.get_value()-3*PI/2)) if angle.get_value() > 0 else PI/2),
            start_angle=-3*PI/2,
            color=YELLOW_A,
            fill_opacity=0.6,
            arc_center=axes.c2p(0, 0)
        ))
        fourth_quadrant_label = MathTex(r"\sin\alpha>0\\\cos\alpha>0", font_size=36, color=YELLOW_A).move_to(axes.c2p(1.4, 1.4))

        self.add(first_quadrant, second_quadrant, third_quadrant, fourth_quadrant)
        
        # 执行扫描动画（从2π到0）
        self.play(angle.animate.set_value(0),
                  AnimationGroup(Create(first_quadrant_label), Create(second_quadrant_label), Create(third_quadrant_label), Create(fourth_quadrant_label), lag_ratio=0.5), run_time=4)
        self.wait(2)

        self.play(FadeOut(first_quadrant), FadeOut(second_quadrant), FadeOut(third_quadrant), FadeOut(fourth_quadrant),
                  FadeOut(first_quadrant_label), FadeOut(second_quadrant_label), FadeOut(third_quadrant_label), FadeOut(fourth_quadrant_label),
                  FadeOut(sin_value), FadeOut(cos_value), FadeOut(tan_value), run_time=1)
        self.play(angle.animate.set_value(PI/3), run_time=1)

        triangle = Polygon(axes.c2p(0, 0), axes.c2p(np.cos(angle.get_value()), 0), axes.c2p(np.cos(angle.get_value()), np.sin(angle.get_value())), color=YELLOW, stroke_width=6)
        x_marker = MathTex(r"x", font_size=36, color=GREEN).move_to(x_line.get_center()+RIGHT*0.3)
        y_marker = MathTex(r"y", font_size=36, color=BLUE).move_to(axes.c2p(np.cos(angle.get_value())/2, 0)+DOWN*0.3)
        radius_marker = MathTex(r"1", font_size=36, color=YELLOW).move_to(radius_line.get_center()+0.5*UP+0.5*LEFT)
        self.play(Create(triangle), Create(x_marker), Create(y_marker), Create(radius_marker), run_time=1)
        self.play(FadeOut(triangle), run_time=1)
        self.wait(1)

        law_text = MathTex(r"x^2+y^2=1", font_size=36, color=WHITE).move_to(4*RIGHT+0*UP)
        self.play(Write(law_text), run_time=1)
        self.wait(1)
        
        new_law_text = MathTex(f"\\sin^2\\alpha+\\cos^2\\alpha=1", font_size=36, color=WHITE).move_to(4*RIGHT+0*UP)
        self.play(Transform(law_text, new_law_text), FadeOut(x_marker), FadeOut(y_marker), FadeOut(radius_marker), run_time=1)
        self.wait(2)

        new_law_text = always_redraw(lambda: MathTex(f"{np.sin(angle.get_value()):.2f}^2+{np.cos(angle.get_value()):.2f}^2=1", font_size=36, color=WHITE).move_to(4*RIGHT+0*UP))
        self.play(Transform(law_text, new_law_text), run_time=1)
        self.add(new_law_text)
        self.remove(law_text)
        self.play(angle.animate.set_value(5*PI/3), run_time=3, rate_func=linear)
        self.wait(1)

        self.play(angle.animate.set_value(PI/6), FadeOut(new_law_text), run_time=1)
        tan_line = Line(axes.c2p(1, 4), axes.c2p(1, -4), color=WHITE, stroke_width=4)
        end_line_reverse = always_redraw(lambda: DashedLine(axes.c2p(0, 0), axes.c2p(-2*np.cos(angle.get_value()), -2*np.sin(angle.get_value())), color=RED_A, stroke_width=3))
        p1_dot = always_redraw(lambda: Dot(color=RED).move_to(axes.c2p(1, np.tan(angle.get_value()))))
        p1_label = always_redraw(lambda: MathTex(r"P_1(1,y_1)", font_size=36, color=RED).move_to(axes.c2p(1, np.tan(angle.get_value()))+RIGHT))
        self.play(Create(tan_line), Create(end_line_reverse), FadeOut(p_dot), FadeOut(p_label), FadeOut(x_line), FadeOut(y_line), run_time=1)
        self.wait(1)
        self.play(Create(p1_dot), Create(p1_label), run_time=1)
        self.wait(1)
        
        radius_line = Line(axes.c2p(0, 0), axes.c2p(1, 0), color=YELLOW, stroke_width=6)
        radius_label = MathTex(r"1", font_size=36, color=YELLOW).move_to(radius_line.get_center()+0.5*DOWN)
        self.play(Create(radius_line), Create(radius_label), run_time=1)
        self.wait(1)

        y1_line = always_redraw(lambda: Line(axes.c2p(1, 0), axes.c2p(1, np.tan(angle.get_value())), color=RED_A, stroke_width=3))
        y1_label = always_redraw(lambda: MathTex(r"y_1", font_size=36, color=RED_A).move_to(axes.c2p(1, np.tan(angle.get_value())/2)+RIGHT*0.5))
        tan_value = MathTex(f"\\tan\\alpha=\\frac{{y_1}}{{1}}", font_size=36, color=RED_A).move_to(4*RIGHT+0*UP)
        self.play(Create(y1_line), Create(y1_label), Create(tan_value), run_time=1)
        self.wait(1)

        new_tan_value = always_redraw(lambda: MathTex(f"y_1=\\tan\\alpha={np.tan(angle.get_value()):.2f}", font_size=36, color=RED_A).move_to(4*RIGHT+0*UP))
        self.play(Transform(tan_value, new_tan_value), run_time=1)
        self.add(new_tan_value)
        self.remove(tan_value)
        self.wait(2)

        self.play(angle.animate.set_value(2*PI/3), run_time=1)
        self.wait(2)

        p_dot = Dot(color=PURPLE_A).move_to(axes.c2p(np.cos(angle.get_value()), np.sin(angle.get_value())))
        p_label = MathTex(r"P(x,y)", font_size=36, color=PURPLE_A).move_to(axes.c2p(np.cos(angle.get_value()), np.sin(angle.get_value()))+RIGHT)
        tan_value = MathTex(f"\\tan\\alpha=\\frac{{y}}{{x}}", font_size=36, color=RED_A).move_to(4*RIGHT+0*UP)
        self.play(Create(p_dot), Create(p_label), Transform(new_tan_value, tan_value), run_time=1)
        self.add(tan_value)
        self.remove(new_tan_value)
        self.wait(1)
        
        new_tan_value = MathTex(f"\\tan\\alpha=\\frac{{\\sin\\alpha}}{{\\cos\\alpha}}", font_size=36, color=RED_A).move_to(4*RIGHT+0*UP)
        self.play(Transform(tan_value, new_tan_value), run_time=1)
        self.wait(2)

        self.play(*[FadeOut(_) for _ in self.mobjects], run_time=1)
        
        
        
        

        
        
        
        

