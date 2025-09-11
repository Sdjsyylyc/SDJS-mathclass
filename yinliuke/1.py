from manim import *
import numpy as np
import sys
import os
import math
# 将项目根目录添加到 sys.path（从当前文件向上两级到 SDJS-mathclass）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from modules import SliderComponent, CustomAxes, CollisionEffect, LinearFunctionPointSlope, PowerFunction

class Xiandaoke01(Scene):
    def construct(self):
        # 背景设置为白色
        self.camera.background_color = WHITE
        # 创建自定义坐标系（放大范围以完整展示双曲线与运动）
        axes = CustomAxes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=8,
            y_length=8,
            axis_config={"color": BLACK, "stroke_width": 2, "tip_length": 0.2},
        )
        self.play(Create(axes), run_time=0.5)

        # 双曲线参数：x^2/8 - y^2/8 = 1  => a^2 = 8, b^2 = 8, c^2 = a^2 + b^2 = 16
        a2 = 8
        b2 = 8
        a = math.sqrt(a2)
        b = math.sqrt(b2)
        c = math.sqrt(a2 + b2)

        # 先出现三个点：两焦点与动点（动点从右支上方开始）
        focus_right = Dot(axes.c2p(c, 0), color=BLUE)
        focus_left = Dot(axes.c2p(-c, 0), color=BLUE)

        u_max = 1.4
        # 动点初始在右支靠上处
        start_right = axes.c2p(a * math.cosh(u_max), b * math.sinh(u_max))
        moving_dot = Dot(start_right, color=RED)

        self.play(FadeIn(VGroup(focus_right, focus_left, moving_dot)))

        # 连接动点到两焦点的线段（右支阶段的规则）：
        # - 右焦点连线固定为黄色
        # - 左焦点连线分段：上半段黄色（长度与右焦点连线等长），下半段蓝色
        def get_right_phase_segments():
            p = moving_dot.get_center()
            r = focus_right.get_center()
            l = focus_left.get_center()
            right_len = np.linalg.norm(p - r)
            vec_left = l - p
            left_len = np.linalg.norm(vec_left)
            if left_len == 0:
                split_point = p
            else:
                unit_vec = vec_left / max(left_len, 1e-8)
                yellow_len = min(right_len, left_len)
                split_point = p + unit_vec * yellow_len
            return p, r, l, split_point

        # 先以一次性静态线段做“出现动画”：等长两段同时绘制，然后绘制剩余部分（全程匀速）
        temp_right_line = Line(moving_dot.get_center(), focus_right.get_center(), color=BLUE)
        p0, r0, l0, s0 = get_right_phase_segments()
        temp_left_equal = Line(p0, s0, color=BLUE)
        temp_left_remainder = Line(s0, l0, color=ORANGE)
        self.play(Create(temp_right_line), Create(temp_left_equal), run_time=0.4, rate_func=linear)
        self.play(Create(temp_left_remainder), run_time=0.4, rate_func=linear)
        # 再替换为动态跟随的 always_redraw 版本
        line_to_right = always_redraw(lambda: Line(moving_dot.get_center(), focus_right.get_center(), color=BLUE))
        left_yellow = always_redraw(lambda: Line(get_right_phase_segments()[0], get_right_phase_segments()[3], color=BLUE))
        left_blue = always_redraw(lambda: Line(get_right_phase_segments()[3], get_right_phase_segments()[2], color=ORANGE))
        self.add(line_to_right, left_yellow, left_blue)
        # 移除临时静态线段
        self.remove(temp_right_line, temp_left_equal, temp_left_remainder)

        # 使用 TracedPath 让动点绘制曲线：先右支（从上到下），再左支（从上到下）
        u_tracker = ValueTracker(u_max)

        def update_on_right(dot):
            u = u_tracker.get_value()
            x = a * math.cosh(u)
            y = b * math.sinh(u)
            dot.move_to(axes.c2p(x, y))
            return dot

        traced_right_up = TracedPath(moving_dot.get_center, stroke_color=ORANGE, stroke_width=4, dissipating_time=float('inf'))
        moving_dot.add_updater(update_on_right)
        self.add(traced_right_up)
        # 上半段：u 从 u_max 减小到 0
        self.play(u_tracker.animate.set_value(0.0), run_time=2, rate_func=linear)
        # 冻结上半段轨迹，防止继续更新导致覆盖
        traced_right_up.clear_updaters()
        # 下半段：新建一个轨迹对象继续从 0 到 -u_max
        traced_right_down = TracedPath(moving_dot.get_center, stroke_color=ORANGE, stroke_width=4, dissipating_time=float('inf'))
        self.add(traced_right_down)
        self.play(u_tracker.animate.set_value(-u_max), run_time=2, rate_func=linear)
        moving_dot.remove_updater(update_on_right)
        # 右支结束后，动点与连线淡出（保留轨迹）
        self.play(FadeOut(VGroup(moving_dot, line_to_right, left_yellow, left_blue)), run_time=0.6)

        # 右支绘制完成后，创建新的动点用于左支，避免产生直线轨迹
        moving_dot_left = Dot(axes.c2p(-a * math.cosh(u_max), b * math.sinh(u_max)), color=RED)
        self.add(moving_dot_left)

        # 左支阶段：
        # - 左焦点连线固定为黄色
        # - 右焦点连线分段：上半段黄色（长度与左焦点连线等长），下半段蓝色
        def get_left_phase_segments():
            p = moving_dot_left.get_center()
            l = focus_left.get_center()
            r = focus_right.get_center()
            left_len = np.linalg.norm(p - l)
            vec_right = r - p
            right_len = np.linalg.norm(vec_right)
            if right_len == 0:
                split_point = p
            else:
                unit_vec = vec_right / max(right_len, 1e-8)
                yellow_len = min(left_len, right_len)
                split_point = p + unit_vec * yellow_len
            return p, l, r, split_point

        # 左支连线的出现动画
        temp_left_line = Line(moving_dot_left.get_center(), focus_left.get_center(), color=BLUE)
        q0, l1, r1, s1 = get_left_phase_segments()
        temp_right_white = Line(q0, s1, color=BLUE)
        temp_right_blue = Line(s1, r1, color=ORANGE)
        # 等长两段同时出现，然后剩余部分（匀速）
        self.play(Create(temp_left_line), Create(temp_right_white), run_time=0.4, rate_func=linear)
        self.play(Create(temp_right_blue), run_time=0.4, rate_func=linear)
        # 动态版本
        line_to_left_y = always_redraw(lambda: Line(moving_dot_left.get_center(), focus_left.get_center(), color=BLUE))
        right_yellow = always_redraw(lambda: Line(get_left_phase_segments()[0], get_left_phase_segments()[3], color=BLUE))
        right_blue = always_redraw(lambda: Line(get_left_phase_segments()[3], get_left_phase_segments()[2], color=ORANGE))
        self.add(line_to_left_y, right_yellow, right_blue)
        self.remove(temp_left_line, temp_right_white, temp_right_blue)

        # 左支轨迹绘制：从上到下
        u_tracker.set_value(u_max)
        def update_on_left(dot):
            u = u_tracker.get_value()
            x = -a * math.cosh(u)
            y = b * math.sinh(u)
            dot.move_to(axes.c2p(x, y))
            return dot

        traced_left_up = TracedPath(moving_dot_left.get_center, stroke_color=ORANGE, stroke_width=4, dissipating_time=float('inf'))
        moving_dot_left.add_updater(update_on_left)
        self.add(traced_left_up)
        # 上半段：u 从 u_max 到 0
        self.play(u_tracker.animate.set_value(0.0), run_time=2, rate_func=linear)
        traced_left_up.clear_updaters()
        # 下半段
        traced_left_down = TracedPath(moving_dot_left.get_center, stroke_color=ORANGE, stroke_width=4, dissipating_time=float('inf'))
        self.add(traced_left_down)
        self.play(u_tracker.animate.set_value(-u_max), run_time=2, rate_func=linear)
        moving_dot_left.remove_updater(update_on_left)
        # 左支结束后，动点与连线淡出（保留轨迹）
        self.play(FadeOut(VGroup(moving_dot_left, line_to_left_y, right_yellow, right_blue)), run_time=0.6)

        # 最终淡出坐标轴与焦点，仅保留轨迹
        self.play(FadeOut(VGroup(axes, focus_right, focus_left)), run_time=0.6)

        self.wait(0.5)