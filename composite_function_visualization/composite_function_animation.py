from manim import *
import numpy as np
from scipy.optimize import fsolve, minimize_scalar


class CompositeFunctionAnimation(Scene):
    def __init__(self, inner_func, outer_func, x_range=None, y_range=None, x_start=None, x_end=None, title_text=None):
        """
        复合函数动画类
        
        参数:
        inner_func: 内函数 g(x)
        outer_func: 外函数 f(u)
        x_range: x轴范围，默认[-1, 2, 1]
        y_range: y轴范围，默认[-1, 2, 1]
        x_start: 动画起始x值，默认-1
        x_end: 动画结束x值，默认2
        title_text: 标题文本，默认None（不显示标题）
        """
        self.inner_func = inner_func
        self.outer_func = outer_func
        
        # 设置默认值
        self.x_range = x_range if x_range is not None else [-1, 2, 1]
        self.y_range = y_range if y_range is not None else [-1, 2, 1]
        self.x_start = x_start if x_start is not None else -1
        self.x_end = x_end if x_end is not None else 2
        self.title_text = title_text
        
        # 定义复合函数
        self.composite_func = lambda x: self.outer_func(self.inner_func(x))
        
        # 计算内函数的值域
        self.inner_range = self._compute_inner_range()
        
        # 计算反函数（数值方法）
        self.inverse_outer_func = self._compute_inverse_function()
        
        super().__init__()
    
    def _compute_inner_range(self):
        """计算内函数在定义域内的值域"""
        # 在定义域内采样计算内函数的最大最小值
        x_samples = np.linspace(self.x_start, self.x_end, 1000)
        y_samples = [self.inner_func(x) for x in x_samples]
        
        min_val = min(y_samples)
        max_val = max(y_samples)
        
        # 添加一些余量确保完整覆盖
        range_margin = (max_val - min_val) * 0.1
        return [min_val - range_margin, max_val + range_margin]
    
    def _compute_inverse_function(self):
        """计算外函数的反函数（使用数值方法）"""
        def inverse_func(y):
            try:
                # 使用数值方法求解 outer_func(x) = y
                def equation(x):
                    return self.outer_func(x) - y
                
                # 在内函数值域内寻找解
                initial_guess = (self.inner_range[0] + self.inner_range[1]) / 2
                result = fsolve(equation, initial_guess)[0]
                return result
            except:
                return y  # 如果计算失败，返回恒等函数
        
        return inverse_func
    
    def construct(self):
        # 创建标题（如果提供）
        if self.title_text:
            title = MathTex(self.title_text, font_size=36)
            title.to_edge(UP, buff=0.5)
            self.play(Write(title))
        
        # 坐标系参数
        axis_length = 3
        
        # 创建四个坐标系 - 全部白色，无箭头
        # 左上角 - 内函数
        axes_top_left = Axes(
            x_range=self.x_range,
            y_range=self.y_range,
            x_length=axis_length,
            y_length=axis_length,
            axis_config={"color": WHITE, "tip_length": 0.02, "stroke_width": 1, "include_tip": False}
        ).shift(LEFT * 3.5 + UP * 1.5)
        
        # 右上角 - 反函数（xy交换）
        axes_top_right = Axes(
            x_range=self.x_range,
            y_range=self.y_range,
            x_length=axis_length,
            y_length=axis_length,
            axis_config={"color": WHITE, "tip_length": 0.02, "stroke_width": 1, "include_tip": False}
        ).shift(RIGHT * 3.5 + UP * 1.5)
        
        # 左下角 - 复合函数
        axes_bottom_left = Axes(
            x_range=self.x_range,
            y_range=self.y_range,
            x_length=axis_length,
            y_length=axis_length,
            axis_config={"color": WHITE, "tip_length": 0.02, "stroke_width": 1, "include_tip": False}
        ).shift(LEFT * 3.5 + DOWN * 2)
        
        # 右下角 - 外函数
        axes_bottom_right = Axes(
            x_range=self.x_range,
            y_range=self.y_range,
            x_length=axis_length,
            y_length=axis_length,
            axis_config={"color": WHITE, "tip_length": 0.02, "stroke_width": 1, "include_tip": False}
        ).shift(RIGHT * 3.5 + DOWN * 2)
        
        # 添加坐标轴标识
        # 左上角
        label_tl_x = MathTex("x", font_size=30).next_to(axes_top_left.x_axis.get_end(), RIGHT, buff=0.1)
        label_tl_y = MathTex("y", font_size=30).next_to(axes_top_left.y_axis.get_end(), UP, buff=0.1)
        
        # 右上角 - xy反过来
        label_tr_x = MathTex("y", font_size=30).next_to(axes_top_right.x_axis.get_end(), RIGHT, buff=0.1)
        label_tr_y = MathTex("x", font_size=30).next_to(axes_top_right.y_axis.get_end(), UP, buff=0.1)
        
        # 左下角
        label_bl_x = MathTex("x", font_size=30).next_to(axes_bottom_left.x_axis.get_end(), RIGHT, buff=0.1)
        label_bl_y = MathTex("y", font_size=30).next_to(axes_bottom_left.y_axis.get_end(), UP, buff=0.1)
        
        # 右下角
        label_br_x = MathTex("x", font_size=30).next_to(axes_bottom_right.x_axis.get_end(), RIGHT, buff=0.1)
        label_br_y = MathTex("y", font_size=30).next_to(axes_bottom_right.y_axis.get_end(), UP, buff=0.1)
        
        # 创建ValueTracker来控制x的范围
        x_tracker = ValueTracker(self.x_start)
        
        # 创建静态的外函数和反函数图像（完整绘制）
        # 外函数：x范围为内函数的值域
        graph_outer = axes_bottom_right.plot(
            self.outer_func,
            x_range=self.inner_range,
            color=YELLOW
        )
        
        # 反函数：计算外函数在内函数值域上的值域，作为反函数的x范围
        outer_samples = [self.outer_func(u) for u in np.linspace(self.inner_range[0], self.inner_range[1], 100)]
        outer_range = [min(outer_samples), max(outer_samples)]
        
        graph_inverse = axes_top_right.plot(
            self.inverse_outer_func,
            x_range=outer_range,
            color=GREEN
        )
        
        # 创建动态的内函数和复合函数图像
        graph_inner = always_redraw(lambda: axes_top_left.plot(
            self.inner_func,
            x_range=[self.x_start, x_tracker.get_value()],
            color=BLUE
        ))
        
        graph_composite = always_redraw(lambda: axes_bottom_left.plot(
            self.composite_func,
            x_range=[self.x_start, x_tracker.get_value()],
            color=RED
        ))
        
        # 创建动态点
        dot_inner = always_redraw(lambda: Dot(color=BLUE).move_to(
            axes_top_left.coords_to_point(x_tracker.get_value(), self.inner_func(x_tracker.get_value()))))
        
        dot_composite = always_redraw(lambda: Dot(color=RED).move_to(
            axes_bottom_left.coords_to_point(x_tracker.get_value(), self.composite_func(x_tracker.get_value()))))
        
        dot_outer = always_redraw(lambda: Dot(color=YELLOW).move_to(
            axes_bottom_right.coords_to_point(self.inner_func(x_tracker.get_value()), self.composite_func(x_tracker.get_value()))))
        
        dot_inverse = always_redraw(lambda: Dot(color=GREEN).move_to(
            axes_top_right.coords_to_point(self.composite_func(x_tracker.get_value()), self.inner_func(x_tracker.get_value()))))
        
        # 创建连接线（虚线）
        line_inner_to_inverse = always_redraw(
            lambda: DashedLine(
                axes_top_left.coords_to_point(x_tracker.get_value(), self.inner_func(x_tracker.get_value())),
                axes_top_right.coords_to_point(self.composite_func(x_tracker.get_value()), self.inner_func(x_tracker.get_value())),
                stroke_color=BLUE_A,
                stroke_width=1,
            )
        )

        line_inner_to_composite = always_redraw(
            lambda: DashedLine(
                axes_top_left.coords_to_point(x_tracker.get_value(), self.inner_func(x_tracker.get_value())),
                axes_bottom_left.coords_to_point(x_tracker.get_value(), self.composite_func(x_tracker.get_value())),
                stroke_color=BLUE_A,
                stroke_width=1,
            )
        )

        line_composite_to_outer = always_redraw(
            lambda: DashedLine(
                axes_bottom_left.coords_to_point(x_tracker.get_value(), self.composite_func(x_tracker.get_value())),
                axes_bottom_right.coords_to_point(self.inner_func(x_tracker.get_value()), self.composite_func(x_tracker.get_value())),
                stroke_color=BLUE_A,
                stroke_width=1,
            )
        )
        
        # 同时显示所有坐标系和轴标识
        self.play(
            Create(axes_top_left),
            Create(axes_top_right),
            Create(axes_bottom_left),
            Create(axes_bottom_right),
            Create(graph_outer),
            Create(graph_inverse),
            Create(dot_inner),
            Create(dot_composite),
            Create(dot_outer),
            Create(dot_inverse),
            Create(line_inner_to_inverse),
            Create(line_inner_to_composite),
            Create(line_composite_to_outer),
            Write(label_tl_x), Write(label_tl_y),
            Write(label_tr_x), Write(label_tr_y),
            Write(label_bl_x), Write(label_bl_y),
            Write(label_br_x), Write(label_br_y),
            run_time=2
        )
        
        # 添加动态图像到场景
        self.add(graph_inner, graph_composite)
        
        # 通过改变tracker值来实现匀速绘制
        self.play(
            x_tracker.animate.set_value(self.x_end),
            run_time=4,
            rate_func=linear
        )
        
        # 等待结束
        self.wait(3)


# 示例使用
class ExampleScene(CompositeFunctionAnimation):
    def __init__(self):
        # 定义内函数和外函数
        def inner_function(x):
            return x**2 - 1
        
        def outer_function(u):
            return np.exp(u) * 2 / np.exp(3)
        
        # 调用父类构造函数
        super().__init__(
            inner_func=inner_function,
            outer_func=outer_function,
            title_text="f(x) = e^{x^2-1}"
        )