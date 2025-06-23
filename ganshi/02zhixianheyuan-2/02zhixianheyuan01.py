from manim import *
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect,LinearFunctionPointSlope

class zhixianheyuan01(Scene):
    def construct(self):
        # 创建坐标系，x范围(-2,6)，y范围(-2,6)
        axes = CustomAxes(
            x_range=[-2, 6, 1],  # [最小值, 最大值, 步长]
            y_range=[-2, 6, 1],  # [最小值, 最大值, 步长]
            x_length=8,          # x轴在屏幕上的长度
            y_length=8,          # y轴在屏幕上的长度
            origin_point=DL + LEFT * 1.5 + DOWN * 2,  # 坐标系原点更靠左下角
            axis_labels=True,    # 显示轴标签
            x_label="x",      # x轴标签（数学公式格式）
            y_label="y",       # y轴标签（数学公式格式）
        )
        # 添加到场景中
        self.add(axes)
        
        # 等待一段时间
        self.wait(2)