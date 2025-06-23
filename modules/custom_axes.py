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
        origin_point=ORIGIN,  # 坐标系原点在屏幕上的位置
        axis_labels=True,     # 是否显示轴标签
        x_label="x",          # x轴标签文本
        y_label="y",          # y轴标签文本
        label_config=None,    # 标签配置
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.x_range = x_range
        self.y_range = y_range
        self.x_length = x_length
        self.y_length = y_length
        self.origin_point = origin_point
        self.axis_labels = axis_labels
        self.x_label = x_label
        self.y_label = y_label
        
        # 默认轴配置
        default_config = {
            "color": WHITE,
            "stroke_width": 2,
            "tip_length": 0.2,
        }
        if axis_config:
            default_config.update(axis_config)
        self.axis_config = default_config
        
        # 默认标签配置
        default_label_config = {
            "font_size": 24,
            "color": WHITE,
        }
        if label_config:
            default_label_config.update(label_config)
        self.label_config = default_label_config
        
        # 计算单位长度
        self.x_unit = self.x_length / (self.x_range[1] - self.x_range[0])
        self.y_unit = self.y_length / (self.y_range[1] - self.y_range[0])
        
        # 创建轴
        self._create_axes()
    
    def _create_axes(self):
        """创建x轴和y轴"""
        # 创建x轴 - 从x_range[0]到x_range[1]
        self.x_axis = Arrow(
            start=self.c2p(self.x_range[0], 0),
            end=self.c2p(self.x_range[1], 0),
            color=self.axis_config["color"],
            stroke_width=self.axis_config["stroke_width"],
            tip_length=self.axis_config["tip_length"],
            buff=0
        )
        
        # 创建y轴 - 从y_range[0]到y_range[1]
        self.y_axis = Arrow(
            start=self.c2p(0, self.y_range[0]),
            end=self.c2p(0, self.y_range[1]),
            color=self.axis_config["color"],
            stroke_width=self.axis_config["stroke_width"],
            tip_length=self.axis_config["tip_length"],
            buff=0
        )
        
        self.add(self.x_axis, self.y_axis)
        
        # 创建轴标签
        if self.axis_labels:
            # x轴标签 - 位于x轴箭头右侧
            self.x_axis_label = Text(
                self.x_label,
                font_size=self.label_config["font_size"],
                color=self.label_config["color"]
            )
            self.x_axis_label.move_to(self.x_axis.get_end()+0.2*RIGHT)
            
            # y轴标签 - 位于y轴箭头上方
            self.y_axis_label = Text(
                self.y_label,
                font_size=self.label_config["font_size"],
                color=self.label_config["color"]
            )
            self.y_axis_label.move_to(self.y_axis.get_end()+0.2*UP)
            
            self.add(self.x_axis_label, self.y_axis_label)
    
    def c2p(self, x, y):
        """坐标转换：数学坐标到屏幕坐标"""
        # 将数学坐标转换为相对于坐标系原点的屏幕坐标
        screen_x = x * self.x_unit
        screen_y = y * self.y_unit
        
        # 加上坐标系在屏幕上的位置偏移
        return self.origin_point + np.array([screen_x, screen_y, 0])
    
    def p2c(self, point):
        """坐标转换：屏幕坐标到数学坐标"""
        # 减去坐标系原点的位置偏移
        relative_point = point - self.origin_point
        
        # 转换为数学坐标
        math_x = relative_point[0] / self.x_unit
        math_y = relative_point[1] / self.y_unit
        
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
                # 检查y值是否在合理范围内（扩展一点范围以允许超出边界的绘制）
                y_margin = abs(self.y_range[1] - self.y_range[0]) * 0.5
                if self.y_range[0] - y_margin <= y <= self.y_range[1] + y_margin:
                    points.append(self.c2p(x, y))
            except:
                continue
        
        if len(points) < 2:
            return VGroup()  # 返回空组如果没有足够的点
        
        # 创建路径
        path = VMobject()
        path.set_points_as_corners(points)
        
        # 设置样式
        if 'color' in kwargs:
            path.set_color(kwargs['color'])
        if 'stroke_width' in kwargs:
            path.set_stroke_width(kwargs['stroke_width'])
        if 'stroke_opacity' in kwargs:
            path.set_stroke_opacity(kwargs['stroke_opacity'])
        
        return path
    
    def add_coordinates(self, x_values=None, y_values=None, **kwargs):
        """添加坐标标记"""
        coord_group = VGroup()
        
        # 默认坐标值
        if x_values is None:
            x_values = np.arange(self.x_range[0], self.x_range[1] + self.x_range[2], self.x_range[2])
        if y_values is None:
            y_values = np.arange(self.y_range[0], self.y_range[1] + self.y_range[2], self.y_range[2])
        
        # 添加x轴坐标
        for x in x_values:
            if x != 0:  # 不在原点添加标记
                label = Text(str(int(x) if x.is_integer() else f"{x:.1f}"), font_size=20)
                label.move_to(self.c2p(x, 0))
                label.shift(DOWN * 0.3)
                coord_group.add(label)
        
        # 添加y轴坐标
        for y in y_values:
            if y != 0:  # 不在原点添加标记
                label = Text(str(int(y) if isinstance(y, (int, float)) and y.is_integer() else f"{y:.1f}"), font_size=20)
                label.move_to(self.c2p(0, y))
                label.shift(LEFT * 0.3)
                coord_group.add(label)
        self.add(coord_group)
        return coord_group
    
    def get_origin_point(self):
        """获取数学坐标原点(0,0)在屏幕上的位置"""
        return self.c2p(0, 0)
    
    def set_origin_point(self, new_origin):
        """设置坐标系原点位置"""
        self.origin_point = new_origin
        self.move_to(new_origin)
    
    def get_x_unit(self):
        return self.x_unit
    
    def get_y_unit(self):
        return self.y_unit
    
    def set_axis_labels(self, x_label=None, y_label=None):
        """设置轴标签文本"""
        if hasattr(self, 'x_axis_label') and x_label is not None:
            self.x_axis_label.become(Text(
                x_label,
                font_size=self.label_config["font_size"],
                color=self.label_config["color"]
            ))
            self.x_axis_label.move_to(self.x_axis.get_end()+0.2*RIGHT)
        
        if hasattr(self, 'y_axis_label') and y_label is not None:
            self.y_axis_label.become(Text(
                y_label,
                font_size=self.label_config["font_size"],
                color=self.label_config["color"]
            ))
            self.y_axis_label.move_to(self.y_axis.get_end()+0.2*UP)
    
    def show_axis_labels(self):
        """显示轴标签"""
        if hasattr(self, 'x_axis_label'):
            self.x_axis_label.set_opacity(1)
        if hasattr(self, 'y_axis_label'):
            self.y_axis_label.set_opacity(1)
    
    def hide_axis_labels(self):
        """隐藏轴标签"""
        if hasattr(self, 'x_axis_label'):
            self.x_axis_label.set_opacity(0)
        if hasattr(self, 'y_axis_label'):
            self.y_axis_label.set_opacity(0)
    
    