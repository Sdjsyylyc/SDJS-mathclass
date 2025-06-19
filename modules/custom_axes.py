from manim import *
import numpy as np

class CustomAxes(VGroup):
    def __init__(
        self,
        x_range=[-5, 5, 1],
        y_range=[-3, 3, 1],
        x_length=10,
        y_length=6,
        axis_config=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.x_range = x_range
        self.y_range = y_range
        self.x_length = x_length
        self.y_length = y_length
        
        # 默认轴配置
        default_config = {
            "color": WHITE,
            "stroke_width": 2,
            "tip_length": 0.2,
        }
        if axis_config:
            default_config.update(axis_config)
        self.axis_config = default_config
        
        # 创建x轴
        self.x_axis = Arrow(
            start=LEFT * self.x_length/2,
            end=RIGHT * self.x_length/2,
            color=self.axis_config["color"],
            stroke_width=self.axis_config["stroke_width"],
            tip_length=self.axis_config["tip_length"],
            buff=0
        )
        
        # 创建y轴
        self.y_axis = Arrow(
            start=DOWN * self.y_length/2,
            end=UP * self.y_length/2,
            color=self.axis_config["color"],
            stroke_width=self.axis_config["stroke_width"],
            tip_length=self.axis_config["tip_length"],
            buff=0
        )
        
        self.add(self.x_axis, self.y_axis)
        
        # 计算单位长度
        self.x_unit = self.x_length / (self.x_range[1] - self.x_range[0])
        self.y_unit = self.y_length / (self.y_range[1] - self.y_range[0])
    
    def c2p(self, x, y):
        """坐标转换：数学坐标到屏幕坐标"""
        # 将数学坐标转换为相对于原点的屏幕坐标
        screen_x = (x - (self.x_range[0] + self.x_range[1])/2) * self.x_unit
        screen_y = (y - (self.y_range[0] + self.y_range[1])/2) * self.y_unit
        
        # 加上这个坐标系的位置偏移
        return self.get_center() + np.array([screen_x, screen_y, 0])
    
    def p2c(self, point):
        """坐标转换：屏幕坐标到数学坐标"""
        relative_point = point - self.get_center()
        math_x = relative_point[0] / self.x_unit + (self.x_range[0] + self.x_range[1])/2
        math_y = relative_point[1] / self.y_unit + (self.y_range[0] + self.y_range[1])/2
        return [math_x, math_y]
    
    def plot(self, func, x_range=None, **kwargs):
        """绘制函数图像"""
        if x_range is None:
            x_range = [self.x_range[0], self.x_range[1]]
        
        # 创建采样点
        x_values = np.linspace(x_range[0], x_range[1], 200)
        points = []
        
        for x in x_values:
            try:
                y = func(x)
                # 检查y值是否在合理范围内
                if self.y_range[0] - 1 <= y <= self.y_range[1] + 1:
                    points.append(self.c2p(x, y))
            except:
                continue
        
        if len(points) < 2:
            return VGroup()  # 返回空组如果没有足够的点
        
        # 创建路径
        path = VMobject(**kwargs)
        path.set_points_as_corners(points)
        return path 