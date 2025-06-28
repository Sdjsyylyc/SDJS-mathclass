from manim import *
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect,LinearFunctionPointSlope,CustomCircle,LinearFunctionGeneral

class zhixianheyuan01(Scene):
    def construct(self):
        # 创建坐标系，x范围(-2,6)，y范围(-2,6)
        axes = CustomAxes(
            x_range=[-3, 9, 1],  # [最小值, 最大值, 步长]
            y_range=[-3, 9, 1],  # [最小值, 最大值, 步长]
            x_length=8,          # x轴在屏幕上的长度
            y_length=8,          # y轴在屏幕上的长度
            origin_point=DL + LEFT * 1 + DOWN * 2,  # 坐标系原点更靠左下角
            axis_labels=True,    # 显示轴标签
            x_label="x",      # x轴标签（数学公式格式）
            y_label="y",       # y轴标签（数学公式格式）
        )
        # 添加到场景中
        self.add(axes)
        
        # 创建第一个圆：(x+1)^2 + (y-1)^2 = 2 (圆心在(-1,1)，半径为√2)
        circle1 = CustomCircle(center=(-1, 1), radius=np.sqrt(2))
        graph1 = circle1.plot_in(axes, color=BLUE, stroke_width=3)
        
        # 创建第二个圆：(x-3)^2 + (y-4)^2 = 16 (圆心在(3,4)，半径为3)
        circle2 = CustomCircle(center=(3, 4), radius=3)
        graph2 = circle2.plot_in(axes, color=GREEN, stroke_width=3)
      
        
                # 使用动画的方式画出圆
        # 先画出第一个圆：x^2 + y^2 = 1 (蓝色)
        self.play(Create(graph1), run_time=2)
        self.wait(0.5)
        
                # 再画出第二个圆：(x-3)^2 + (y-4)^2 = 16 (红色)  
        self.play(Create(graph2), run_time=2)
        self.wait(1)

        # 创建可调节参数的直线 Ax + By + C = 0
        # 初始参数：A=1, B=-1, C=0 表示直线 x - y = 0 即 y = x
        A_tracker = ValueTracker(1)
        B_tracker = ValueTracker(-1) 
        C_tracker = ValueTracker(0)
        
        # 创建动态更新的直线 - 使用 always_redraw 确保参数变化时直线会更新
        line_graph = always_redraw(lambda: 
            LinearFunctionGeneral(A_tracker, B_tracker, C_tracker).plot_in(
                axes, x_range=(-2, 10), y_range=(-2, 10), 
                color=YELLOW, stroke_width=4)
        )
        
        # 画出直线和方程文本
        self.play(Create(line_graph))
        self.wait(1)
        
        # 动画1: 改变A参数 (1 -> 2)
        self.play(A_tracker.animate.set_value(2), run_time=2)
        self.wait(1)
        
        # 动画2: 改变B参数 (-1 -> -2)
        self.play(B_tracker.animate.set_value(-2), run_time=2)
        self.wait(1)
        
        # 动画3: 改变C参数 (0 -> 3)
        self.play(C_tracker.animate.set_value(3), run_time=2)
        self.wait(1)
        
        # 动画4: 同时改变多个参数
        self.play(
            A_tracker.animate.set_value(1),
            B_tracker.animate.set_value(1),
            C_tracker.animate.set_value(-5),
            run_time=3
        )
        self.wait(2)        