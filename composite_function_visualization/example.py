from manim import *
import numpy as np


class InverseFunctionVisualization(Scene):
    def construct(self):
        # 统一的坐标系范围
        x_range = [-1, 2, 1]
        y_range = [-1, 2, 1]
        axis_length = 3
        x_start = -1
        x_end = 2
        
        # 创建四个坐标系 - 全部白色，箭头更小
        # 左上角 - 内函数 x²+1
        axes_top_left = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=axis_length,
            y_length=axis_length,
            axis_config={"color": WHITE, "tip_length": 0.02, "stroke_width": 1, "include_tip":False}
        ).shift(LEFT * 3.5 + UP * 1.5)
        
        # 右上角 - 反函数（xy交换）
        axes_top_right = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=axis_length,
            y_length=axis_length,
            axis_config={"color": WHITE, "tip_length": 0.02, "stroke_width": 1, "include_tip":False}
        ).shift(RIGHT * 3.5 + UP * 1.5)
        
        axes_bottom_left = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=axis_length,
            y_length=axis_length,
            axis_config={"color": WHITE, "tip_length": 0.02, "stroke_width": 1, "include_tip":False}
        ).shift(LEFT * 3.5 + DOWN * 2)
        
        axes_bottom_right = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=axis_length,
            y_length=axis_length,
            axis_config={"color": WHITE, "tip_length": 0.02, "stroke_width": 1, "include_tip":False}
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
        x_tracker = ValueTracker(x_start)
        
        # 定义函数
        # 内函数: u = x² - 1
        def inner_func(x):
            return x**2 - 1
        
        def composite_func(x):
            u = inner_func(x)
            return np.exp(u)*2/np.exp(3)
        
        def outer_func(x):
            return np.exp(x)*2/np.exp(3)
        
        def inverse_outer_func(y):
            return np.log(y/2*np.exp(3))
        
        # 使用always_redraw创建动态更新的函数图像
        graph_inner = always_redraw(lambda: axes_top_left.plot(
            inner_func,
            x_range=[x_start, x_tracker.get_value()],
            color=BLUE
        ))
        
        graph_inverse = always_redraw(lambda: axes_top_right.plot(
            inverse_outer_func,
            x_range=[outer_func(inner_func(0)), outer_func(inner_func(x_end))],
            color=GREEN
        ))
        
        graph_composite = always_redraw(lambda: axes_bottom_left.plot(
            composite_func,
            x_range=[x_start, x_tracker.get_value()],
            color=RED
        ))
        
        graph_outer = always_redraw(lambda: axes_bottom_right.plot(
            outer_func,
            x_range=[inner_func(0), inner_func(x_end)],
            color=YELLOW
        ))

        dot_inner = always_redraw(lambda: Dot(color=BLUE).move_to(axes_top_left.coords_to_point(x_tracker.get_value(), inner_func(x_tracker.get_value()))))
        dot_composite = always_redraw(lambda: Dot(color=RED).move_to(axes_bottom_left.coords_to_point(x_tracker.get_value(), composite_func(x_tracker.get_value()))))
        dot_outer = always_redraw(lambda: Dot(color=YELLOW).move_to(axes_bottom_right.coords_to_point(inner_func(x_tracker.get_value()), composite_func(x_tracker.get_value()))))
        dot_inverse = always_redraw(lambda: Dot(color=GREEN).move_to(axes_top_right.coords_to_point(composite_func(x_tracker.get_value()), inner_func(x_tracker.get_value()))))

        line_inner_to_outer = always_redraw(
            lambda: DashedLine(
                axes_top_left.coords_to_point(x_tracker.get_value(), inner_func(x_tracker.get_value())),
                axes_top_right.coords_to_point(composite_func(x_tracker.get_value()), inner_func(x_tracker.get_value())),
                stroke_color=BLUE_A,
                stroke_width=1,
            )
        )

        line_inner_to_composite = always_redraw(
            lambda: DashedLine(
                axes_top_left.coords_to_point(x_tracker.get_value(), inner_func(x_tracker.get_value())),
                axes_bottom_left.coords_to_point(x_tracker.get_value(), composite_func(x_tracker.get_value())),
                stroke_color=BLUE_A,
                stroke_width=1,
            )
        )

        line_composite_to_outer = always_redraw(
            lambda: DashedLine(
                axes_bottom_left.coords_to_point(x_tracker.get_value(), composite_func(x_tracker.get_value())),
                axes_bottom_right.coords_to_point(inner_func(x_tracker.get_value()), composite_func(x_tracker.get_value())),
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
            Create(line_inner_to_outer),
            Create(line_inner_to_composite),
            Create(line_composite_to_outer),
            Write(label_tl_x), Write(label_tl_y),
            Write(label_tr_x), Write(label_tr_y),
            Write(label_bl_x), Write(label_bl_y),
            Write(label_br_x), Write(label_br_y),
            run_time=2
        )
        
        # 添加图像到场景
        self.add(graph_inner, graph_composite)
        
        # 通过改变tracker值来实现匀速绘制
        self.play(
            x_tracker.animate.set_value(x_end),
            run_time=4,
            rate_func=linear
        )
        
        # 等待结束
        self.wait(3)