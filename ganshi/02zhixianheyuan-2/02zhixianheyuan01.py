from manim import *
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, LinearFunctionTwoPoints
class zhixianheyuan01(Scene):
    def construct(self):
        # 创建坐标系，x范围(-2,6)，y范围(-2,6)
        axes = CustomAxes(
            x_range=[-2, 6, 1],  # [最小值, 最大值, 步长]
            y_range=[-2, 6, 1],  # [最小值, 最大值, 步长]
            x_length=6,          # x轴在屏幕上的长度
            y_length=6,          # y轴在屏幕上的长度
            origin_point=(DOWN + LEFT)*1.5,  # 坐标系原点更靠左下角
            axis_labels=True,    # 显示轴标签
            x_label="x",      # x轴标签（数学公式格式）
            y_label="y",       # y轴标签（数学公式格式）
        )
        # 添加到场景中
        self.add(axes)

        R_tracker = ValueTracker(4)
        unit_len = axes.get_x_unit()

        o_dot = Dot(color=WHITE, radius=0.1).move_to(axes.c2p(0, 0))
        o1_dot = Dot(color=WHITE, radius=0.1).move_to(axes.c2p(3, 4))
        circ1 = Circle(radius=unit_len, color=WHITE, stroke_width=1).move_to(o_dot.get_center())
        circ2 = always_redraw(lambda: Circle(radius=R_tracker.get_value()*unit_len, color=WHITE, stroke_width=1).move_to(o1_dot.get_center()))
        self.play(Create(o_dot), Create(o1_dot), Create(circ1), Create(circ2))

        self.wait(2)
        
        def get_tangent_line():
            R = R_tracker.get_value()
            c1 = -1 - R
            c2 = -1 + R
            b21 = (4*c2+3*np.sqrt(25-c2**2))/25
            b22 = (4*c2-3*np.sqrt(25-c2**2))/25
            if c2-4*b21 != 0:
                x1 = -3/(c2-4*b21)
            else:
                x1 = float('inf')
            if c2-4*b22 != 0:
                x2 = -3/(c2-4*b22)
            else:
                x2 = float('inf')
            if b21 != 0:
                y1 = -1/b21
            else:
                y1 = float('inf')
            if b22 != 0:
                y2 = -1/b22
            else:
                y2 = float('inf')
            l1 = LinearFunctionTwoPoints((x1, 0), (0, y1))
            l2 = LinearFunctionTwoPoints((x2, 0), (0, y2))
            l1_graph = l1.plot_in(axes, [-2, 6], [-2, 6], color=GREEN)
            l2_graph = l2.plot_in(axes, [-2, 6], [-2, 6], color=GREEN)
            if R > 4:
                return VGroup(l1_graph, l2_graph)
            elif R == 4:
                b11 = (4*c1)/25
                l3 = LinearFunctionTwoPoints((-3/(c1-4*b11), 0), (0, -1/b11))
                l3_graph = l3.plot_in(axes, [-2, 6], [-2, 6], color=RED)
                return VGroup(l1_graph, l2_graph, l3_graph)
            else:
                b11 = (4*c1+3*np.sqrt(25-c1**2))/25
                b12 = (4*c1-3*np.sqrt(25-c1**2))/25
                l3 = LinearFunctionTwoPoints((-3/(c1-4*b11), 0), (0, -1/b11))
                l4 = LinearFunctionTwoPoints((-3/(c1-4*b12), 0), (0, -1/b12))
                l3_graph = l3.plot_in(axes, [-2, 6], [-2, 6], color=RED)
                l4_graph = l4.plot_in(axes, [-2, 6], [-2, 6], color=RED)
                return VGroup(l1_graph, l2_graph, l3_graph, l4_graph)
        
        tangent_line = always_redraw(get_tangent_line)
        self.play(Create(tangent_line))
        self.wait(2)

        self.play(R_tracker.animate.set_value(5), run_time=4)
        self.wait(3)
        self.play(R_tracker.animate.set_value(3), run_time=4)
        self.wait(3)



