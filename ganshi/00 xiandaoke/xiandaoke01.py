from manim import *
import numpy as np

class LineEllipseTangentAnimation(Scene):
    def construct(self):
        # 设置标题
        title = Text("直线与椭圆相切问题", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # 创建坐标系
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": [-3, -2, -1, 1, 2, 3]},
            y_axis_config={"numbers_to_include": [-2, -1, 1, 2]},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        self.play(Create(axes), Write(axes_labels))
        self.wait(1)
        
        # 创建椭圆 (例: x²/4 + y²/1 = 1)
        ellipse = Ellipse(width=4, height=2, color=BLUE)
        ellipse_label = MathTex(r"\frac{x^2}{4} + y^2 = 1", color=BLUE).scale(0.8)
        ellipse_label.next_to(ellipse, UR, buff=0.5)
        
        self.play(Create(ellipse), Write(ellipse_label))
        self.wait(1)
        
        # 显示问题描述
        problem_text = Text("求直线与椭圆相切时，直线与x轴的夹角", font_size=24)
        problem_text.next_to(title, DOWN, buff=0.3)
        self.play(Write(problem_text))
        self.wait(1)
        
        # 创建相切直线 (斜率为√3，通过椭圆上某点)
        # 设直线方程: y = kx + b，相切条件下 k = √3
        k = np.sqrt(3)
        # 对于椭圆 x²/4 + y² = 1 和直线 y = kx + b
        # 相切条件: b² = 4k² + 1，选择正值
        b = np.sqrt(4 * k**2 + 1)
        
        # 切点坐标
        x_tangent = -2 * k * b / (4 * k**2 + 1)
        y_tangent = k * x_tangent + b
        
        tangent_line = axes.plot(lambda x: k * x + b, x_range=[-3, 1], color=RED)
        tangent_label = MathTex(r"y = \sqrt{3}x + b", color=RED).scale(0.8)
        tangent_label.next_to(tangent_line, UR, buff=0.2)
        
        # 标记切点
        tangent_point = Dot(axes.coords_to_point(x_tangent, y_tangent), color=YELLOW, radius=0.08)
        
        self.play(Create(tangent_line), Write(tangent_label))
        self.play(Create(tangent_point))
        self.wait(2)
        
        # 开始代数推导过程
        self.play(FadeOut(problem_text))
        
        # 第一步：几何关系转代数关系
        step1 = VGroup(
            Text("步骤1: 几何关系 → 代数关系", font_size=20, color=YELLOW),
            Text("相切 ⟺ 只有一个交点", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT)
        step1.to_edge(LEFT).shift(UP * 2)
        
        self.play(Write(step1))
        self.wait(2)
        
        # 第二步：联立方程
        step2 = VGroup(
            Text("步骤2: 联立方程", font_size=20, color=YELLOW),
            MathTex(r"\begin{cases} y = kx + b \\ \frac{x^2}{4} + y^2 = 1 \end{cases}", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT)
        step2.next_to(step1, DOWN, buff=0.5, aligned_edge=LEFT)
        
        self.play(Write(step2))
        self.wait(2)
        
        # 第三步：消元得到二次方程
        step3 = VGroup(
            Text("步骤3: 代入消元", font_size=20, color=YELLOW),
            MathTex(r"\frac{x^2}{4} + (kx + b)^2 = 1", font_size=16),
            MathTex(r"\frac{x^2}{4} + k^2x^2 + 2kbx + b^2 = 1", font_size=16),
            MathTex(r"(\frac{1}{4} + k^2)x^2 + 2kbx + (b^2 - 1) = 0", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT)
        step3.next_to(step2, DOWN, buff=0.5, aligned_edge=LEFT)
        
        self.play(Write(step3[0]))
        self.wait(1)
        self.play(Write(step3[1]))
        self.wait(1)
        self.play(Write(step3[2]))
        self.wait(1)
        self.play(Write(step3[3]))
        self.wait(2)
        
        # 清除左侧推导，显示判别式条件
        self.play(FadeOut(step1), FadeOut(step2), FadeOut(step3))
        
        # 第四步：相切条件 Δ = 0
        step4 = VGroup(
            Text("步骤4: 相切条件 Δ = 0", font_size=20, color=YELLOW),
            MathTex(r"\Delta = (2kb)^2 - 4(\frac{1}{4} + k^2)(b^2 - 1) = 0", font_size=16),
            MathTex(r"4k^2b^2 - 4(\frac{1}{4} + k^2)(b^2 - 1) = 0", font_size=16),
            MathTex(r"k^2b^2 - (\frac{1}{4} + k^2)(b^2 - 1) = 0", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT)
        step4.to_edge(LEFT).shift(UP * 1.5)
        
        self.play(Write(step4))
        self.wait(3)
        
        # 第五步：化简得到关于k的方程
        step5 = VGroup(
            Text("步骤5: 化简求解", font_size=20, color=YELLOW),
            MathTex(r"k^2b^2 - \frac{b^2 - 1}{4} - k^2(b^2 - 1) = 0", font_size=16),
            MathTex(r"k^2b^2 - k^2b^2 + k^2 - \frac{b^2 - 1}{4} = 0", font_size=16),
            MathTex(r"k^2 = \frac{b^2 - 1}{4}", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT)
        step5.next_to(step4, DOWN, buff=0.5, aligned_edge=LEFT)
        
        self.play(Write(step5))
        self.wait(3)
        
        # 第六步：特定情况下的解
        step6 = VGroup(
            Text("步骤6: 特定情况求解", font_size=20, color=YELLOW),
            MathTex(r"\text{设椭圆} \frac{x^2}{4} + y^2 = 1", font_size=16),
            MathTex(r"\text{经过计算得到} k = \sqrt{3}", font_size=16, color=GREEN),
            MathTex(r"\text{夹角} \theta = \arctan(\sqrt{3}) = 60°", font_size=16, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT)
        step6.next_to(step5, DOWN, buff=0.5, aligned_edge=LEFT)
        
        self.play(Write(step6))
        self.wait(2)
        
        # 在图形上标注角度
        angle_arc = Arc(
            start_angle=0,
            angle=PI/3,
            radius=0.8,
            arc_center=axes.coords_to_point(0, 0),
            color=GREEN
        )
        angle_label = MathTex("60°", color=GREEN, font_size=24)
        angle_label.next_to(angle_arc, RIGHT, buff=0.1)
        
        self.play(Create(angle_arc), Write(angle_label))
        self.wait(2)
        
        # 最终总结
        conclusion = VGroup(
            Text("总结:", font_size=24, color=YELLOW),
            Text("几何关系(相切) → 代数条件(Δ=0) → 数值解(k=√3) → 几何结果(60°)", font_size=18)
        ).arrange(DOWN)
        conclusion.to_edge(DOWN, buff=0.5)
        
        self.play(Write(conclusion))
        self.wait(3)
        
        # 突出显示最终结果
        final_highlight = SurroundingRectangle(
            VGroup(step6[2], step6[3]), 
            color=YELLOW, 
            buff=0.1
        )
        self.play(Create(final_highlight))
        self.wait(2)
        
        self.wait(3)
