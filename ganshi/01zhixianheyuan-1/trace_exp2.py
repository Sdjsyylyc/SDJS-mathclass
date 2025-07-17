from manim import *
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__))))))
from modules import CustomAxes, SliderComponent, LinearFunctionPointSlope, CollisionEffect, CustomCircle

def TraceExp2(Scene):
    def construct(self):
        axes = CustomAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"tip_width": 0.1},
            x_length=7,
            y_length=7,
        )

        # 暂定