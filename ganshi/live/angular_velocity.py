from manim import *
import numpy as np

class AngularVelocityDemo(Scene):
    def construct(self):
        # 创建非正方形画面
        
        # 创建两个独立坐标系
        # 左侧坐标系用于单位圆，左移更多，避免重叠
        circle_axes = Axes(
            x_range=[-1.5, 1.5, 1], 
            y_range=[-1.5, 1.5, 1],
            x_length=3,
            y_length=3,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "include_ticks": False,
                "tip_width": 0.2,
                "tip_height": 0.2
            }
        ).to_edge(LEFT, buff=0)  # 增加左侧缓冲，避免重叠
        
        # 右侧坐标系用于函数图像，水平刻度为pi/2
        graph_axes = Axes(
            x_range=[0, 8*PI, PI/2], 
            y_range=[-1.5, 1.5, 1],
            x_length=10,
            y_length=3,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "include_ticks": False,
                "tip_width": 0.2,
                "tip_height": 0.2
            }
        ).to_edge(RIGHT, buff=0.5)  # 函数图像坐标系靠右
        
        # 添加坐标刻度
        self.add_coordinates(circle_axes, graph_axes)
        
        # 计算单位圆半径
        origin_point = circle_axes.coords_to_point(0, 0)
        unit_point = circle_axes.coords_to_point(1, 0)
        unit_length = np.sqrt(np.sum((np.array(unit_point) - np.array(origin_point))**2))
        
        # 创建单位圆
        unit_circle = Circle(radius=unit_length, color=BLUE, stroke_width=2)
        unit_circle.move_to(origin_point)
        
        # 创建原点
        origin = Dot(origin_point, color=WHITE)
        
        # 创建动态角度追踪器
        angle = ValueTracker(0)
        
        # 创建角度多值标签
        multi_omega_label = always_redraw(
            lambda: VGroup(
                MathTex(r"t = ", f"{angle.get_value():.2f}", color=WHITE),
                MathTex(r"\omega_1 = 1: \theta_1 = ", f"{angle.get_value():.2f}", color=RED),
                MathTex(r"\omega_2 = 2: \theta_2 = ", f"{(2*angle.get_value()):.2f}", color=BLUE),
                MathTex(r"\omega_3 = 0.5: \theta_3 = ", f"{(0.5*angle.get_value()):.2f}", color=GREEN)
            ).arrange(DOWN, aligned_edge=LEFT).scale(0.5).to_corner(UR, buff=0.5)
        )
        
        # 创建三个不同速度的终边
        ray1 = always_redraw(
            lambda: Line(
                origin_point,
                circle_axes.coords_to_point(np.cos(angle.get_value()), np.sin(angle.get_value())),
                color=RED,
                stroke_width=2
            )
        )
        
        ray2 = always_redraw(
            lambda: Line(
                origin_point,
                circle_axes.coords_to_point(np.cos(2*angle.get_value()), np.sin(2*angle.get_value())),
                color=BLUE,
                stroke_width=2
            )
        )
        
        ray3 = always_redraw(
            lambda: Line(
                origin_point,
                circle_axes.coords_to_point(np.cos(0.5*angle.get_value()), np.sin(0.5*angle.get_value())),
                color=GREEN,
                stroke_width=2
            )
        )
        
        # 圆上的点
        point1 = always_redraw(
            lambda: Dot(
                circle_axes.coords_to_point(np.cos(angle.get_value()), np.sin(angle.get_value())),
                color=RED,
                radius=0.06
            )
        )
        
        point2 = always_redraw(
            lambda: Dot(
                circle_axes.coords_to_point(np.cos(2*angle.get_value()), np.sin(2*angle.get_value())),
                color=BLUE,
                radius=0.06
            )
        )
        
        point3 = always_redraw(
            lambda: Dot(
                circle_axes.coords_to_point(np.cos(0.5*angle.get_value()), np.sin(0.5*angle.get_value())),
                color=GREEN,
                radius=0.06
            )
        )
        
        # 创建不同频率的sin函数 - 在函数坐标系中绘制
        sin_normal = always_redraw(
            lambda: ParametricFunction(
                lambda t: graph_axes.coords_to_point(t, np.sin(t)),
                t_range=[0, angle.get_value()],
                color=RED,
                stroke_width=2
            )
        )
        
        sin_fast = always_redraw(
            lambda: ParametricFunction(
                lambda t: graph_axes.coords_to_point(t, np.sin(2*t)),
                t_range=[0, angle.get_value()],
                color=BLUE,
                stroke_width=2
            )
        )
        
        sin_slow = always_redraw(
            lambda: ParametricFunction(
                lambda t: graph_axes.coords_to_point(t, np.sin(0.5*t)),
                t_range=[0, angle.get_value()],
                color=GREEN,
                stroke_width=2
            )
        )
        
        # 创建从单位圆到函数值的辅助线
        sin_normal_vline = always_redraw(
            lambda: DashedLine(
                origin_point,
                circle_axes.coords_to_point(0, np.sin(angle.get_value())),
                color=RED,
                stroke_width=1,
                stroke_opacity=0.7
            )
        )
        
        sin_fast_vline = always_redraw(
            lambda: DashedLine(
                origin_point,
                circle_axes.coords_to_point(0, np.sin(2*angle.get_value())),
                color=BLUE,
                stroke_width=1,
                stroke_opacity=0.7
            )
        )
        
        sin_slow_vline = always_redraw(
            lambda: DashedLine(
                origin_point,
                circle_axes.coords_to_point(0, np.sin(0.5*angle.get_value())),
                color=GREEN,
                stroke_width=1,
                stroke_opacity=0.7
            )
        )
        
        # 创建从单位圆到函数图像的连接线 - 添加这些连接线
        cross_connection1 = always_redraw(
            lambda: DashedLine(
                circle_axes.coords_to_point(0, np.sin(angle.get_value())),
                graph_axes.coords_to_point(angle.get_value(), np.sin(angle.get_value())),
                color=RED,
                stroke_width=1,
                stroke_opacity=0.7
            )
        )
        
        cross_connection2 = always_redraw(
            lambda: DashedLine(
                circle_axes.coords_to_point(0, np.sin(2*angle.get_value())),
                graph_axes.coords_to_point(angle.get_value(), np.sin(2*angle.get_value())),
                color=BLUE, 
                stroke_width=1,
                stroke_opacity=0.7
            )
        )
        
        cross_connection3 = always_redraw(
            lambda: DashedLine(
                circle_axes.coords_to_point(0, np.sin(0.5*angle.get_value())),
                graph_axes.coords_to_point(angle.get_value(), np.sin(0.5*angle.get_value())),
                color=GREEN,
                stroke_width=1,
                stroke_opacity=0.7
            )
        )
        
        # 创建轨迹点 - 在函数坐标系中
        sin_normal_trace = always_redraw(
            lambda: Dot(
                graph_axes.coords_to_point(angle.get_value(), np.sin(angle.get_value())),
                color=RED,
                radius=0.05
            )
        )
        
        sin_fast_trace = always_redraw(
            lambda: Dot(
                graph_axes.coords_to_point(angle.get_value(), np.sin(2*angle.get_value())),
                color=BLUE,
                radius=0.05
            )
        )
        
        sin_slow_trace = always_redraw(
            lambda: Dot(
                graph_axes.coords_to_point(angle.get_value(), np.sin(0.5*angle.get_value())),
                color=GREEN,
                radius=0.05
            )
        )
        
        # 添加基本元素
        self.add(circle_axes, graph_axes)
        self.add(unit_circle, origin)
        self.add(multi_omega_label)
        
        # 添加动画元素
        self.play(
            Create(ray1), Create(ray2), Create(ray3),
            Create(point1), Create(point2), Create(point3)
        )
        
        self.play(
            Create(sin_normal_vline), Create(sin_fast_vline), Create(sin_slow_vline)
        )
        
        self.play(
            Create(sin_normal), Create(sin_fast), Create(sin_slow),
            Create(sin_normal_trace), Create(sin_fast_trace), Create(sin_slow_trace)
        )
        
        # 添加单位圆到函数图像的连接线
        self.play(
            Create(cross_connection1), 
            Create(cross_connection2), 
            Create(cross_connection3)
        )
        
        # 动画展示 - 确保画到8π为止
        self.play(angle.animate.set_value(8*PI), run_time=15, rate_func=linear)
        self.wait(1)
        
    def add_coordinates(self, circle_axes, graph_axes):
        """添加坐标轴刻度"""
        # 单位圆坐标系刻度
        circle_x_ticks = VGroup()
        circle_y_ticks = VGroup()
        
        # 添加-1, 0, 1刻度
        for x in [-1, 0, 1]:
            tick_pos = circle_axes.coords_to_point(x, 0)
            dot = Dot(tick_pos, radius=0.04, color=WHITE)
            label = MathTex(f"{x}", color=WHITE).scale(0.5)
            label.next_to(dot, DOWN, buff=0.1)
            circle_x_ticks.add(dot, label)
        
        for y in [-1, 0, 1]:
            tick_pos = circle_axes.coords_to_point(0, y)
            dot = Dot(tick_pos, radius=0.04, color=WHITE)
            label = MathTex(f"{y}", color=WHITE).scale(0.5)
            label.next_to(dot, LEFT, buff=0.1)
            circle_y_ticks.add(dot, label)
        
        # 函数坐标系π/2刻度
        graph_x_ticks = VGroup()
        graph_y_ticks = VGroup()
        
        # x轴π/2刻度
        for i in range(17):  # 0到8π，以π/2为间隔
            pos = i * PI/2
            if pos > 8*PI:
                continue
                
            tick_pos = graph_axes.coords_to_point(pos, 0)
            
            # 为偶数倍π/2（即整数倍π）使用正常大小的点和标签
            if i % 2 == 0:
                dot = Dot(tick_pos, radius=0.05, color=YELLOW)
                pi_value = i // 2
                if pi_value == 0:
                    label_text = "0"
                elif pi_value == 1:
                    label_text = r"\pi"
                else:
                    label_text = f"{pi_value}\pi"
                label = MathTex(label_text, color=YELLOW).scale(0.5)
            else:
                # 为奇数倍π/2使用更小的点和标签
                dot = Dot(tick_pos, radius=0.03, color=YELLOW_D)  # 更小、更暗的点
                # 使用更简单的π/2表示法
                label_text = f"{i}" + r"\pi/2"
                label = MathTex(label_text, color=YELLOW_D).scale(0.3)  # 更小的标签和更暗的颜色
                
            label.next_to(dot, DOWN, buff=0.1)
            graph_x_ticks.add(dot, label)
        
        # y轴刻度
        for y in [-1, 0, 1]:
            tick_pos = graph_axes.coords_to_point(0, y)
            dot = Dot(tick_pos, radius=0.04, color=WHITE)
            label = MathTex(f"{y}", color=WHITE).scale(0.5)
            label.next_to(dot, LEFT, buff=0.1)
            graph_y_ticks.add(dot, label)
        
        # 添加刻度到坐标轴
        circle_axes.add(circle_x_ticks, circle_y_ticks)
        graph_axes.add(graph_x_ticks, graph_y_ticks)
        
        return 