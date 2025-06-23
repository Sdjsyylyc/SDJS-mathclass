from manim import *
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect

class Xiandaoke01(Scene):
    def construct(self):
        # 创建自定义坐标系
        axes = CustomAxes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        self.play(Create(axes), run_time=0.2)
        
        # 创建椭圆
        ellipse = Ellipse(width=4, height=2, color=BLUE)
        ellipse_label = MathTex(r"\frac{x^2}{4} + y^2 = 1", color=BLUE).scale(0.8)
        ellipse_label.to_edge(UP+LEFT, buff=0.5)
        
        self.play(Create(ellipse), Write(ellipse_label), run_time=1.5)
        self.wait(2)
        
        # 定点 (0, 2)
        fixed_point = Dot(axes.c2p(-1, 2), color=YELLOW, radius=0.08)
        fixed_point_label = MathTex("(-1, 2)", color=YELLOW).scale(0.8)
        fixed_point_label.next_to(fixed_point, UR, buff=0.2)
        
        self.play(Create(fixed_point), Write(fixed_point_label), run_time=1)
     
        
        # 创建围绕定点旋转的直线
        # 使用倾斜角参数 theta 来控制斜率 k = tan(theta)
        theta_tracker = ValueTracker(PI/6)  # 初始角度30度
        
        def get_rotating_line():
            theta = theta_tracker.get_value()
            k = np.tan(theta)  # 斜率 = tan(倾斜角)
            # 直线方程：y = k(x+1) + 2 (通过定点(-1,2))
            return axes.plot(lambda x: k * (x+1) + 2, x_range=[-3, 3],color=YELLOW)
        
        def get_line_label():
            theta = theta_tracker.get_value()
            k = np.tan(theta)
            return MathTex(f"y = k(x+1) + 2", color=YELLOW).scale(0.7)
        
        rotating_line = always_redraw(get_rotating_line)
        line_label = MathTex("y = k(x+1) + 2", color=YELLOW).scale(0.7)
        line_label.to_edge(UP+LEFT, buff=0.5).shift(DOWN*1.2)
        
        self.play(Create(rotating_line), Write(line_label), run_time=1)
        
        # 直线围绕定点旋转2秒
        self.play(
            theta_tracker.animate.set_value(5*PI/6),  # 从30度逆时针旋转到150度（即-30度）
            run_time=2,
            rate_func=linear
        )
        self.wait(1)
        # 直线围绕定点旋转2秒
        self.play(
            theta_tracker.animate.set_value(PI/6),  # 转回30度
            run_time=2,
            rate_func=linear
        )
        self.wait(1)
        
        # 直线转到62度
        tangent_angle1 = 62 * PI / 180  # 62度
        self.play(
            theta_tracker.animate.set_value(tangent_angle1),
            run_time=3,
            rate_func=smooth
        )
        
        # 在点(-1.93, 0.258)处发生碰撞效果
        tangent_point1 = axes.c2p(-1.93, 0.258)
        collision_effect1 = CollisionEffect(tangent_point1, color=YELLOW, duration=1.0)
        self.add(collision_effect1.get_lines())
        self.play(collision_effect1.get_animation())
        self.remove(collision_effect1.get_lines())
        
        self.wait(2)  # 停顿2秒
        
        # 直线转到152度
        tangent_angle2 = 152 * PI / 180  # 152度
        self.play(
            theta_tracker.animate.set_value(tangent_angle2),
            run_time=3,
            rate_func=smooth
        )
        
        # 在点(1.46, 0.683)处发生碰撞效果
        tangent_point2 = axes.c2p(1.46, 0.683)
        collision_effect2 = CollisionEffect(tangent_point2, color=YELLOW, duration=1.0)
        self.add(collision_effect2.get_lines())
        self.play(collision_effect2.get_animation())
        self.remove(collision_effect2.get_lines())
        
        self.wait(2)
        
        # 将所有图形元素向右移动2个单位
        self.play(
            axes.animate.shift(RIGHT * 2),
            ellipse.animate.shift(RIGHT * 2),
            fixed_point.animate.shift(RIGHT * 2),
            fixed_point_label.animate.shift(RIGHT * 2),
            rotating_line.animate.shift(RIGHT * 2),
            run_time=2,
            rate_func=smooth
        )
        
        # 在左侧两个方程的右边添加联立符号
        brace = MathTex(r"\right\}", color=WHITE).scale(2)
        # 计算椭圆方程和直线方程的中点，然后向右偏移1个单位
        mid_point = (ellipse_label.get_center() + line_label.get_center()) / 2
        brace.move_to(mid_point + RIGHT * 1.6)
        
        self.play(Write(brace), run_time=1)
        self.wait(1)
        
        # 创建代入公式：x²/4 + [k(x+1) + 2]² = 1
        substitution_formula = MathTex(
            r"\frac{x^2}{4}", "+", r"[", r"k(x+1) + 2", r"]^2", "=", "1"
        ).scale(0.8)
        
        # 手动设置各部分颜色
        substitution_formula[0].set_color(BLUE)   # x²/4 蓝色
        substitution_formula[1].set_color(WHITE)  # + 白色
        substitution_formula[2].set_color(WHITE)  # [ 白色
        substitution_formula[3].set_color(YELLOW) # k(x+1) + 2 黄色
        substitution_formula[4].set_color(WHITE)  # ]² 白色
        substitution_formula[5].set_color(WHITE)  # = 白色
        substitution_formula[6].set_color(BLUE)   # 1 蓝色
        
        # 将公式放在直线方程下方，左对齐
        substitution_formula.next_to(line_label, DOWN, buff=0.5, aligned_edge=LEFT)
        
        self.play(Write(substitution_formula), run_time=2)
        self.wait(1)
        
        # 添加判别式公式：Δ = 3k² - 4k - 3 = 0
        discriminant_formula = MathTex(
            r"\Delta", "=", r"3k^2", "-", r"4k", "-", "3", "=", "0",
            color=WHITE
        ).scale(0.8)

        # 将公式放在代入公式下方，左对齐
        discriminant_formula.next_to(substitution_formula, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(Write(discriminant_formula), run_time=2)
        self.wait(1)

        
        # 添加斜率到角度的转换公式
        k1_theta1_formula = MathTex(
            r"k_{1}", r"\approx", r"1.87", r"\rightarrow", r"\theta_{1}", r"\approx", r"62^{\circ}",
            color=WHITE
        ).scale(0.8)
        
        k2_theta2_formula = MathTex(
            r"k_{2}", r"\approx", r"0.54", r"\rightarrow", r"\theta_{2}", r"\approx", r"152^{\circ}",
            color=WHITE
        ).scale(0.8)
        
        # 将公式放在判别式公式下方，左对齐
        k1_theta1_formula.next_to(discriminant_formula, DOWN, buff=0.5, aligned_edge=LEFT)
        k2_theta2_formula.next_to(k1_theta1_formula, DOWN, buff=0.3, aligned_edge=LEFT)
        
        # 直线转到62度
        tangent_angle1 = 62 * PI / 180  # 62度
        self.play(
            theta_tracker.animate.set_value(tangent_angle1),
            run_time=3,
            rate_func=smooth
        )
        
        # 在点(-1.93, 0.258)处发生碰撞效果
        tangent_point1 = axes.c2p(-1.93, 0.258)
        collision_effect1 = CollisionEffect(tangent_point1, color=YELLOW, duration=1.0)
        self.add(collision_effect1.get_lines())
        self.play(collision_effect1.get_animation())
        self.remove(collision_effect1.get_lines())
        
        # 添加θ₁角度标注效果
        # 计算直线与x轴的交点
        k1 = np.tan(tangent_angle1)
        x_intercept1 = -1 - 2/k1  # 直线y = k(x+1) + 2 与x轴交点的x坐标
        intersection_point1 = axes.c2p(x_intercept1, 0)
        
        # 创建x轴正方向的参考线段
        x_axis_line1 = Line(
            start=intersection_point1,
            end=intersection_point1 + RIGHT * 1.5,
            color=GRAY,
            stroke_width=2
        )
        
        # 创建直线段（从交点向右上方延伸）
        line_segment1 = Line(
            start=intersection_point1,
            end=intersection_point1 + 1.5 * np.array([np.cos(tangent_angle1), np.sin(tangent_angle1), 0]),
            color=YELLOW,
            stroke_width=2
        )
        
        # 创建角度弧线（从x轴正方向到直线方向）
        angle_arc1 = Arc(
            radius=0.8,
            start_angle=0,
            angle=tangent_angle1,
            color=ORANGE,
            stroke_width=3,
            arc_center=intersection_point1
        )
        
        # 创建角度标签
        theta_label1 = MathTex(r"\theta_1", color=ORANGE).scale(0.7)
        # 将标签放在弧线的中间位置
        label_angle1 = tangent_angle1 / 2
        label_pos1 = intersection_point1 + 1.2 * np.array([np.cos(label_angle1), np.sin(label_angle1), 0])
        theta_label1.move_to(label_pos1)
        
        # 显示角度标注
        self.play(
            Create(x_axis_line1),
            Create(line_segment1),
            Create(angle_arc1),
            Write(theta_label1),
            run_time=1
        )
        
        


        self.play(Write(k1_theta1_formula), run_time=1.5)
        self.wait(0.5)
        # 等待1秒后消失
        self.wait(1)
        self.play(
            FadeOut(x_axis_line1),
            FadeOut(line_segment1),
            FadeOut(angle_arc1),
            FadeOut(theta_label1),
            run_time=0.5
        )
        
        self.wait(2)  # 停顿2秒

        # 直线转到152度
        tangent_angle2 = 152 * PI / 180  # 152度
        self.play(
            theta_tracker.animate.set_value(tangent_angle2),
            run_time=3,
            rate_func=smooth
        )
        
        # 在点(1.46, 0.683)处发生碰撞效果
        tangent_point2 = axes.c2p(1.46, 0.683)
        collision_effect2 = CollisionEffect(tangent_point2, color=YELLOW, duration=1.0)
        self.add(collision_effect2.get_lines())
        self.play(collision_effect2.get_animation())
        self.remove(collision_effect2.get_lines())
        
        # 添加θ₂角度标注效果
        # 计算直线与x轴的交点
        k2 = np.tan(tangent_angle2)
        x_intercept2 = -1 - 2/k2  # 直线y = k(x+1) + 2 与x轴交点的x坐标
        intersection_point2 = axes.c2p(x_intercept2, 0)
        
        # 创建x轴正方向的参考线段
        x_axis_line2 = Line(
            start=intersection_point2,
            end=intersection_point2 + RIGHT * 1.5,
            color=GRAY,
            stroke_width=2
        )
        
        # 创建直线段（从交点向左上方延伸）
        line_segment2 = Line(
            start=intersection_point2,
            end=intersection_point2 + 1.5 * np.array([np.cos(tangent_angle2), np.sin(tangent_angle2), 0]),
            color=YELLOW,
            stroke_width=2
        )
        
        # 创建角度弧线（从x轴正方向到直线方向）
        angle_arc2 = Arc(
            radius=0.8,
            start_angle=0,
            angle=tangent_angle2,
            color=ORANGE,
            stroke_width=3,
            arc_center=intersection_point2
        )
        
        # 创建角度标签
        theta_label2 = MathTex(r"\theta_2", color=ORANGE).scale(0.7)
        # 将标签放在弧线的中间位置
        label_angle2 = tangent_angle2 / 2
        label_pos2 = intersection_point2 + 1.2 * np.array([np.cos(label_angle2), np.sin(label_angle2), 0])
        theta_label2.move_to(label_pos2)
        
        # 显示角度标注
        self.play(
            Create(x_axis_line2),
            Create(line_segment2),
            Create(angle_arc2),
            Write(theta_label2),
            run_time=1
        )
        
        
        
        self.wait(2)
        
        self.play(Write(k2_theta2_formula), run_time=1.5)
        self.wait(1)
        # 等待1秒后消失
        self.wait(1)
        self.play(
            FadeOut(x_axis_line2),
            FadeOut(line_segment2),
            FadeOut(angle_arc2),
            FadeOut(theta_label2),
            run_time=0.5
        )
        self.wait(1)