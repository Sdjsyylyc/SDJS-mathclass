from manim import *
import numpy as np

class TriangleMedianScene(Scene):
    def construct(self):
        # 设置画面分区 - 左侧2/3为动画区，右侧1/3为公式区
        animation_area = Rectangle(
            width=config.frame_width * 2/3,
            height=config.frame_height,
            stroke_opacity=0,
            fill_opacity=0
        ).to_edge(LEFT, buff=0)
        
        formula_area = Rectangle(
            width=config.frame_width * 1/3,
            height=config.frame_height,
            stroke_opacity=0,
            fill_opacity=0
        ).to_edge(RIGHT, buff=0.8)  # 左移公式区
        
        # 创建一个坐标系，方便定位(不会显示)
        axes = Axes(
            x_range=[-5, 5],
            y_range=[-3, 5],
            x_length=8,
            y_length=6,
        ).move_to(animation_area.get_center() + UP * 1.0)  # 更上移以改善显示
        
        # 创建明显不规则的三角形
        A = axes.c2p(-4.2, -1.2)
        B = axes.c2p(3.8, 0.5)
        C = axes.c2p(-1.5, 4.0)
        
        triangle = Polygon(A, B, C, color=BLUE, fill_opacity=0.2)
        
        # 标注三角形顶点
        label_A = MathTex("A", font_size=40, color=BLUE_D).next_to(A, DOWN+LEFT, buff=0.2)
        label_B = MathTex("B", font_size=40, color=RED_D).next_to(B, DOWN+RIGHT, buff=0.2)
        label_C = MathTex("C", font_size=40, color=GREEN_D).next_to(C, UP, buff=0.2)
        
        # 绘制三角形边（不标记边长）
        side_AB = Line(A, B, color=BLUE, stroke_width=3)
        side_BC = Line(B, C, color=RED, stroke_width=3)
        side_AC = Line(A, C, color=GREEN, stroke_width=3)
        
        self.play(
            Create(triangle),
            Write(label_A), Write(label_B), Write(label_C),
            Create(side_AB), Create(side_BC), Create(side_AC)
        )
        self.wait(1)
        
        # 计算AB的中点D
        D = (A + B) / 2
        
        # 创建中线CD
        median_CD = Line(C, D, color=YELLOW, stroke_width=4)
        
        # 添加中线
        self.play(Create(median_CD))
        self.wait(1)
        
        # 标记点D
        dot_D = Dot(D, color=YELLOW)
        label_D = MathTex("D", font_size=36, color=YELLOW).next_to(D, DOWN, buff=0.2)
        
        self.play(
            Create(dot_D),
            Write(label_D)
        )
        self.wait(1)
        
        # 右侧推导区域 - 纯符号表示
        median_name = MathTex("|CD|", font_size=36, color=YELLOW).move_to(formula_area.get_center() + UP * 3)
        self.play(Write(median_name))
        self.wait(1)
        
        # 右侧使用纯符号推导中线长性质 - 简化版本，字体更小，行更短
        derivation_1 = MathTex("\\triangle ABC").scale(0.8).move_to(formula_area.get_center() + UP * 2.5)
        self.play(Write(derivation_1))
        self.wait(1)
        
        # D是AB的中点
        derivation_2 = MathTex("D \\in AB", "\\quad", "|AD| = |DB|").scale(0.75).move_to(formula_area.get_center() + UP * 1.5)
        self.play(Write(derivation_2))
        self.wait(1)
        
        # 创建三角形和中线的副本，准备旋转
        triangle_copy = triangle.copy()
        triangle_copy.set_color(BLUE_A)
        triangle_copy.set_fill(opacity=0.2)
        
        median_copy = median_CD.copy()
        median_copy.set_color(YELLOW_A)
        
        self.play(
            Create(triangle_copy),
            Create(median_copy)
        )
        
        # 将复制的三角形和中线沿点D旋转180度
        self.play(
            Rotate(
                triangle_copy, 
                angle=PI, 
                about_point=D,
                rate_func=smooth
            ),
            Rotate(
                median_copy, 
                angle=PI, 
                about_point=D,
                rate_func=smooth
            ),
            run_time=2
        )
        self.wait(1)
        
        # 计算旋转后C点的新位置（C关于D的对称点）
        C_prime = 2*D - C
        
        # 标记旋转后的C点为C'
        label_C_prime = MathTex("C'", font_size=40, color=GREEN_D).next_to(C_prime, DOWN, buff=0.2)
        self.play(Write(label_C_prime))
        self.wait(1)
        
        # 按顺序高亮显示AC、BC
        AC_highlight = Line(A, C, color=YELLOW, stroke_width=6)
        self.play(Create(AC_highlight), run_time=1)
        self.wait(0.5)
        
        BC_highlight = Line(B, C, color=YELLOW, stroke_width=6)
        self.play(Create(BC_highlight), run_time=1)
        self.wait(0.5)
        
        # 将BC的高亮线平移到AC'位置
        AC_prime = Line(A, C_prime, color=YELLOW, stroke_width=6)
        self.play(
            Transform(BC_highlight, AC_prime),
            run_time=1.5
        )
        self.wait(0.5)
        
        # 高亮CC'
        CC_prime = Line(C, C_prime, color=RED, stroke_width=6)
        self.play(Create(CC_prime), run_time=1.5)
        self.wait(1)
        
        # 余弦定理简化版本 - 分成多行显示，字体更小
        derivation_4a = MathTex("\\triangle ACC':").scale(0.75).move_to(formula_area.get_center() + UP * 0.5)
        derivation_4b = MathTex("|CC'|^2 = |AC|^2 + |AC'|^2").scale(0.7).move_to(formula_area.get_center() - UP * 0)
        derivation_4c = MathTex("-2|AC||AC'|\\cos \\angle CAC'").scale(0.7).move_to(formula_area.get_center() - UP * 0.5)
        
        self.play(Write(derivation_4a))
        self.play(Write(derivation_4b))
        self.play(Write(derivation_4c))
        self.wait(1)
        
        # 使用余弦定理 - 分成多行显示，字体更小
        derivation_5a = MathTex("\\angle CAC' + \\angle ACB = \\pi").scale(0.7).move_to(formula_area.get_center() - UP * 1.5)
        derivation_5b = MathTex("\\Rightarrow \\cos \\angle CAC' = -\\cos \\angle ACB").scale(0.65).move_to(formula_area.get_center() - UP * 2)
        
        self.play(Write(derivation_5a))
        self.play(Write(derivation_5b))
        self.wait(1)
        
        # 最终结果 - 分成两行显示，字体适当
        final_formula1 = MathTex("|CD|^2 = ").scale(0.85).move_to(formula_area.get_center())
        final_formula2 = MathTex("\\frac14(|AC|^2 + |BC|^2 + 2|AC||BC|\\cos \\angle ACB)", color=BLUE_A).scale(0.5).move_to(formula_area.get_center() - UP * 1.0)
        
        # 清除之前的所有推导
        self.play(
            FadeOut(median_name),
            FadeOut(derivation_1),
            FadeOut(derivation_2),
            FadeOut(derivation_4a),
            FadeOut(derivation_4b),
            FadeOut(derivation_4c),
            FadeOut(derivation_5a),
            FadeOut(derivation_5b),
        )
        
        self.play(Write(final_formula1))
        self.play(Write(final_formula2))
        self.wait(1)
        
        # 将两个公式组合起来，以便创建框
        final_formula_group = VGroup(final_formula1, final_formula2)
        
        # 结果框
        result_box = SurroundingRectangle(final_formula_group, color=YELLOW, buff=0.2)
        self.play(Create(result_box))
        self.wait(2) 