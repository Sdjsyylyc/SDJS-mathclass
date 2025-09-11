from manim import *
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import SliderComponent, CustomAxes

class LineGeometryFormulas(Scene):
    def construct(self):
        # 创建自定义坐标系
        axes = CustomAxes(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        self.play(Create(axes), run_time=0.8)
        
        # 场景1：线段长度公式推导
        self.clear()
        self.add(axes)
        
        # 距离公式 - 放在左边，字体放大两倍
        distance_formula = MathTex("d = ?", 
                        font_size=40, color=YELLOW)
        distance_formula.to_edge(LEFT+UP, buff=0.5)
        
        # 参数跟踪器
        x1_tracker = ValueTracker(-2)
        y1_tracker = ValueTracker(-1)
        x2_tracker = ValueTracker(2)
        y2_tracker = ValueTracker(1.5)
        
        # 滑块
        x1_slider = SliderComponent("x_1", x1_tracker, -3, 3, position=[4.2, 2.8, 0])
        y1_slider = SliderComponent("y_1", y1_tracker, -2, 2, position=[4.2, 2.4, 0])
        x2_slider = SliderComponent("x_2", x2_tracker, -3, 3, position=[4.2, 2.0, 0])
        y2_slider = SliderComponent("y_2", y2_tracker, -2, 2, position=[4.2, 1.6, 0])
        self.play(Create(x1_slider), Create(y1_slider), Create(x2_slider), Create(y2_slider))
        
        # 两个点
        def get_point1():
            return Dot(axes.c2p(x1_tracker.get_value(), y1_tracker.get_value()), color=RED, radius=0.08)
        
        def get_point2():
            return Dot(axes.c2p(x2_tracker.get_value(), y2_tracker.get_value()), color=RED, radius=0.08)
        
        point1 = always_redraw(get_point1)
        point2 = always_redraw(get_point2)
        
        # 点的标签 - 放大字体
        def get_point1_label():
            x1, y1 = x1_tracker.get_value(), y1_tracker.get_value()
            label = MathTex("(x_1, y_1)", font_size=36, color=RED)
            label.next_to(axes.c2p(x1, y1), DL, buff=0.1)
            return label
        
        def get_point2_label():
            x2, y2 = x2_tracker.get_value(), y2_tracker.get_value()
            label = MathTex("(x_2, y_2)", font_size=36, color=RED)
            label.next_to(axes.c2p(x2, y2), UR, buff=0.1)
            return label
        
        point1_label = always_redraw(get_point1_label)
        point2_label = always_redraw(get_point2_label)
        
        self.play(Create(point1), Create(point2), Create(point1_label), Create(point2_label))
        
        # 连接线段 - 画完整的直线
        def get_full_line():
            x1, y1 = x1_tracker.get_value(), y1_tracker.get_value()
            x2, y2 = x2_tracker.get_value(), y2_tracker.get_value()
            
            # 避免两点重合
            if abs(x2 - x1) < 0.01 and abs(y2 - y1) < 0.01:
                return axes.plot(lambda x: y1, x_range=[-4.8, 4.8], color=BLUE, stroke_width=4)
            elif abs(x2 - x1) < 0.01:  # 垂直线
                return Line(axes.c2p(x1, -2.8), axes.c2p(x1, 2.8), color=BLUE, stroke_width=4)
            else:  # 一般情况 - 画完整直线
                slope = (y2 - y1) / (x2 - x1)
                def line_func(x):
                    return y1 + slope * (x - x1)
                return axes.plot(line_func, x_range=[-4.8, 4.8], color=BLUE, stroke_width=4)
        
        full_line = always_redraw(get_full_line)
        self.play(Create(full_line))
        
        # 添加线段标记（突出显示两点间的距离）
        def get_line_segment():
            return Line(
                axes.c2p(x1_tracker.get_value(), y1_tracker.get_value()),
                axes.c2p(x2_tracker.get_value(), y2_tracker.get_value()),
                color=RED, stroke_width=6
            )
        
        line_segment = always_redraw(get_line_segment)
        distance_label = always_redraw(lambda: MathTex("d", font_size=32, color=RED).move_to(line_segment.get_center()+0.3*UP))
        self.play(Create(line_segment), Create(distance_label))
        self.wait(1)
        self.play(Write(distance_formula))
        
        # 构造直角三角形（不包含直角符号）
        def get_right_triangle():
            x1, y1 = x1_tracker.get_value(), y1_tracker.get_value()
            x2, y2 = x2_tracker.get_value(), y2_tracker.get_value()
            
            # 水平线
            horizontal = Line(axes.c2p(x1, y1), axes.c2p(x2, y1), color=GREEN, stroke_width=3)
            # 垂直线
            vertical = Line(axes.c2p(x2, y1), axes.c2p(x2, y2), color=GREEN, stroke_width=3)
            
            return VGroup(horizontal, vertical)
        
        right_triangle = always_redraw(get_right_triangle)
        self.play(Create(right_triangle))
        
        # 标记水平距离 - 放大字体
        def get_horizontal_label():
            x1, y1 = x1_tracker.get_value(), y1_tracker.get_value()
            x2, y2 = x2_tracker.get_value(), y2_tracker.get_value()
            label = MathTex("|x_2 - x_1|", font_size=32, color=GREEN)
            label.next_to(axes.c2p((x1 + x2)/2, y1), DOWN, buff=0.1)
            return label
        
        # 标记垂直距离 - 放大字体
        def get_vertical_label():
            x1, y1 = x1_tracker.get_value(), y1_tracker.get_value()
            x2, y2 = x2_tracker.get_value(), y2_tracker.get_value()
            label = MathTex("|y_2 - y_1|", font_size=32, color=GREEN)
            label.next_to(axes.c2p(x2, (y1 + y2)/2), RIGHT, buff=0.1)
            return label
        
        horizontal_label = always_redraw(get_horizontal_label)
        vertical_label = always_redraw(get_vertical_label)
        self.play(Create(horizontal_label), Create(vertical_label))
        self.wait(1)
        self.play(Transform(distance_formula,
                            MathTex("d = \\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}", 
                            font_size=40, color=YELLOW).to_edge(LEFT+UP, buff=0.5)))
        
        # 添加倾斜角显示
        def get_inclination_angle():
            x1, y1 = x1_tracker.get_value(), y1_tracker.get_value()
            x2, y2 = x2_tracker.get_value(), y2_tracker.get_value()
            
            if abs(x2 - x1) < 0.01:  # 垂直线，不显示倾斜角
                return VGroup()
            
            slope = (y2 - y1) / (x2 - x1)
            angle = np.arctan(slope)
            
            # 以第一个点为中心的倾斜角弧线
            arc = Arc(
                start_angle=0,
                angle=angle,
                arc_center=axes.c2p(x1, y1),
                radius=1.0,
                color=ORANGE,
                stroke_width=3
            )
            return arc
        
        inclination_angle = always_redraw(get_inclination_angle)
        self.play(Create(inclination_angle))
        
        # 添加 tan θ = k 标签
        def get_tan_label():
            x1, y1 = x1_tracker.get_value(), y1_tracker.get_value()
            x2, y2 = x2_tracker.get_value(), y2_tracker.get_value()
            
            label = MathTex("\\theta", font_size=28, color=ORANGE)
            
            # 位置在第一个点附近
            label.next_to(axes.c2p(x1, y1), DOWN + RIGHT, buff=0.3)
            return label
        
        tan_label = always_redraw(get_tan_label)
        self.play(Write(tan_label))

        self.wait(1)
        self.play(
            Transform(distance_formula,
                            MathTex("d = \\sqrt{k^2 + 1} \\cdot |x_2 - x_1|", 
                            font_size=40, color=YELLOW).to_edge(LEFT+UP, buff=0.5)),
            Transform(horizontal_label,
                      MathTex("k|x_2 - x_1|", font_size=32, color=GREEN).move_to(horizontal_label.get_center())),
        )
        self.wait(3)
        self.play(Transform(distance_formula,
                            MathTex("d = \\sqrt{1 + \\frac{1}{k^2}} \\cdot |y_2 - y_1|", 
                            font_size=40, color=YELLOW).to_edge(LEFT+UP, buff=0.5)),
            Transform(vertical_label,
                      MathTex("\\frac{1}{k}|y_2 - y_1|", font_size=32, color=GREEN).move_to(vertical_label.get_center())),
        )
        self.wait(3)
        
        # 演示参数变化
        self.play(x2_tracker.animate.set_value(3), y2_tracker.animate.set_value(-1), run_time=3)
        self.play(x1_tracker.animate.set_value(-1), y1_tracker.animate.set_value(1.5), run_time=3)
        self.play(x1_tracker.animate.set_value(-2), y1_tracker.animate.set_value(-1), 
                  x2_tracker.animate.set_value(2), y2_tracker.animate.set_value(1.5), run_time=2)
        
        self.wait(2)
        
        # 清理场景1
        self.play(FadeOut(VGroup(point1, point2, point1_label, point2_label, full_line, line_segment, 
                                right_triangle, horizontal_label, vertical_label, inclination_angle, 
                                tan_label, distance_formula, x1_slider, y1_slider, x2_slider, y2_slider)), run_time=1)
        
        # 场景2：点到直线距离公式推导
        self.clear()
        self.add(axes)
        
        # 点到直线距离公式 - 放在左边，字体放大两倍
        distance_formula2 = MathTex("d = \\frac{|Ax_0 + By_0 + C|}{\\sqrt{A^2 + B^2}}", 
                        font_size=40, color=YELLOW)
        distance_formula2.to_edge(LEFT+UP, buff=0.5)
        self.play(Write(distance_formula2))
        
        # 直线参数
        A_tracker = ValueTracker(1)
        B_tracker = ValueTracker(1)
        C_tracker = ValueTracker(-1)
        
        # 点参数
        px_tracker = ValueTracker(2)
        py_tracker = ValueTracker(1.5)
        
        # 滑块
        A_slider = SliderComponent("A", A_tracker, 0.5, 2, position=[4.0, 2.8, 0])
        B_slider = SliderComponent("B", B_tracker, 0.5, 2, position=[4.0, 2.4, 0])
        C_slider = SliderComponent("C", C_tracker, -2, 2, position=[4.0, 2.0, 0])
        px_slider = SliderComponent("P_x", px_tracker, -3, 3, position=[4.0, 1.6, 0])
        py_slider = SliderComponent("P_y", py_tracker, -2, 2, position=[4.0, 1.2, 0])
        
        self.play(Create(A_slider), Create(B_slider), Create(C_slider), 
                  Create(px_slider), Create(py_slider))
        
        # 直线
        def get_line():
            A, B, C = A_tracker.get_value(), B_tracker.get_value(), C_tracker.get_value()
            if abs(B) < 0.01:
                B = 0.01
            def line_func(x):
                return -(A/B)*x - C/B
            return axes.plot(line_func, x_range=[-4.8, 4.8], color=BLUE, stroke_width=4)
        
        line = always_redraw(get_line)
        
        # 点P
        def get_point_P():
            return Dot(axes.c2p(px_tracker.get_value(), py_tracker.get_value()), 
                      color=RED, radius=0.08)
        
        point_P = always_redraw(get_point_P)
        
        # 点P标签 - 放大字体
        def get_point_P_label():
            px, py = px_tracker.get_value(), py_tracker.get_value()
            label = MathTex("P(x_0, y_0)", font_size=36, color=RED)
            label.next_to(axes.c2p(px, py), UR, buff=0.1)
            return label
        
        point_P_label = always_redraw(get_point_P_label)
        
        self.play(Create(line), Create(point_P), Create(point_P_label))
        
        # 垂足点
        def get_foot_point():
            A, B, C = A_tracker.get_value(), B_tracker.get_value(), C_tracker.get_value()
            px, py = px_tracker.get_value(), py_tracker.get_value()
            
            # 垂足坐标公式
            denominator = A*A + B*B
            if denominator < 0.01:
                return Dot(ORIGIN, radius=0, fill_opacity=0)
            
            foot_x = (B*B*px - A*B*py - A*C) / denominator
            foot_y = (A*A*py - A*B*px - B*C) / denominator
            
            return Dot(axes.c2p(foot_x, foot_y), color=GREEN, radius=0.08)
        
        foot_point = always_redraw(get_foot_point)
        
        # 垂直线段
        def get_perpendicular():
            A, B, C = A_tracker.get_value(), B_tracker.get_value(), C_tracker.get_value()
            px, py = px_tracker.get_value(), py_tracker.get_value()
            
            denominator = A*A + B*B
            if denominator < 0.01:
                return Line(ORIGIN, ORIGIN, color=GREEN, stroke_width=3)
            
            foot_x = (B*B*px - A*B*py - A*C) / denominator
            foot_y = (A*A*py - A*B*px - B*C) / denominator
            
            return Line(axes.c2p(px, py), axes.c2p(foot_x, foot_y), 
                       color=GREEN, stroke_width=3)
        
        perpendicular = always_redraw(get_perpendicular)
        
        self.play(Create(foot_point), Create(perpendicular))
        
                # 直线方程显示 - 放大字体
        line_equation = MathTex("Ax + By + C = 0",
                     font_size=36, color=BLUE)
        line_equation.to_corner(DR, buff=0.5)
        self.play(Write(line_equation))
        
        # 演示参数变化
        self.play(px_tracker.animate.set_value(-1), py_tracker.animate.set_value(-1), run_time=3)
        self.play(A_tracker.animate.set_value(1.5), B_tracker.animate.set_value(0.5), run_time=3)
        self.play(C_tracker.animate.set_value(0.5), run_time=2)
        
        self.wait(2)
        
        # 清理场景2
        self.play(FadeOut(VGroup(line, point_P, point_P_label, foot_point, perpendicular,
                                distance_formula2, line_equation,
                                A_slider, B_slider, C_slider, px_slider, py_slider)), run_time=1)
        
        # 场景3：两平行线距离
        self.clear()
        self.add(axes)
        
        # 平行线距离公式 - 放在左边，字体放大两倍
        parallel_distance = MathTex("d = \\frac{|C_2 - C_1|}{\\sqrt{A^2 + B^2}}", 
                        font_size=40, color=YELLOW)
        parallel_distance.to_edge(LEFT+UP, buff=0.5)
        self.play(Write(parallel_distance))
        
        # 平行线参数
        A_tracker = ValueTracker(1)
        B_tracker = ValueTracker(1)
        C1_tracker = ValueTracker(-1)
        C2_tracker = ValueTracker(1)
        
        # 滑块
        A_slider = SliderComponent("A", A_tracker, 0.5, 2, position=[4.0, 2.6, 0])
        B_slider = SliderComponent("B", B_tracker, 0.5, 2, position=[4.0, 2.2, 0])
        C1_slider = SliderComponent("C_1", C1_tracker, -2, 2, position=[4.0, 1.8, 0])
        C2_slider = SliderComponent("C_2", C2_tracker, -2, 2, position=[4.0, 1.4, 0])
        
        self.play(Create(A_slider), Create(B_slider), Create(C1_slider), Create(C2_slider))
        
        # 两条平行线
        def get_line1():
            A, B, C1 = A_tracker.get_value(), B_tracker.get_value(), C1_tracker.get_value()
            if abs(B) < 0.01:
                B = 0.01
            def line_func(x):
                return -(A/B)*x - C1/B
            return axes.plot(line_func, x_range=[-4.8, 4.8], color=BLUE, stroke_width=4)
        
        def get_line2():
            A, B, C2 = A_tracker.get_value(), B_tracker.get_value(), C2_tracker.get_value()
            if abs(B) < 0.01:
                B = 0.01
            def line_func(x):
                return -(A/B)*x - C2/B
            return axes.plot(line_func, x_range=[-4.8, 4.8], color=RED, stroke_width=4)
        
        line1 = always_redraw(get_line1)
        line2 = always_redraw(get_line2)
        
        self.play(Create(line1), Create(line2))
        
        # 两直线方程 - 放大字体
        eq1 = MathTex("L_1: Ax + By + C_1 = 0", 
                     font_size=32, color=BLUE)
        eq2 = MathTex("L_2: Ax + By + C_2 = 0", 
                     font_size=32, color=RED)
        eq1.to_corner(DR, buff=1.0)
        eq2.next_to(eq1, DOWN, buff=0.1)
        equations = VGroup(eq1, eq2)
        self.play(Write(equations))
        
        # 演示距离变化
        self.play(C2_tracker.animate.set_value(2), run_time=3)
        self.play(C1_tracker.animate.set_value(-2), run_time=3)
        self.play(A_tracker.animate.set_value(1.5), B_tracker.animate.set_value(0.8), run_time=3)
        
        self.wait(2)
        
        # 清理场景3
        self.play(FadeOut(VGroup(line1, line2, equations, parallel_distance,
                                A_slider, B_slider, C1_slider, C2_slider)), run_time=1)
        
        # 场景4：两直线夹角公式
        self.clear()
        self.add(axes)
        
        # 夹角公式 - 放在左边，字体放大两倍
        angle_formula = MathTex("\\tan \\theta = \\left|\\frac{k_2 - k_1}{1 + k_1 k_2}\\right|", 
                        font_size=40, color=YELLOW)
        angle_formula.to_edge(LEFT+UP, buff=0.5)
        self.play(Write(angle_formula))
        
        # 倾斜角公式 - 在主公式下方
        inclination_formula = MathTex("\\tan \\alpha = k", 
                        font_size=36, color=ORANGE)
        inclination_formula.next_to(angle_formula, DOWN, buff=0.5)
        self.play(Write(inclination_formula))
        
        # 斜率参数
        k1_tracker = ValueTracker(1)
        k2_tracker = ValueTracker(-0.5)
        
        # 滑块
        k1_slider = SliderComponent("k_1", k1_tracker, -2, 2, position=[4.0, 2.6, 0])
        k2_slider = SliderComponent("k_2", k2_tracker, -2, 2, position=[4.0, 2.2, 0])
        
        self.play(Create(k1_slider), Create(k2_slider))
        
        # 两条直线
        def get_line_k1():
            k1 = k1_tracker.get_value()
            return axes.plot(lambda x: k1 * x, x_range=[-4.8, 4.8], color=BLUE, stroke_width=4)
        
        def get_line_k2():
            k2 = k2_tracker.get_value()
            return axes.plot(lambda x: k2 * x, x_range=[-4.8, 4.8], color=RED, stroke_width=4)
        
        line_k1 = always_redraw(get_line_k1)
        line_k2 = always_redraw(get_line_k2)
        
        self.play(Create(line_k1), Create(line_k2))
        
        # 倾斜角弧线 - 显示k1直线的倾斜角
        def get_inclination_arc():
            k1 = k1_tracker.get_value()
            angle1 = np.arctan(k1)
            
            return Arc(
                start_angle=0, 
                angle=angle1,
                arc_center=axes.c2p(0, 0),
                radius=1.2,
                color=ORANGE,
                stroke_width=3
            )
        
        inclination_arc = always_redraw(get_inclination_arc)
        self.play(Create(inclination_arc))
        
        # 两直线夹角弧线
        def get_angle_arc():
            k1, k2 = k1_tracker.get_value(), k2_tracker.get_value()
            angle1 = np.arctan(k1)
            angle2 = np.arctan(k2)
            
            # 确保角度在正确范围内
            if angle1 < angle2:
                start_angle = angle1
                end_angle = angle2
            else:
                start_angle = angle2
                end_angle = angle1
            
            return Arc(
                start_angle=start_angle, 
                angle=end_angle - start_angle,
                arc_center=axes.c2p(0, 0),
                radius=0.8,
                color=GREEN,
                stroke_width=3
            )
        
        angle_arc = always_redraw(get_angle_arc)
        self.play(Create(angle_arc))
        
        # 斜率显示 - 放大字体
        slope1 = MathTex("L_1: y = k_1 x", font_size=32, color=BLUE)
        slope2 = MathTex("L_2: y = k_2 x", font_size=32, color=RED)
        slope1.to_corner(DR, buff=1.0)
        slope2.next_to(slope1, DOWN, buff=0.1)
        slopes = VGroup(slope1, slope2)
        self.play(Write(slopes))
        
        # 演示参数变化
        self.play(k1_tracker.animate.set_value(2), run_time=3)
        self.play(k2_tracker.animate.set_value(-1), run_time=3)
        self.play(k1_tracker.animate.set_value(-0.5), k2_tracker.animate.set_value(1.5), run_time=3)
        
        self.wait(2)
        
        # 清理场景4
        self.play(FadeOut(VGroup(line_k1, line_k2, inclination_arc, angle_arc, angle_formula, 
                                inclination_formula, slopes, k1_slider, k2_slider)), run_time=1)
        
        # 场景5：垂足公式推导
        self.clear()
        self.add(axes)
        
        # 垂足公式 - 放在左边，字体放大两倍
        foot_formula = MathTex(
            "H\\left(\\frac{B^2x_0 - ABy_0 - AC}{A^2 + B^2}, \\frac{A^2y_0 - ABx_0 - BC}{A^2 + B^2}\\right)",
            font_size=28, color=YELLOW
        )
        foot_formula.to_edge(LEFT+UP, buff=0.5)
        self.play(Write(foot_formula))
        
        # 重用场景2的部分参数
        A_tracker = ValueTracker(1)
        B_tracker = ValueTracker(1)
        C_tracker = ValueTracker(-1)
        px_tracker = ValueTracker(2)
        py_tracker = ValueTracker(1.5)
        
        # 滑块
        A_slider = SliderComponent("A", A_tracker, 0.5, 2, position=[4.0, 2.8, 0])
        B_slider = SliderComponent("B", B_tracker, 0.5, 2, position=[4.0, 2.4, 0])
        C_slider = SliderComponent("C", C_tracker, -2, 2, position=[4.0, 2.0, 0])
        px_slider = SliderComponent("P_x", px_tracker, -3, 3, position=[4.0, 1.6, 0])
        py_slider = SliderComponent("P_y", py_tracker, -2, 2, position=[4.0, 1.2, 0])
        
        self.play(Create(A_slider), Create(B_slider), Create(C_slider), 
                  Create(px_slider), Create(py_slider))
        
        # 直线、点P、垂足（重用之前的函数）
        line = always_redraw(get_line)
        point_P = always_redraw(get_point_P)
        point_P_label = always_redraw(get_point_P_label)
        foot_point = always_redraw(get_foot_point)
        perpendicular = always_redraw(get_perpendicular)
        
        self.play(Create(line), Create(point_P), Create(point_P_label), 
                  Create(foot_point), Create(perpendicular))
        
        # 直线方程
        line_equation = MathTex("Ax + By + C = 0",
                     font_size=18, color=BLUE)
        line_equation.to_corner(DR, buff=0.5)
        self.play(Write(line_equation))
        
        # 演示参数变化
        self.play(px_tracker.animate.set_value(-1.5), py_tracker.animate.set_value(2), run_time=3)
        self.play(A_tracker.animate.set_value(2), B_tracker.animate.set_value(0.5), run_time=3)
        self.play(C_tracker.animate.set_value(0.8), run_time=2)
        
        self.wait(2)
        
        # 最终清理
        self.play(FadeOut(VGroup(line, point_P, point_P_label, foot_point, perpendicular,
                                foot_formula, line_equation,
                                A_slider, B_slider, C_slider, px_slider, py_slider)), run_time=1)
        
        self.play(FadeOut(axes), run_time=0.5)
        self.wait(0.5) 