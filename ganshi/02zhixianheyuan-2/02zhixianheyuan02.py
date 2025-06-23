from manim import *
import numpy as np
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction

class Xiandaoke01(Scene):
    def construct(self):
        # 创建自定义坐标系
        axes = CustomAxes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=8,
            y_length=8,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        self.play(Create(axes), run_time=0.2)

        # 1. 创建根号x的图像 (y = x^0.5)
        sqrt_func = PowerFunction(0.5)
        sqrt_graph = axes.plot(sqrt_func.get_function(), x_range=[0, 2])
        sqrt_graph.set_color(BLUE).set_stroke_width(3)
        
        # 2. 创建圆 x^2 + y^2 = 1/5 (半径为sqrt(1/5) ≈ 0.447)
        from modules.function_definitions import Ellipse
        radius = math.sqrt(1/5)
        circle = Ellipse(radius, radius)  # 圆是特殊的椭圆，a=b=半径
        circle_graph = ParametricFunction(
            lambda t: axes.c2p(*circle.get_parametric_function()(t)),
            t_range=[0, 2 * math.pi]
        )
        circle_graph.set_color(RED).set_stroke_width(3)
        
        # 3. 计算精确的切线参数
        # 对于根号函数 y=√x 和圆 x²+y²=1/5 的公切线
        # 设切点在根号函数上为(t, √t)，切线斜率为 k = 1/(2√t)
        # 切线方程：y - √t = k(x - t) => y = kx + (√t - kt)
        # 设 c = √t - kt = √t - t/(2√t) = √t/2
        
        # 对于圆心在原点、半径为r的圆，直线y=kx+c与圆相切的条件是：
        # |c| = r√(1+k²)
        # 即 c² = r²(1+k²)
        
        # 代入我们的值：(√t/2)² = (1/5)(1 + 1/(4t))
        # t/4 = (1/5)(1 + 1/(4t)) = 1/5 + 1/(20t)
        # t/4 - 1/5 = 1/(20t)
        # (5t - 4)/20 = 1/(20t)
        # (5t - 4)t = 1
        # 5t² - 4t - 1 = 0
        # 解得：t = (4 ± √(16 + 20))/10 = (4 ± 6)/10
        # 取正根：t = 1 (另一根t = -0.2不合理)
        
        t = 1.0  # 根号函数上的切点x坐标
        cut_point_x = t
        cut_point_y = math.sqrt(t)  # = 1
        
        # 计算切线斜率和角度
        slope = 1 / (2 * math.sqrt(t))  # = 0.5
        angle = math.atan(slope)
        
        # 创建切线
        tangent_line = LinearFunctionPointSlope((cut_point_x, cut_point_y), angle)
        tangent_graph = axes.plot(tangent_line.get_function(), x_range=[-0.5, 2])
        tangent_graph.set_color(GREEN).set_stroke_width(2)
        
        # 标记根号函数上的切点
        cut_point_sqrt = Dot(axes.c2p(cut_point_x, cut_point_y), color=YELLOW, radius=0.08)
        
        # 计算圆上的切点
        # 切线方程：y = 0.5x + 0.5，即 x - 2y + 1 = 0
        # 圆心到直线的距离 = |1|/√(1+4) = 1/√5 = √(1/5) = r，验证相切
        # 圆上切点可通过 圆心 + r * 法向量 求得
        # 法向量方向：(1, -2)/√5，单位法向量：(1/√5, -2/√5)
        r = math.sqrt(1/5)
        normal_x = 1 / math.sqrt(5)
        normal_y = -2 / math.sqrt(5)
        circle_cut_x = 0 + r * normal_x  # = 1/5
        circle_cut_y = 0 + r * normal_y  # = -2/5
        cut_point_circle = Dot(axes.c2p(circle_cut_x, circle_cut_y), color=YELLOW, radius=0.08)
        
        # 添加标签
        sqrt_label = MathTex(r"y = \sqrt{x}", color=BLUE).scale(0.8)
        sqrt_label.next_to(axes.c2p(1.5, 1.2), RIGHT)
        
        circle_label = MathTex(r"x^2 + y^2 = \frac{1}{5}", color=RED).scale(0.8)
        circle_label.next_to(axes.c2p(-0.3, 0.6), LEFT)
        
        tangent_label = MathTex(r"y = \frac{1}{2}x + \frac{1}{2}", color=GREEN).scale(0.7)
        tangent_label.next_to(axes.c2p(1.2, 0.8), UR)
        
        # 添加切点标注
        sqrt_point_label = MathTex(r"(1, 1)", color=YELLOW).scale(0.6)
        sqrt_point_label.next_to(cut_point_sqrt, UR, buff=0.1)
        
        circle_point_label = MathTex(r"(\frac{1}{5}, -\frac{2}{5})", color=YELLOW).scale(0.6)
        circle_point_label.next_to(cut_point_circle, DR, buff=0.1)
        
        # 动画演示
        self.play(Create(sqrt_graph), run_time=2)
        self.play(Write(sqrt_label), run_time=1)
        
        self.play(Create(circle_graph), run_time=2)
        self.play(Write(circle_label), run_time=1)
        
        self.play(Create(tangent_graph), run_time=2)
        self.play(Write(tangent_label), run_time=1)
        
        self.play(
            Create(cut_point_sqrt),
            Create(cut_point_circle),
            run_time=1
        )
        
    
        
        self.wait(3)
        