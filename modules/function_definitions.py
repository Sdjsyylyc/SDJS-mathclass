"""
数学函数定义模块

包含常见数学函数的类定义，支持ValueTracker参数控制
每个类都可以生成函数句柄，并提供相关的计算方法
"""

import numpy as np
import math
from manim import ValueTracker, VMobject, WHITE, ParametricFunction, FunctionGraph, Dot, Line, DashedLine


class LinearFunctionTwoPoints:
    """两点式直线：通过两个点定义的直线"""
    
    def __init__(self, point1, point2):
        """
        初始化两点式直线
        
        Args:
            point1: 第一个点，可以是(x1, y1)元组或包含ValueTracker的列表
            point2: 第二个点，可以是(x2, y2)元组或包含ValueTracker的列表
        """
        self.point1 = point1
        self.point2 = point2
    
    def _get_point_value(self, point):
        """获取点的实际数值"""
        if isinstance(point[0], ValueTracker):
            return (point[0].get_value(), point[1].get_value())
        return point
    
    def get_function(self):
        """返回函数句柄"""
        def func(x):
            p1 = self._get_point_value(self.point1)
            p2 = self._get_point_value(self.point2)
            
            x1, y1 = p1
            x2, y2 = p2
            
            if abs(x2 - x1) < 1e-10:  # 垂直线
                return float('inf') if x == x1 else float('nan')
            
            # 两点式公式：(y - y1) / (y2 - y1) = (x - x1) / (x2 - x1)
            return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
        
        return func
    
    def get_slope(self):
        """获取当前斜率"""
        p1 = self._get_point_value(self.point1)
        p2 = self._get_point_value(self.point2)
        
        x1, y1 = p1
        x2, y2 = p2
        
        if abs(x2 - x1) < 1e-10:
            return float('inf')
        
        return (y2 - y1) / (x2 - x1)
    
    def get_range(self, y_min, y_max):
        """根据y范围返回对应的x范围"""
        p1 = self._get_point_value(self.point1)
        p2 = self._get_point_value(self.point2)
        
        x1, y1 = p1
        x2, y2 = p2
        
        if abs(x2 - x1) < 1e-10:  # 垂直线
            return (x1, x1)
        
        slope = (y2 - y1) / (x2 - x1)
        
        # 根据 y = y1 + slope * (x - x1) 求解 x
        x_at_y_min = x1 + (y_min - y1) / slope
        x_at_y_max = x1 + (y_max - y1) / slope
        
        return (min(x_at_y_min, x_at_y_max), max(x_at_y_min, x_at_y_max))
    
    def plot_in(self, axes, x_range, y_range=None, color=WHITE, stroke_width=2, stroke_opacity=1):
        """
        在指定的坐标轴中绘制函数图像
        
        Args:
            axes: Manim的Axes对象
            x_range: x值范围，(x_min, x_max)
            y_range: y值范围限制，(y_min, y_max)，可选
            color: 线条颜色，可以是ValueTracker或颜色值
            stroke_width: 线条宽度，可以是ValueTracker或数值
            stroke_opacity: 线条透明度，可以是ValueTracker或数值
            
        Returns:
            VMobject: 函数图像对象
        """
        def _get_param_value(param):
            """获取参数的实际值"""
            if isinstance(param, ValueTracker):
                return param.get_value()
            return param
        
        def create_graph():
            func = self.get_function()
            x_min, x_max = x_range
            
            # 如果有y_range限制，需要调整x_range
            if y_range is not None:
                y_min, y_max = y_range
                try:
                    # 计算在y_range限制下的实际x范围
                    func_x_range = self.get_range(y_min, y_max)
                    if not (math.isnan(func_x_range[0]) or math.isnan(func_x_range[1])):
                        x_min = max(x_min, func_x_range[0])
                        x_max = min(x_max, func_x_range[1])
                except:
                    pass
            
            # 创建受限制的函数
            def limited_func(x):
                y = func(x)
                if y_range is not None:
                    y_min, y_max = y_range
                    if y < y_min or y > y_max:
                        return float('nan')
                return y
            
            try:
                graph = axes.plot(limited_func, x_range=[x_min, x_max], discontinuities=[], 
                                color=_get_param_value(color),
                                stroke_width=_get_param_value(stroke_width),
                                stroke_opacity=_get_param_value(stroke_opacity))
                return graph
            except:
                # 如果绘制失败，返回空的VMobject
                return VMobject()
        
        return create_graph()


class LinearFunctionPointSlope:
    """点斜式直线：通过一个点和倾斜角定义的直线"""
    
    def __init__(self, point, angle):
        """
        初始化点斜式直线
        
        Args:
            point: 过线的点，可以是(x0, y0)元组或包含ValueTracker的列表
            angle: 倾斜角（弧度），可以是ValueTracker或数值
        """
        self.point = point
        self.angle = angle
    
    def _get_point_value(self, point):
        """获取点的实际数值"""
        if isinstance(point[0], ValueTracker):
            return (point[0].get_value(), point[1].get_value())
        return point
    
    def _get_angle_value(self):
        """获取角度的实际数值"""
        if isinstance(self.angle, ValueTracker):
            return self.angle.get_value()
        return self.angle
    
    def get_function(self):
        """返回函数句柄"""
        def func(x):
            x0, y0 = self._get_point_value(self.point)
            angle = self._get_angle_value()
            
            # 垂直线的情况
            if abs(angle - math.pi/2) < 1e-10 or abs(angle + math.pi/2) < 1e-10:
                return float('inf') if x == x0 else float('nan')
            
            slope = math.tan(angle)
            return y0 + slope * (x - x0)
        
        return func
    
    def get_slope(self):
        """获取当前斜率"""
        angle = self._get_angle_value()
        
        # 垂直线的情况
        if abs(angle - math.pi/2) < 1e-10 or abs(angle + math.pi/2) < 1e-10:
            return float('inf')
        
        return math.tan(angle)
    
    def get_range(self, y_min, y_max):
        """根据y范围返回对应的x范围"""
        x0, y0 = self._get_point_value(self.point)
        angle = self._get_angle_value()
        
        # 垂直线的情况
        if abs(angle - math.pi/2) < 1e-10 or abs(angle + math.pi/2) < 1e-10:
            return (x0, x0)
        
        slope = math.tan(angle)
        
        # 根据 y = y0 + slope * (x - x0) 求解 x
        x_at_y_min = x0 + (y_min - y0) / slope
        x_at_y_max = x0 + (y_max - y0) / slope
        
        return (min(x_at_y_min, x_at_y_max), max(x_at_y_min, x_at_y_max))
    
    def plot_in(self, axes, x_range, y_range=None, color=WHITE, stroke_width=2, stroke_opacity=1):
        """
        在指定的坐标轴中绘制函数图像
        
        Args:
            axes: Manim的Axes对象
            x_range: x值范围，(x_min, x_max)
            y_range: y值范围限制，(y_min, y_max)，可选
            color: 线条颜色，可以是ValueTracker或颜色值
            stroke_width: 线条宽度，可以是ValueTracker或数值
            stroke_opacity: 线条透明度，可以是ValueTracker或数值
            
        Returns:
            VMobject: 函数图像对象
        """
        def _get_param_value(param):
            """获取参数的实际值"""
            if isinstance(param, ValueTracker):
                return param.get_value()
            return param
        
        def create_graph():
            func = self.get_function()
            x_min, x_max = x_range
            
            # 如果有y_range限制，需要调整x_range
            if y_range is not None:
                y_min, y_max = y_range
                try:
                    # 计算在y_range限制下的实际x范围
                    func_x_range = self.get_range(y_min, y_max)
                    if not (math.isnan(func_x_range[0]) or math.isnan(func_x_range[1])):
                        x_min = max(x_min, func_x_range[0])
                        x_max = min(x_max, func_x_range[1])
                except:
                    pass
            
            # 创建受限制的函数
            def limited_func(x):
                y = func(x)
                if y_range is not None:
                    y_min, y_max = y_range
                    if y < y_min or y > y_max:
                        return float('nan')
                return y
            
            try:
                graph = axes.plot(limited_func, x_range=[x_min, x_max], discontinuities=[], 
                                color=_get_param_value(color),
                                stroke_width=_get_param_value(stroke_width),
                                stroke_opacity=_get_param_value(stroke_opacity))
                return graph
            except:
                # 如果绘制失败，返回空的VMobject
                return VMobject()
        
        return create_graph()


class LinearFunctionGeneral:
    """一般式直线：Ax + By + C = 0 形式的直线"""
    
    def __init__(self, A, B, C):
        """
        初始化一般式直线
        
        Args:
            A, B, C: 一般式系数，可以是ValueTracker或数值
                    满足 Ax + By + C = 0
        """
        self.A = A
        self.B = B
        self.C = C
    
    def _get_coefficient_value(self, coeff):
        """获取系数的实际数值"""
        if isinstance(coeff, ValueTracker):
            return coeff.get_value()
        return coeff
    
    def get_function(self):
        """返回函数句柄"""
        def func(x):
            A = self._get_coefficient_value(self.A)
            B = self._get_coefficient_value(self.B)
            C = self._get_coefficient_value(self.C)
            
            if abs(B) < 1e-10:  # 垂直线
                return float('inf') if abs(A * x + C) < 1e-10 else float('nan')
            
            # 从 Ax + By + C = 0 解出 y = -(Ax + C) / B
            return -(A * x + C) / B
        
        return func
    
    def get_slope(self):
        """获取当前斜率"""
        A = self._get_coefficient_value(self.A)
        B = self._get_coefficient_value(self.B)
        
        if abs(B) < 1e-10:
            return float('inf')
        
        return -A / B
    
    def get_range(self, y_min, y_max):
        """根据y范围返回对应的x范围"""
        A = self._get_coefficient_value(self.A)
        B = self._get_coefficient_value(self.B)
        C = self._get_coefficient_value(self.C)
        
        if abs(B) < 1e-10:  # 垂直线
            if abs(A) < 1e-10:
                return (float('-inf'), float('inf'))
            x_val = -C / A
            return (x_val, x_val)
        
        # 从 y = -(Ax + C) / B 解出 x = -(By + C) / A
        if abs(A) < 1e-10:  # 水平线
            return (float('-inf'), float('inf'))
        
        x_at_y_min = -(B * y_min + C) / A
        x_at_y_max = -(B * y_max + C) / A
        
        return (min(x_at_y_min, x_at_y_max), max(x_at_y_min, x_at_y_max))
    
    def plot_in(self, axes, x_range, y_range=None, color=WHITE, stroke_width=2, stroke_opacity=1):
        """
        在指定的坐标轴中绘制函数图像
        
        Args:
            axes: Manim的Axes对象
            x_range: x值范围，(x_min, x_max)
            y_range: y值范围限制，(y_min, y_max)，可选
            color: 线条颜色，可以是ValueTracker或颜色值
            stroke_width: 线条宽度，可以是ValueTracker或数值
            stroke_opacity: 线条透明度，可以是ValueTracker或数值
            
        Returns:
            VMobject: 函数图像对象
        """
        def _get_param_value(param):
            """获取参数的实际值"""
            if isinstance(param, ValueTracker):
                return param.get_value()
            return param
        
        def create_graph():
            func = self.get_function()
            x_min, x_max = x_range
            
            # 如果有y_range限制，需要调整x_range
            if y_range is not None:
                y_min, y_max = y_range
                try:
                    # 计算在y_range限制下的实际x范围
                    func_x_range = self.get_range(y_min, y_max)
                    if not (math.isnan(func_x_range[0]) or math.isnan(func_x_range[1])):
                        x_min = max(x_min, func_x_range[0])
                        x_max = min(x_max, func_x_range[1])
                except:
                    pass
            
            # 创建受限制的函数
            def limited_func(x):
                y = func(x)
                if y_range is not None:
                    y_min, y_max = y_range
                    if y < y_min or y > y_max:
                        return float('nan')
                return y
            
            try:
                graph = axes.plot(limited_func, x_range=[x_min, x_max], discontinuities=[], 
                                color=_get_param_value(color),
                                stroke_width=_get_param_value(stroke_width),
                                stroke_opacity=_get_param_value(stroke_opacity))
                return graph
            except:
                # 如果绘制失败，返回空的VMobject
                return VMobject()
        
        return create_graph()


class ExponentialFunction:
    """指数函数：y = a^x 形式"""
    
    def __init__(self, base):
        """
        初始化指数函数
        
        Args:
            base: 底数，可以是ValueTracker或数值
        """
        self.base = base
    
    def _get_base_value(self):
        """获取底数的实际数值"""
        if isinstance(self.base, ValueTracker):
            return self.base.get_value()
        return self.base
    
    def get_function(self):
        """返回函数句柄"""
        def func(x):
            base = self._get_base_value()
            if base <= 0:
                return float('nan')
            return base ** x
        
        return func
    
    def get_range(self, y_min, y_max):
        """根据y范围返回对应的x范围"""
        base = self._get_base_value()
        
        if base <= 0 or base == 1:
            return (float('-inf'), float('inf'))
        
        if y_min <= 0:
            y_min = 1e-10  # 指数函数y值必须为正
        
        if base > 1:
            x_at_y_min = math.log(y_min) / math.log(base)
            x_at_y_max = math.log(y_max) / math.log(base)
        else:  # 0 < base < 1
            x_at_y_min = math.log(y_max) / math.log(base)
            x_at_y_max = math.log(y_min) / math.log(base)
        
        return (min(x_at_y_min, x_at_y_max), max(x_at_y_min, x_at_y_max))
    
    def plot_in(self, axes, x_range, y_range=None, color=WHITE, stroke_width=2, stroke_opacity=1):
        """
        在指定的坐标轴中绘制函数图像
        
        Args:
            axes: Manim的Axes对象
            x_range: x值范围，(x_min, x_max)
            y_range: y值范围限制，(y_min, y_max)，可选
            color: 线条颜色，可以是ValueTracker或颜色值
            stroke_width: 线条宽度，可以是ValueTracker或数值
            stroke_opacity: 线条透明度，可以是ValueTracker或数值
            
        Returns:
            VMobject: 函数图像对象
        """
        def _get_param_value(param):
            """获取参数的实际值"""
            if isinstance(param, ValueTracker):
                return param.get_value()
            return param
        
        def create_graph():
            func = self.get_function()
            x_min, x_max = x_range
            
            # 如果有y_range限制，需要调整x_range
            if y_range is not None:
                y_min, y_max = y_range
                if y_min <= 0:
                    y_min = 1e-10  # 指数函数y值必须为正
                try:
                    # 计算在y_range限制下的实际x范围
                    func_x_range = self.get_range(y_min, y_max)
                    if not (math.isnan(func_x_range[0]) or math.isnan(func_x_range[1])):
                        x_min = max(x_min, func_x_range[0])
                        x_max = min(x_max, func_x_range[1])
                except:
                    pass
            
            # 创建受限制的函数
            def limited_func(x):
                y = func(x)
                if y_range is not None:
                    y_min, y_max = y_range
                    if y < y_min or y > y_max:
                        return float('nan')
                return y
            
            try:
                graph = axes.plot(limited_func, x_range=[x_min, x_max], discontinuities=[], 
                                color=_get_param_value(color),
                                stroke_width=_get_param_value(stroke_width),
                                stroke_opacity=_get_param_value(stroke_opacity))
                return graph
            except:
                # 如果绘制失败，返回空的VMobject
                return VMobject()
        
        return create_graph()


class LogarithmicFunction:
    """对数函数：y = log_a(x) 形式"""
    
    def __init__(self, base):
        """
        初始化对数函数
        
        Args:
            base: 底数，可以是ValueTracker或数值
        """
        self.base = base
    
    def _get_base_value(self):
        """获取底数的实际数值"""
        if isinstance(self.base, ValueTracker):
            return self.base.get_value()
        return self.base
    
    def get_function(self):
        """返回函数句柄"""
        def func(x):
            base = self._get_base_value()
            if base <= 0 or base == 1 or x <= 0:
                return float('nan')
            return math.log(x) / math.log(base)
        
        return func
    
    def get_range(self, y_min, y_max):
        """根据y范围返回对应的x范围"""
        base = self._get_base_value()
        
        if base <= 0 or base == 1:
            return (0, float('inf'))
        
        if base > 1:
            x_at_y_min = base ** y_min
            x_at_y_max = base ** y_max
        else:  # 0 < base < 1
            x_at_y_min = base ** y_max
            x_at_y_max = base ** y_min
        
        return (min(x_at_y_min, x_at_y_max), max(x_at_y_min, x_at_y_max))
    
    def plot_in(self, axes, x_range, y_range=None, color=WHITE, stroke_width=2, stroke_opacity=1):
        """
        在指定的坐标轴中绘制函数图像
        
        Args:
            axes: Manim的Axes对象
            x_range: x值范围，(x_min, x_max)
            y_range: y值范围限制，(y_min, y_max)，可选
            color: 线条颜色，可以是ValueTracker或颜色值
            stroke_width: 线条宽度，可以是ValueTracker或数值
            stroke_opacity: 线条透明度，可以是ValueTracker或数值
            
        Returns:
            VMobject: 函数图像对象
        """
        def _get_param_value(param):
            """获取参数的实际值"""
            if isinstance(param, ValueTracker):
                return param.get_value()
            return param
        
        def create_graph():
            func = self.get_function()
            x_min, x_max = x_range
            
            # 对数函数要求x > 0
            x_min = max(x_min, 1e-10)
            if x_max <= 0:
                return VMobject()
            
            # 如果有y_range限制，需要调整x_range
            if y_range is not None:
                y_min, y_max = y_range
                try:
                    # 计算在y_range限制下的实际x范围
                    func_x_range = self.get_range(y_min, y_max)
                    if not (math.isnan(func_x_range[0]) or math.isnan(func_x_range[1])):
                        x_min = max(x_min, func_x_range[0])
                        x_max = min(x_max, func_x_range[1])
                except:
                    pass
            
            # 创建受限制的函数
            def limited_func(x):
                y = func(x)
                if y_range is not None:
                    y_min, y_max = y_range
                    if y < y_min or y > y_max:
                        return float('nan')
                return y
            
            try:
                graph = axes.plot(limited_func, x_range=[x_min, x_max], discontinuities=[], 
                                color=_get_param_value(color),
                                stroke_width=_get_param_value(stroke_width),
                                stroke_opacity=_get_param_value(stroke_opacity))
                return graph
            except:
                # 如果绘制失败，返回空的VMobject
                return VMobject()
        
        return create_graph()


class PowerFunction:
    """幂函数：y = x^n 形式"""
    
    def __init__(self, exponent):
        """
        初始化幂函数
        
        Args:
            exponent: 幂次，可以是ValueTracker或数值
        """
        self.exponent = exponent
    
    def _get_exponent_value(self):
        """获取幂次的实际数值"""
        if isinstance(self.exponent, ValueTracker):
            return self.exponent.get_value()
        return self.exponent
    
    def get_function(self):
        """返回函数句柄"""
        def func(x):
            exp = self._get_exponent_value()
            
            # 处理特殊情况
            if exp == 0:
                return 1
            
            if x == 0:
                if exp > 0:
                    return 0
                else:
                    return float('inf')
            
            if x < 0 and not isinstance(exp, int) and exp != int(exp):
                # 负数的非整数次幂在实数范围内无定义
                return float('nan')
            
            return x ** exp
        
        return func
    
    def get_range(self, y_min, y_max):
        """根据y范围返回对应的x范围"""
        exp = self._get_exponent_value()
        
        if exp == 0:
            # y = 1，常函数
            return (float('-inf'), float('inf')) if y_min <= 1 <= y_max else (float('nan'), float('nan'))
        
        if exp > 0:
            if exp % 2 == 1:  # 奇数次幂
                x_at_y_min = y_min ** (1/exp) if y_min >= 0 else -(abs(y_min) ** (1/exp))
                x_at_y_max = y_max ** (1/exp) if y_max >= 0 else -(abs(y_max) ** (1/exp))
                return (min(x_at_y_min, x_at_y_max), max(x_at_y_min, x_at_y_max))
            else:  # 偶数次幂
                if y_min < 0:
                    return (float('nan'), float('nan'))
                if y_min == 0:
                    x_max = y_max ** (1/exp)
                    return (-x_max, x_max)
                else:
                    x_min = y_min ** (1/exp)
                    x_max = y_max ** (1/exp)
                    return (-x_max, -x_min) if y_max < y_min else (-x_max, x_max)
        else:  # exp < 0
            # 反比例函数类型
            if y_min * y_max <= 0:
                return (float('-inf'), float('inf'))
            
            x_at_y_min = y_min ** (1/exp)
            x_at_y_max = y_max ** (1/exp)
            return (min(x_at_y_min, x_at_y_max), max(x_at_y_min, x_at_y_max))
    
    def plot_in(self, axes, x_range, y_range=None, color=WHITE, stroke_width=2, stroke_opacity=1):
        """
        在指定的坐标轴中绘制函数图像
        
        Args:
            axes: Manim的Axes对象
            x_range: x值范围，(x_min, x_max)
            y_range: y值范围限制，(y_min, y_max)，可选
            color: 线条颜色，可以是ValueTracker或颜色值
            stroke_width: 线条宽度，可以是ValueTracker或数值
            stroke_opacity: 线条透明度，可以是ValueTracker或数值
            
        Returns:
            VMobject: 函数图像对象
        """
        def _get_param_value(param):
            """获取参数的实际值"""
            if isinstance(param, ValueTracker):
                return param.get_value()
            return param
        
        def create_graph():
            func = self.get_function()
            x_min, x_max = x_range
            
            # 幂函数的特殊处理
            exp = self._get_exponent_value()
            
            # 如果有y_range限制，需要调整x_range
            if y_range is not None:
                y_min, y_max = y_range
                try:
                    # 计算在y_range限制下的实际x范围
                    func_x_range = self.get_range(y_min, y_max)
                    if not (math.isnan(func_x_range[0]) or math.isnan(func_x_range[1])):
                        x_min = max(x_min, func_x_range[0])
                        x_max = min(x_max, func_x_range[1])
                except:
                    pass
            
            # 对于负指数的幂函数，需要避免x=0
            if exp < 0:
                if x_min <= 0 <= x_max:
                    # 分段绘制，避开x=0
                    graphs = []
                    if x_min < 0:
                        # 绘制负半轴
                        def limited_func_neg(x):
                            y = func(x)
                            if y_range is not None:
                                y_min, y_max = y_range
                                if y < y_min or y > y_max:
                                    return float('nan')
                            return y
                        
                        try:
                            graph_neg = axes.plot(limited_func_neg, x_range=[x_min, -1e-10], 
                                                discontinuities=[], 
                                                color=_get_param_value(color),
                                                stroke_width=_get_param_value(stroke_width),
                                                stroke_opacity=_get_param_value(stroke_opacity))
                            graphs.append(graph_neg)
                        except:
                            pass
                    
                    if x_max > 0:
                        # 绘制正半轴
                        def limited_func_pos(x):
                            y = func(x)
                            if y_range is not None:
                                y_min, y_max = y_range
                                if y < y_min or y > y_max:
                                    return float('nan')
                            return y
                        
                        try:
                            graph_pos = axes.plot(limited_func_pos, x_range=[1e-10, x_max], 
                                                discontinuities=[], 
                                                color=_get_param_value(color),
                                                stroke_width=_get_param_value(stroke_width),
                                                stroke_opacity=_get_param_value(stroke_opacity))
                            graphs.append(graph_pos)
                        except:
                            pass
                    
                    if graphs:
                        # 合并多个图形
                        combined = graphs[0]
                        for g in graphs[1:]:
                            combined = combined + g
                        return combined
                    else:
                        return VMobject()
            
            # 创建受限制的函数
            def limited_func(x):
                y = func(x)
                if y_range is not None:
                    y_min, y_max = y_range
                    if y < y_min or y > y_max:
                        return float('nan')
                return y
            
            # 对于非整数指数且x可能为负的情况，需要特殊处理
            if exp != int(exp) and x_min < 0:
                x_min = max(x_min, 0)
            
            try:
                graph = axes.plot(limited_func, x_range=[x_min, x_max], discontinuities=[], 
                                color=_get_param_value(color),
                                stroke_width=_get_param_value(stroke_width),
                                stroke_opacity=_get_param_value(stroke_opacity))
                return graph
            except:
                # 如果绘制失败，返回空的VMobject
                return VMobject()
        
        return create_graph()


class Ellipse:
    """椭圆：中心在原点的标准椭圆 x²/a² + y²/b² = 1"""
    
    def __init__(self, a, b):
        """
        初始化椭圆
        
        Args:
            a: 长半轴（x方向），可以是ValueTracker或数值
            b: 短半轴（y方向），可以是ValueTracker或数值
        """
        self.a = a
        self.b = b
    
    def _get_param_value(self, param):
        """获取参数的实际数值"""
        if isinstance(param, ValueTracker):
            return param.get_value()
        return param
    
    def get_parametric_function(self):
        """返回参数方程 (x(t), y(t))"""
        def parametric_func(t):
            a = self._get_param_value(self.a)
            b = self._get_param_value(self.b)
            x = a * math.cos(t)
            y = b * math.sin(t)
            return (x, y)
        
        return parametric_func
    
    def get_eccentricity(self):
        """获取离心率"""
        a = self._get_param_value(self.a)
        b = self._get_param_value(self.b)
        
        if a == 0 or b == 0:
            return 1  # 退化情况
        
        # 确保a是长半轴
        if a >= b:
            c = math.sqrt(a * a - b * b)
            return c / a
        else:
            c = math.sqrt(b * b - a * a)
            return c / b
    
    def get_foci_coordinates(self):
        """获取焦点坐标"""
        a = self._get_param_value(self.a)
        b = self._get_param_value(self.b)
        
        if a == 0 or b == 0:
            return [(0, 0), (0, 0)]
        
        if a >= b:
            # 长轴在x方向
            c = math.sqrt(a * a - b * b)
            return [(-c, 0), (c, 0)]
        else:
            # 长轴在y方向
            c = math.sqrt(b * b - a * a)
            return [(0, -c), (0, c)]
    
    def get_foci_dots(self, axes, color=WHITE, radius=0.05):
        """获取焦点的Dot对象"""
        foci = self.get_foci_coordinates()
        dots = []
        for focus in foci:
            dot = Dot(axes.coords_to_point(focus[0], focus[1]), 
                     color=color, radius=radius)
            dots.append(dot)
        return dots
    
    def get_directrix_equations(self):
        """获取准线方程"""
        a = self._get_param_value(self.a)
        b = self._get_param_value(self.b)
        
        if a == 0 or b == 0:
            return []
        
        if a >= b:
            # 长轴在x方向，准线垂直于x轴
            c = math.sqrt(a * a - b * b)
            if c == 0:
                return []
            d = a * a / c  # 准线到中心的距离
            return [f"x = {-d}", f"x = {d}"]
        else:
            # 长轴在y方向，准线垂直于y轴
            c = math.sqrt(b * b - a * a)
            if c == 0:
                return []
            d = b * b / c
            return [f"y = {-d}", f"y = {d}"]
    
    def get_directrix_lines(self, axes, color=WHITE, stroke_width=1):
        """获取准线的Line对象"""
        a = self._get_param_value(self.a)
        b = self._get_param_value(self.b)
        
        if a == 0 or b == 0:
            return []
        
        lines = []
        x_range = axes.x_range
        y_range = axes.y_range
        
        if a >= b:
            # 长轴在x方向，准线垂直于x轴
            c = math.sqrt(a * a - b * b)
            if c == 0:
                return []
            d = a * a / c
            
            # 左准线
            line1 = DashedLine(
                axes.coords_to_point(-d, y_range[0]),
                axes.coords_to_point(-d, y_range[1]),
                color=color, stroke_width=stroke_width
            )
            # 右准线
            line2 = DashedLine(
                axes.coords_to_point(d, y_range[0]),
                axes.coords_to_point(d, y_range[1]),
                color=color, stroke_width=stroke_width
            )
            lines = [line1, line2]
        else:
            # 长轴在y方向，准线垂直于y轴
            c = math.sqrt(b * b - a * a)
            if c == 0:
                return []
            d = b * b / c
            
            # 下准线
            line1 = DashedLine(
                axes.coords_to_point(x_range[0], -d),
                axes.coords_to_point(x_range[1], -d),
                color=color, stroke_width=stroke_width
            )
            # 上准线
            line2 = DashedLine(
                axes.coords_to_point(x_range[0], d),
                axes.coords_to_point(x_range[1], d),
                color=color, stroke_width=stroke_width
            )
            lines = [line1, line2]
        
        return lines
    
    def plot_in(self, axes, color=WHITE, stroke_width=2, stroke_opacity=1):
        """
        在指定的坐标轴中绘制椭圆
        
        Args:
            axes: Manim的Axes对象
            color: 线条颜色，可以是ValueTracker或颜色值
            stroke_width: 线条宽度，可以是ValueTracker或数值
            stroke_opacity: 线条透明度，可以是ValueTracker或数值
            
        Returns:
            VMobject: 椭圆图像对象
        """
        def _get_param_value(param):
            """获取参数的实际值"""
            if isinstance(param, ValueTracker):
                return param.get_value()
            return param
        
        def create_curve():
            parametric_func = self.get_parametric_function()
            
            try:
                curve = ParametricFunction(
                    lambda t: axes.coords_to_point(*parametric_func(t)),
                    t_range=[0, 2 * math.pi],
                    color=_get_param_value(color),
                    stroke_width=_get_param_value(stroke_width),
                    stroke_opacity=_get_param_value(stroke_opacity)
                )
                return curve
            except:
                return VMobject()
        
        return create_curve()


class Parabola:
    """抛物线：中心在原点的标准抛物线"""
    
    def __init__(self, p, orientation='right'):
        """
        初始化抛物线
        
        Args:
            p: 焦点参数，可以是ValueTracker或数值
            orientation: 开口方向 'right', 'left', 'up', 'down'
        """
        self.p = p
        self.orientation = orientation
    
    def _get_param_value(self, param):
        """获取参数的实际数值"""
        if isinstance(param, ValueTracker):
            return param.get_value()
        return param
    
    def get_parametric_function(self):
        """返回参数方程 (x(t), y(t))"""
        def parametric_func(t):
            p = self._get_param_value(self.p)
            
            if self.orientation == 'right':
                # x = t²/(4p), y = t
                x = t * t / (4 * p) if p != 0 else 0
                y = t
            elif self.orientation == 'left':
                # x = -t²/(4p), y = t
                x = -t * t / (4 * p) if p != 0 else 0
                y = t
            elif self.orientation == 'up':
                # x = t, y = t²/(4p)
                x = t
                y = t * t / (4 * p) if p != 0 else 0
            else:  # 'down'
                # x = t, y = -t²/(4p)
                x = t
                y = -t * t / (4 * p) if p != 0 else 0
            
            return (x, y)
        
        return parametric_func
    
    def get_eccentricity(self):
        """获取离心率（抛物线的离心率恒为1）"""
        return 1
    
    def get_focus_coordinate(self):
        """获取焦点坐标"""
        p = self._get_param_value(self.p)
        
        if self.orientation == 'right':
            return (p, 0)
        elif self.orientation == 'left':
            return (-p, 0)
        elif self.orientation == 'up':
            return (0, p)
        else:  # 'down'
            return (0, -p)
    
    def get_focus_dot(self, axes, color=WHITE, radius=0.05):
        """获取焦点的Dot对象"""
        focus = self.get_focus_coordinate()
        dot = Dot(axes.coords_to_point(focus[0], focus[1]), 
                 color=color, radius=radius)
        return dot
    
    def get_directrix_equation(self):
        """获取准线方程"""
        p = self._get_param_value(self.p)
        
        if self.orientation == 'right':
            return f"x = {-p}"
        elif self.orientation == 'left':
            return f"x = {p}"
        elif self.orientation == 'up':
            return f"y = {-p}"
        else:  # 'down'
            return f"y = {p}"
    
    def get_directrix_line(self, axes, color=WHITE, stroke_width=1):
        """获取准线的Line对象"""
        p = self._get_param_value(self.p)
        x_range = axes.x_range
        y_range = axes.y_range
        
        if self.orientation == 'right':
            # 垂直线 x = -p
            line = DashedLine(
                axes.coords_to_point(-p, y_range[0]),
                axes.coords_to_point(-p, y_range[1]),
                color=color, stroke_width=stroke_width
            )
        elif self.orientation == 'left':
            # 垂直线 x = p
            line = DashedLine(
                axes.coords_to_point(p, y_range[0]),
                axes.coords_to_point(p, y_range[1]),
                color=color, stroke_width=stroke_width
            )
        elif self.orientation == 'up':
            # 水平线 y = -p
            line = DashedLine(
                axes.coords_to_point(x_range[0], -p),
                axes.coords_to_point(x_range[1], -p),
                color=color, stroke_width=stroke_width
            )
        else:  # 'down'
            # 水平线 y = p
            line = DashedLine(
                axes.coords_to_point(x_range[0], p),
                axes.coords_to_point(x_range[1], p),
                color=color, stroke_width=stroke_width
            )
        
        return line
    
    def plot_in(self, axes, t_range=(-5, 5), color=WHITE, stroke_width=2, stroke_opacity=1):
        """
        在指定的坐标轴中绘制抛物线
        
        Args:
            axes: Manim的Axes对象
            t_range: 参数t的范围，(t_min, t_max)
            color: 线条颜色，可以是ValueTracker或颜色值
            stroke_width: 线条宽度，可以是ValueTracker或数值
            stroke_opacity: 线条透明度，可以是ValueTracker或数值
            
        Returns:
            VMobject: 抛物线图像对象
        """
        def _get_param_value(param):
            """获取参数的实际值"""
            if isinstance(param, ValueTracker):
                return param.get_value()
            return param
        
        def create_curve():
            parametric_func = self.get_parametric_function()
            
            try:
                curve = ParametricFunction(
                    lambda t: axes.coords_to_point(*parametric_func(t)),
                    t_range=t_range,
                    color=_get_param_value(color),
                    stroke_width=_get_param_value(stroke_width),
                    stroke_opacity=_get_param_value(stroke_opacity)
                )
                return curve
            except:
                return VMobject()
        
        return create_curve()


class Hyperbola:
    """双曲线：中心在原点的标准双曲线"""
    
    def __init__(self, a, b, orientation='horizontal'):
        """
        初始化双曲线
        
        Args:
            a: 实半轴，可以是ValueTracker或数值
            b: 虚半轴，可以是ValueTracker或数值
            orientation: 方向 'horizontal' (x²/a² - y²/b² = 1) 或 'vertical' (y²/a² - x²/b² = 1)
        """
        self.a = a
        self.b = b
        self.orientation = orientation
    
    def _get_param_value(self, param):
        """获取参数的实际数值"""
        if isinstance(param, ValueTracker):
            return param.get_value()
        return param
    
    def get_parametric_function(self):
        """返回参数方程 (x(t), y(t))"""
        def parametric_func(t):
            a = self._get_param_value(self.a)
            b = self._get_param_value(self.b)
            
            if self.orientation == 'horizontal':
                # x²/a² - y²/b² = 1
                # x = ±a*cosh(t), y = b*sinh(t)
                x = a * math.cosh(t)
                y = b * math.sinh(t)
            else:  # 'vertical'
                # y²/a² - x²/b² = 1
                # x = b*sinh(t), y = ±a*cosh(t)
                x = b * math.sinh(t)
                y = a * math.cosh(t)
            
            return (x, y)
        
        return parametric_func
    
    def get_eccentricity(self):
        """获取离心率"""
        a = self._get_param_value(self.a)
        b = self._get_param_value(self.b)
        
        if a == 0:
            return float('inf')
        
        c = math.sqrt(a * a + b * b)
        return c / a
    
    def get_foci_coordinates(self):
        """获取焦点坐标"""
        a = self._get_param_value(self.a)
        b = self._get_param_value(self.b)
        
        c = math.sqrt(a * a + b * b)
        
        if self.orientation == 'horizontal':
            return [(-c, 0), (c, 0)]
        else:  # 'vertical'
            return [(0, -c), (0, c)]
    
    def get_foci_dots(self, axes, color=WHITE, radius=0.05):
        """获取焦点的Dot对象"""
        foci = self.get_foci_coordinates()
        dots = []
        for focus in foci:
            dot = Dot(axes.coords_to_point(focus[0], focus[1]), 
                     color=color, radius=radius)
            dots.append(dot)
        return dots
    
    def get_directrix_equations(self):
        """获取准线方程"""
        a = self._get_param_value(self.a)
        b = self._get_param_value(self.b)
        
        if a == 0:
            return []
        
        c = math.sqrt(a * a + b * b)
        d = a * a / c  # 准线到中心的距离
        
        if self.orientation == 'horizontal':
            return [f"x = {-d}", f"x = {d}"]
        else:  # 'vertical'
            return [f"y = {-d}", f"y = {d}"]
    
    def get_directrix_lines(self, axes, color=WHITE, stroke_width=1):
        """获取准线的Line对象"""
        a = self._get_param_value(self.a)
        b = self._get_param_value(self.b)
        
        if a == 0:
            return []
        
        c = math.sqrt(a * a + b * b)
        d = a * a / c
        x_range = axes.x_range
        y_range = axes.y_range
        lines = []
        
        if self.orientation == 'horizontal':
            # 垂直准线
            line1 = DashedLine(
                axes.coords_to_point(-d, y_range[0]),
                axes.coords_to_point(-d, y_range[1]),
                color=color, stroke_width=stroke_width
            )
            line2 = DashedLine(
                axes.coords_to_point(d, y_range[0]),
                axes.coords_to_point(d, y_range[1]),
                color=color, stroke_width=stroke_width
            )
            lines = [line1, line2]
        else:  # 'vertical'
            # 水平准线
            line1 = DashedLine(
                axes.coords_to_point(x_range[0], -d),
                axes.coords_to_point(x_range[1], -d),
                color=color, stroke_width=stroke_width
            )
            line2 = DashedLine(
                axes.coords_to_point(x_range[0], d),
                axes.coords_to_point(x_range[1], d),
                color=color, stroke_width=stroke_width
            )
            lines = [line1, line2]
        
        return lines
    
    def get_asymptote_equations(self):
        """获取渐近线方程"""
        a = self._get_param_value(self.a)
        b = self._get_param_value(self.b)
        
        if a == 0:
            return []
        
        if self.orientation == 'horizontal':
            # y = ±(b/a)x
            slope = b / a
            return [f"y = {slope}x", f"y = {-slope}x"]
        else:  # 'vertical'
            # y = ±(a/b)x
            if b == 0:
                return ["x = 0"]  # 垂直渐近线
            slope = a / b
            return [f"y = {slope}x", f"y = {-slope}x"]
    
    def get_asymptote_lines(self, axes, color=WHITE, stroke_width=1):
        """获取渐近线的Line对象"""
        a = self._get_param_value(self.a)
        b = self._get_param_value(self.b)
        
        if a == 0:
            return []
        
        x_range = axes.x_range
        y_range = axes.y_range
        lines = []
        
        if self.orientation == 'horizontal':
            # y = ±(b/a)x
            slope = b / a
            
            # 计算直线在坐标轴范围内的端点
            x_min, x_max = x_range[0], x_range[1]
            y_min, y_max = y_range[0], y_range[1]
            
            # 正斜率渐近线
            y1_at_xmin = slope * x_min
            y1_at_xmax = slope * x_max
            x1_at_ymin = y_min / slope if slope != 0 else x_min
            x1_at_ymax = y_max / slope if slope != 0 else x_max
            
            # 找到在坐标轴范围内的端点
            if y_min <= y1_at_xmin <= y_max and y_min <= y1_at_xmax <= y_max:
                line1 = DashedLine(
                    axes.coords_to_point(x_min, y1_at_xmin),
                    axes.coords_to_point(x_max, y1_at_xmax),
                    color=color, stroke_width=stroke_width
                )
            else:
                # 使用y范围限制
                start_x = max(x_min, min(x_max, x1_at_ymin))
                end_x = max(x_min, min(x_max, x1_at_ymax))
                line1 = DashedLine(
                    axes.coords_to_point(start_x, y_min),
                    axes.coords_to_point(end_x, y_max),
                    color=color, stroke_width=stroke_width
                )
            
            # 负斜率渐近线
            y2_at_xmin = -slope * x_min
            y2_at_xmax = -slope * x_max
            x2_at_ymin = -y_min / slope if slope != 0 else x_min
            x2_at_ymax = -y_max / slope if slope != 0 else x_max
            
            if y_min <= y2_at_xmin <= y_max and y_min <= y2_at_xmax <= y_max:
                line2 = DashedLine(
                    axes.coords_to_point(x_min, y2_at_xmin),
                    axes.coords_to_point(x_max, y2_at_xmax),
                    color=color, stroke_width=stroke_width
                )
            else:
                start_x = max(x_min, min(x_max, x2_at_ymax))
                end_x = max(x_min, min(x_max, x2_at_ymin))
                line2 = DashedLine(
                    axes.coords_to_point(start_x, y_max),
                    axes.coords_to_point(end_x, y_min),
                    color=color, stroke_width=stroke_width
                )
            
            lines = [line1, line2]
            
        else:  # 'vertical'
            if b == 0:
                # 垂直渐近线 x = 0
                line = DashedLine(
                    axes.coords_to_point(0, y_range[0]),
                    axes.coords_to_point(0, y_range[1]),
                    color=color, stroke_width=stroke_width
                )
                lines = [line]
            else:
                # y = ±(a/b)x
                slope = a / b
                
                x_min, x_max = x_range[0], x_range[1]
                y_min, y_max = y_range[0], y_range[1]
                
                # 正斜率渐近线
                line1 = DashedLine(
                    axes.coords_to_point(x_min, slope * x_min),
                    axes.coords_to_point(x_max, slope * x_max),
                    color=color, stroke_width=stroke_width
                )
                
                # 负斜率渐近线
                line2 = DashedLine(
                    axes.coords_to_point(x_min, -slope * x_min),
                    axes.coords_to_point(x_max, -slope * x_max),
                    color=color, stroke_width=stroke_width
                )
                
                lines = [line1, line2]
        
        return lines
    
    def plot_in(self, axes, t_range=(-3, 3), color=WHITE, stroke_width=2, stroke_opacity=1):
        """
        在指定的坐标轴中绘制双曲线
        
        Args:
            axes: Manim的Axes对象
            t_range: 参数t的范围，(t_min, t_max)
            color: 线条颜色，可以是ValueTracker或颜色值
            stroke_width: 线条宽度，可以是ValueTracker或数值
            stroke_opacity: 线条透明度，可以是ValueTracker或数值
            
        Returns:
            VMobject: 双曲线图像对象（包含两支）
        """
        def _get_param_value(param):
            """获取参数的实际值"""
            if isinstance(param, ValueTracker):
                return param.get_value()
            return param
        
        def create_curve():
            parametric_func = self.get_parametric_function()
            
            try:
                # 绘制双曲线的两支
                if self.orientation == 'horizontal':
                    # 右支：x = a*cosh(t), y = b*sinh(t)
                    curve_right = ParametricFunction(
                        lambda t: axes.coords_to_point(*parametric_func(t)),
                        t_range=t_range,
                        color=_get_param_value(color),
                        stroke_width=_get_param_value(stroke_width),
                        stroke_opacity=_get_param_value(stroke_opacity)
                    )
                    
                    # 左支：x = -a*cosh(t), y = b*sinh(t)
                    def left_branch_func(t):
                        x, y = parametric_func(t)
                        return (-x, y)
                    
                    curve_left = ParametricFunction(
                        lambda t: axes.coords_to_point(*left_branch_func(t)),
                        t_range=t_range,
                        color=_get_param_value(color),
                        stroke_width=_get_param_value(stroke_width),
                        stroke_opacity=_get_param_value(stroke_opacity)
                    )
                    
                else:  # 'vertical'
                    # 上支：x = b*sinh(t), y = a*cosh(t)
                    curve_upper = ParametricFunction(
                        lambda t: axes.coords_to_point(*parametric_func(t)),
                        t_range=t_range,
                        color=_get_param_value(color),
                        stroke_width=_get_param_value(stroke_width),
                        stroke_opacity=_get_param_value(stroke_opacity)
                    )
                    
                    # 下支：x = b*sinh(t), y = -a*cosh(t)
                    def lower_branch_func(t):
                        x, y = parametric_func(t)
                        return (x, -y)
                    
                    curve_lower = ParametricFunction(
                        lambda t: axes.coords_to_point(*lower_branch_func(t)),
                        t_range=t_range,
                        color=_get_param_value(color),
                        stroke_width=_get_param_value(stroke_width),
                        stroke_opacity=_get_param_value(stroke_opacity)
                    )
                    
                    return curve_upper + curve_lower
                
                return curve_right + curve_left
                
            except:
                return VMobject()
        
        return create_curve()


class CustomCircle:
    """圆：圆心在任意位置的圆 (x-h)² + (y-k)² = r²"""
    
    def __init__(self, center, radius):
        """
        初始化圆
        
        Args:
            center: 圆心坐标，可以是(h, k)元组或包含ValueTracker的列表
            radius: 半径，可以是ValueTracker或数值
        """
        self.center = center
        self.radius = radius
    
    def _get_param_value(self, param):
        """获取参数的实际数值"""
        if isinstance(param, ValueTracker):
            return param.get_value()
        return param
    
    def _get_center_value(self):
        """获取圆心的实际坐标"""
        if isinstance(self.center[0], ValueTracker):
            return (self.center[0].get_value(), self.center[1].get_value())
        return self.center
    
    def get_parametric_function(self):
        """返回参数方程 (x(t), y(t))"""
        def parametric_func(t):
            h, k = self._get_center_value()
            r = self._get_param_value(self.radius)
            x = h + r * math.cos(t)
            y = k + r * math.sin(t)
            return (x, y)
        
        return parametric_func
    
    def get_center_coordinate(self):
        """获取圆心坐标"""
        return self._get_center_value()
    
    def get_radius_value(self):
        """获取半径值"""
        return self._get_param_value(self.radius)
    
    def get_diameter(self):
        """获取直径"""
        return 2 * self._get_param_value(self.radius)
    
    def get_circumference(self):
        """获取周长"""
        r = self._get_param_value(self.radius)
        return 2 * math.pi * r
    
    def get_area(self):
        """获取面积"""
        r = self._get_param_value(self.radius)
        return math.pi * r * r
    
    def get_center_dot(self, axes, color=WHITE, radius=0.05):
        """获取圆心的Dot对象"""
        h, k = self._get_center_value()
        dot = Dot(axes.coords_to_point(h, k), 
                 color=color, radius=radius)
        return dot
    
    def get_diameter_line(self, axes, angle=0, color=WHITE, stroke_width=1):
        """
        获取指定角度的直径线段
        
        Args:
            axes: Manim的Axes对象
            angle: 直径的角度（弧度），默认为0（水平）
            color: 线条颜色
            stroke_width: 线条宽度
            
        Returns:
            Line: 直径线段对象
        """
        h, k = self._get_center_value()
        r = self._get_param_value(self.radius)
        
        # 计算直径两端点
        x1 = h + r * math.cos(angle)
        y1 = k + r * math.sin(angle)
        x2 = h - r * math.cos(angle)
        y2 = k - r * math.sin(angle)
        
        line = Line(
            axes.coords_to_point(x1, y1),
            axes.coords_to_point(x2, y2),
            color=color, stroke_width=stroke_width
        )
        return line
    
    def get_radius_line(self, axes, angle=0, color=WHITE, stroke_width=1):
        """
        获取指定角度的半径线段
        
        Args:
            axes: Manim的Axes对象
            angle: 半径的角度（弧度），默认为0（向右）
            color: 线条颜色
            stroke_width: 线条宽度
            
        Returns:
            Line: 半径线段对象
        """
        h, k = self._get_center_value()
        r = self._get_param_value(self.radius)
        
        # 计算半径端点
        x = h + r * math.cos(angle)
        y = k + r * math.sin(angle)
        
        line = Line(
            axes.coords_to_point(h, k),
            axes.coords_to_point(x, y),
            color=color, stroke_width=stroke_width
        )
        return line
    
    def get_tangent_line_at_angle(self, axes, angle, length_factor=2, color=WHITE, stroke_width=1):
        """
        获取在指定角度处的切线
        
        Args:
            axes: Manim的Axes对象
            angle: 切点角度（弧度）
            length_factor: 切线长度系数（相对于半径）
            color: 线条颜色
            stroke_width: 线条宽度
            
        Returns:
            Line: 切线对象
        """
        h, k = self._get_center_value()
        r = self._get_param_value(self.radius)
        
        # 切点坐标
        x0 = h + r * math.cos(angle)
        y0 = k + r * math.sin(angle)
        
        # 切线方向（垂直于半径）
        tangent_angle = angle + math.pi / 2
        length = r * length_factor
        
        # 切线两端点
        x1 = x0 + length * math.cos(tangent_angle) / 2
        y1 = y0 + length * math.sin(tangent_angle) / 2
        x2 = x0 - length * math.cos(tangent_angle) / 2
        y2 = y0 - length * math.sin(tangent_angle) / 2
        
        line = Line(
            axes.coords_to_point(x1, y1),
            axes.coords_to_point(x2, y2),
            color=color, stroke_width=stroke_width
        )
        return line
    
    def is_point_inside(self, point):
        """
        判断点是否在圆内
        
        Args:
            point: 点坐标 (x, y)
            
        Returns:
            bool: True表示在圆内，False表示在圆外
        """
        h, k = self._get_center_value()
        r = self._get_param_value(self.radius)
        x, y = point
        
        distance_squared = (x - h) ** 2 + (y - k) ** 2
        return distance_squared < r ** 2
    
    def is_point_on_circle(self, point, tolerance=1e-6):
        """
        判断点是否在圆上
        
        Args:
            point: 点坐标 (x, y)
            tolerance: 误差容限
            
        Returns:
            bool: True表示在圆上，False表示不在圆上
        """
        h, k = self._get_center_value()
        r = self._get_param_value(self.radius)
        x, y = point
        
        distance_squared = (x - h) ** 2 + (y - k) ** 2
        return abs(distance_squared - r ** 2) < tolerance
    
    def get_distance_from_center(self, point):
        """
        获取点到圆心的距离
        
        Args:
            point: 点坐标 (x, y)
            
        Returns:
            float: 距离值
        """
        h, k = self._get_center_value()
        x, y = point
        return math.sqrt((x - h) ** 2 + (y - k) ** 2)
    
    def plot_in(self, axes, color=WHITE, stroke_width=2, stroke_opacity=1):
        """
        在指定的坐标轴中绘制圆
        
        Args:
            axes: Manim的Axes对象
            color: 线条颜色，可以是ValueTracker或颜色值
            stroke_width: 线条宽度，可以是ValueTracker或数值
            stroke_opacity: 线条透明度，可以是ValueTracker或数值
            
        Returns:
            VMobject: 圆图像对象
        """
        def _get_param_value(param):
            """获取参数的实际值"""
            if isinstance(param, ValueTracker):
                return param.get_value()
            return param
        
        def create_curve():
            parametric_func = self.get_parametric_function()
            
            try:
                curve = ParametricFunction(
                    lambda t: axes.coords_to_point(*parametric_func(t)),
                    t_range=[0, 2 * math.pi],
                    color=_get_param_value(color),
                    stroke_width=_get_param_value(stroke_width),
                    stroke_opacity=_get_param_value(stroke_opacity)
                )
                return curve
            except:
                return VMobject()
        
        return create_curve() 