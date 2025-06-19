from manim import *
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import SliderComponent, CustomAxes, CollisionEffect

class LineFormsAnimation(Scene):
    def construct(self):
        # 创建坐标系
        axes = CustomAxes(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2, "include_ticks": False},
        ).shift(LEFT*1.5)
        self.play(Create(axes), run_time=0.8)
        
        # 场景1：点斜式 - 围绕定点旋转的"钢管"
        # 清除其他元素
        self.clear()
        self.add(axes)
        
        # 公式显示
        formula1 = MathTex("y - y_0 = k(x - x_0)", font_size=45, color=WHITE)
        formula1.to_corner(UL, buff=0.5)
        self.play(Write(formula1))
        
        # 参数跟踪器 - k_tracker现在表示倾斜角（弧度）
        k_tracker = ValueTracker(np.pi/6)  # 初始倾斜角30度
        x0_tracker = ValueTracker(0.8)
        y0_tracker = ValueTracker(0.2)
        
        # 三个滑块 - k滑块现在控制倾斜角，使用取模功能让它可以连续旋转
        k_slider = SliderComponent("k", k_tracker, -np.pi/2 + 0.01, np.pi/2 - 0.01, [4.5, 2.8, 0], use_modulo=True)
        x0_slider = SliderComponent("x_0", x0_tracker, -1.5, 1.5, [4.5, 2.4, 0])
        y0_slider = SliderComponent("y_0", y0_tracker, -1, 1, [4.5, 2.0, 0])
        self.play(Create(k_slider), Create(x0_slider), Create(y0_slider))
        
        # 动态定点
        def get_fixed_point():
            return Dot(axes.c2p(x0_tracker.get_value(), y0_tracker.get_value()), color=YELLOW, radius=0.08)
        
        fixed_point = always_redraw(get_fixed_point)
        self.play(Create(fixed_point), run_time=0.5)
        
                # 使用always_redraw的旋转直线
        def get_rotating_line():
            raw_angle = k_tracker.get_value()  # 原始倾斜角（可能超出范围）
            x0 = x0_tracker.get_value()
            y0 = y0_tracker.get_value()
            
            # 将角度规范化到(-π/2, π/2)范围内，用于实际绘制
            angle_range = (np.pi/2 - 0.01) - (-np.pi/2 + 0.01)
            normalized_angle = ((raw_angle - (-np.pi/2 + 0.01)) % angle_range) + (-np.pi/2 + 0.01)
            
            # 如果接近垂直线（倾斜角接近±π/2）
            if abs(abs(normalized_angle) - np.pi/2) < 0.05:
                # 绘制垂直线，截断在y=[-3,3]范围内
                return Line(
                    axes.c2p(x0, -3), 
                    axes.c2p(x0, 3), 
                    color=BLUE, 
                    stroke_width=5
                )
            else:
                # 通过倾斜角计算斜率: k = tan(angle)
                slope = np.tan(normalized_angle)
                # 点斜式: y - y0 = k(x - x0)
                def line_func(x):
                    y = slope * (x - x0) + y0
                    # 截断y值在[-3,3]范围内
                    return max(-3, min(3, y))
                
                # 计算x范围，确保y在[-3,3]内
                # 求解 slope * (x - x0) + y0 = ±3
                if abs(slope) > 0.001:  # 避免除零
                    x_at_y3 = (3 - y0) / slope + x0
                    x_at_y_minus3 = (-3 - y0) / slope + x0
                    x_min = max(-4.8, min(x_at_y3, x_at_y_minus3))
                    x_max = min(4.8, max(x_at_y3, x_at_y_minus3))
                else:
                    x_min, x_max = -4.8, 4.8
                
                return axes.plot(line_func, x_range=[x_min, x_max], color=BLUE, stroke_width=5)
        
        rotating_line = always_redraw(get_rotating_line)
        
        # 定点标签
        def get_point_label():
            x0 = x0_tracker.get_value()
            y0 = y0_tracker.get_value()
            label = MathTex("(x_0, y_0)", font_size=40, color=YELLOW)
            label.next_to(axes.c2p(x0, y0), UR, buff=0.1)
            return label
        
        point_label = always_redraw(get_point_label)
        
        self.play(Create(rotating_line), Create(point_label), run_time=0.5)
        
                # 连续变化参数 - 点斜式核心演示 (总共约95秒)
        # 展示"钢管旋转"概念 - 正反向旋转 + 定点变化组合，18组动画，每组4秒+1秒停顿
        current_angle = np.pi/6  # 当前角度追踪
        
        # 第1组：顺时针转1圈 + 定点右移
        current_angle += 2*np.pi
        self.play(k_tracker.animate.set_value(current_angle), x0_tracker.animate.set_value(1.2), run_time=4)
        self.wait(1)
        
        # 第2组：逆时针转1.5圈 + 定点上移
        current_angle -= 3*np.pi
        self.play(k_tracker.animate.set_value(current_angle), y0_tracker.animate.set_value(0.8), run_time=4)
        self.wait(1)
        
        # 第3组：顺时针转3/4圈 + 定点左下移
        current_angle += 3*np.pi/2
        self.play(k_tracker.animate.set_value(current_angle), x0_tracker.animate.set_value(-0.5), y0_tracker.animate.set_value(-0.3), run_time=4)
        self.wait(1)
        
        # 第4组：逆时针转1圈
        current_angle -= 2*np.pi
        self.play(k_tracker.animate.set_value(current_angle), run_time=4)
        self.wait(1)
        
        # 第5组：顺时针转2圈 + 定点右上移
        current_angle += 4*np.pi
        self.play(k_tracker.animate.set_value(current_angle), x0_tracker.animate.set_value(0.6), y0_tracker.animate.set_value(0.5), run_time=4)
        self.wait(1)
        
        # 第6组：逆时针转半圈 + 定点左移
        current_angle -= np.pi
        self.play(k_tracker.animate.set_value(current_angle), x0_tracker.animate.set_value(-0.8), run_time=4)
        self.wait(1)
        
        # 第7组：顺时针转1.5圈 + 定点下移
        current_angle += 3*np.pi
        self.play(k_tracker.animate.set_value(current_angle), y0_tracker.animate.set_value(-0.4), run_time=4)
        self.wait(1)
        
        # 第8组：逆时针转2.5圈 + 定点居中上移
        current_angle -= 5*np.pi
        self.play(k_tracker.animate.set_value(current_angle), x0_tracker.animate.set_value(0.1), y0_tracker.animate.set_value(0.7), run_time=4)
        self.wait(1)
        
        # 第9组：顺时针转1圈 + 定点右下移
        current_angle += 2*np.pi
        self.play(k_tracker.animate.set_value(current_angle), x0_tracker.animate.set_value(1.0), y0_tracker.animate.set_value(-0.2), run_time=4)
        self.wait(1)
        
        # 第10组：逆时针转3/4圈 + 定点左上移
        current_angle -= 3*np.pi/2
        self.play(k_tracker.animate.set_value(current_angle), x0_tracker.animate.set_value(-0.4), y0_tracker.animate.set_value(0.6), run_time=4)
        self.wait(1)
        
        # 第11组：顺时针转2.5圈
        current_angle += 5*np.pi
        self.play(k_tracker.animate.set_value(current_angle), run_time=4)
        self.wait(1)
        
        # 第12组：逆时针转1.5圈 + 定点右移
        current_angle -= 3*np.pi
        self.play(k_tracker.animate.set_value(current_angle), x0_tracker.animate.set_value(0.7), run_time=4)
        self.wait(1)
        
        # 第13组：顺时针转半圈 + 定点下移
        current_angle += np.pi
        self.play(k_tracker.animate.set_value(current_angle), y0_tracker.animate.set_value(0.0), run_time=4)
        self.wait(1)
        
        # 第14组：逆时针转2圈 + 定点左移
        current_angle -= 4*np.pi
        self.play(k_tracker.animate.set_value(current_angle), x0_tracker.animate.set_value(-0.2), run_time=4)
        self.wait(1)
        
        # 第15组：顺时针转3/4圈 + 定点上移
        current_angle += 3*np.pi/2
        self.play(k_tracker.animate.set_value(current_angle), y0_tracker.animate.set_value(0.4), run_time=4)
        self.wait(1)
        
        # 第16组：逆时针转1圈 + 定点右下移
        current_angle -= 2*np.pi
        self.play(k_tracker.animate.set_value(current_angle), x0_tracker.animate.set_value(0.5), y0_tracker.animate.set_value(-0.1), run_time=4)
        self.wait(1)
        
        # 第17组：顺时针转1.5圈 + 定点左上移
        current_angle += 3*np.pi
        self.play(k_tracker.animate.set_value(current_angle), x0_tracker.animate.set_value(-0.3), y0_tracker.animate.set_value(0.3), run_time=4)
        self.wait(1)
        
        # 第18组：逆时针转1圈 + 复位到初始位置
        current_angle -= 2*np.pi
        self.play(k_tracker.animate.set_value(current_angle), x0_tracker.animate.set_value(0.8), y0_tracker.animate.set_value(0.2), run_time=4)
        self.wait(1)
        
        self.wait(3)  # 最后停顿3秒强调效果

        # 过定点做切线演示 - "钢管顶硬墙"概念
        unit_length = axes.c2p(1, 0)[0] - axes.c2p(0, 0)[0]
        circle = Circle(radius=unit_length, color=GREEN).move_to(axes.c2p(1, -1))

        self.play(x0_tracker.animate.set_value(-1), y0_tracker.animate.set_value(1), k_tracker.animate.set_value(np.pi/4),
                  Create(circle), run_time=4)
        self.wait(2)

        # 展示切线寻找过程
        tangent_slope = (np.sqrt(7)-4)/3
        tangent_angle = np.arctan(tangent_slope)
        

        
        # 计算切点坐标
        # 直线方程: y - 1 = tan(tangent_angle) * (x - (-1))
        # 圆心(1, -1)，半径1
        # 切点计算：设切点为(x0, y0)
        slope = tangent_slope
        # 切点到圆心的向量垂直于切线
        # 切线斜率为slope，垂直线斜率为-1/slope
        # 从圆心(1, -1)到切点的向量方向
        denominator = np.sqrt(1 + slope**2)
        # 两个切点
        cx, cy = 1, -1  # 圆心
        r = 1  # 半径
        
        # 第一个切点
        x1_tangent = cx - r * slope / denominator
        y1_tangent = cy + r / denominator
        
        # 第二个切点  
        x2_tangent = cx + r * slope / denominator
        y2_tangent = cy - r / denominator
        
        # 选择与直线方程匹配的切点
        # 直线: y - 1 = slope * (x + 1)
        # 检查哪个切点在直线上
        y1_on_line = 1 + slope * (x1_tangent + 1)
        y2_on_line = 1 + slope * (x2_tangent + 1)
        
        if abs(y1_on_line - y1_tangent) < abs(y2_on_line - y2_tangent):
            touch_point = axes.c2p(x1_tangent, y1_tangent)
        else:
            touch_point = axes.c2p(x2_tangent, y2_tangent)
        
        # 动画向切线角度变化，当接近时产生碰撞效果
        self.play(k_tracker.animate.set_value(tangent_angle), run_time=6)
        
        # 在切点处创建碰撞特效
        collision_effect = CollisionEffect(touch_point)
        self.add(collision_effect.get_lines())
        
        self.play(collision_effect.get_animation(), run_time=1.0)
        
        # 移除直线
        self.remove(collision_effect.get_lines())
        
        self.wait(2)  # 强调第一个切线
        
        # 展示第二个切线 - 顺时针旋转到另一个切点
        tangent_slope2 = -(np.sqrt(7)+4)/3
        tangent_angle2 = np.arctan(tangent_slope2)+np.pi-0.02
        
        # 计算第二个切点坐标
        slope2 = tangent_slope2
        denominator2 = np.sqrt(1 + slope2**2)
        
        # 第二个切点的两个可能位置
        x1_tangent2 = cx - r * slope2 / denominator2
        y1_tangent2 = cy + r / denominator2
        
        x2_tangent2 = cx + r * slope2 / denominator2
        y2_tangent2 = cy - r / denominator2
        
        # 选择与直线方程匹配的切点
        # 直线: y - 1 = slope2 * (x + 1)
        y1_on_line2 = 1 + slope2 * (x1_tangent2 + 1)
        y2_on_line2 = 1 + slope2 * (x2_tangent2 + 1)
        
        if abs(y1_on_line2 - y1_tangent2) < abs(y2_on_line2 - y2_tangent2):
            touch_point2 = axes.c2p(x1_tangent2, y1_tangent2)
        else:
            touch_point2 = axes.c2p(x2_tangent2, y2_tangent2)
        
        # 顺时针旋转到第二个切线角度
        self.play(k_tracker.animate.set_value(tangent_angle2), run_time=6)
        
        # 在第二个切点处创建碰撞特效
        collision_effect2 = CollisionEffect(touch_point2)
        self.add(collision_effect2.get_lines())
        
        # 播放第二个碰撞特效
        self.play(collision_effect2.get_animation(), run_time=1.0)
        
        # 移除第二批直线
        self.remove(collision_effect2.get_lines())
        
        self.wait(2)  # 强调第二个切线概念
        
        self.wait(0.8)
        self.play(FadeOut(rotating_line),
                  FadeOut(fixed_point),
                  FadeOut(point_label),
                  FadeOut(circle),
                  FadeOut(k_slider),
                  FadeOut(x0_slider),
                  FadeOut(y0_slider),
                  FadeOut(formula1), run_time=0.5)
        
        # 场景2：斜截式 - 平行线族平移
        # 清除其他元素
        self.clear()
        self.add(axes)
        
        # 公式显示
        formula2 = MathTex("y = kx + b", font_size=45, color=WHITE)
        formula2.to_corner(UL, buff=0.5)
        self.play(Write(formula2))
        
        # 参数跟踪器
        k_tracker = ValueTracker(0.7)
        b_tracker = ValueTracker(0)
        
        # 两个滑块
        k_slider = SliderComponent("k", k_tracker, -2, 2, [4.5, 2.8, 0])
        b_slider = SliderComponent("b", b_tracker, -1.8, 1.8, [4.5, 2.4, 0])
        self.play(Create(k_slider), Create(b_slider))
        
        # 使用always_redraw的平行线
        def get_parallel_line():
            slope = k_tracker.get_value()
            intercept = b_tracker.get_value()
            # 斜截式: y = kx + b
            def line_func(x):
                y = slope * x + intercept
                return max(-3, min(3, y))
            
            # 计算x范围，确保y在[-3,3]内
            if abs(slope) > 0.001:
                x_at_y3 = (3 - intercept) / slope
                x_at_y_minus3 = (-3 - intercept) / slope
                x_min = max(-4.8, min(x_at_y3, x_at_y_minus3))
                x_max = min(4.8, max(x_at_y3, x_at_y_minus3))
            else:
                x_min, x_max = -4.8, 4.8
                
            return axes.plot(line_func, x_range=[x_min, x_max], color=BLUE, stroke_width=5)
        
        parallel_line = always_redraw(get_parallel_line)
        
        # y轴截距点
        def get_y_intercept_point():
            return Dot(axes.c2p(0, b_tracker.get_value()), color=YELLOW, radius=0.06)
        
        y_intercept_point = always_redraw(get_y_intercept_point)
        
        # y轴截距标签
        def get_y_intercept_label():
            b = b_tracker.get_value()
            label = MathTex("(0, b)", font_size=40, color=YELLOW)
            label.next_to(axes.c2p(0, b), RIGHT, buff=0.1)
            return label
        
        y_intercept_label = always_redraw(get_y_intercept_label)
        
        self.play(Create(parallel_line), Create(y_intercept_point), Create(y_intercept_label), run_time=0.5)
        
        # 连续变化参数 - 斜截式核心演示 (总共约60秒)
        # 展示截距快速变化 - 上下平移
        self.play(b_tracker.animate.set_value(1.8), run_time=4)
        self.play(b_tracker.animate.set_value(-1.8), run_time=4)
        self.play(b_tracker.animate.set_value(1.8), run_time=3)
        self.play(b_tracker.animate.set_value(-1.8), run_time=3)
        self.play(b_tracker.animate.set_value(0), run_time=2)
        
        # 展示斜率快速变化
        self.play(k_tracker.animate.set_value(-1.5), run_time=3)
        self.play(k_tracker.animate.set_value(2), run_time=3)
        self.play(k_tracker.animate.set_value(-1.5), run_time=3)
        self.play(k_tracker.animate.set_value(2), run_time=3)
        
        # 综合快速变化
        self.play(k_tracker.animate.set_value(0.7), b_tracker.animate.set_value(1.2), run_time=3)
        self.play(k_tracker.animate.set_value(-0.8), b_tracker.animate.set_value(-1.5), run_time=3)
        self.play(k_tracker.animate.set_value(0.7), b_tracker.animate.set_value(0), run_time=3)        
        
        # 展示与ln(x)图像相切的演示 - "直线顶曲线"概念
        # 创建ln(x)曲线
        def ln_func(x):
            if x <= 0:
                return -10  # 避免ln(0)或ln(负数)
            return np.log(x)
        
        ln_curve = axes.plot(ln_func, x_range=[0.01, 4.5], color=GREEN, stroke_width=4)
        
        # 设置初始值：截距b=-1，斜率k=5
        self.play(Create(ln_curve), b_tracker.animate.set_value(-1), k_tracker.animate.set_value(5), run_time=3)
        self.wait(1)
        
        # 计算与ln(x)的切点
        # 对于y = kx + b与y = ln(x)相切，需要满足：
        # 1) kx + b = ln(x) (相交)
        # 2) k = 1/x (切线斜率相等)
        # 从第二个条件得到 x = 1/k，代入第一个条件：
        # k * (1/k) + b = ln(1/k)
        # 1 + b = -ln(k)
        # 所以 b = -ln(k) - 1
        
        # 动画到相切位置
        self.play(k_tracker.animate.set_value(1), run_time=4)
        
        # 在切点处创建碰撞特效
        touch_point_ln = axes.c2p(1, 0)
        
        # 使用CollisionEffect类创建碰撞特效
        collision_effect_ln = CollisionEffect(touch_point_ln)
        self.add(collision_effect_ln.get_lines())
        
        # 播放碰撞特效
        self.play(collision_effect_ln.get_animation(), run_time=1.0)
        
        # 移除直线
        self.remove(collision_effect_ln.get_lines())
        
        self.wait(3)  # 强调相切效果
        
        # 移除ln曲线，继续其他演示
        self.play(FadeOut(ln_curve), run_time=1)

        self.wait(0.8)
        self.play(FadeOut(parallel_line), FadeOut(y_intercept_point), FadeOut(y_intercept_label), FadeOut(k_slider), FadeOut(b_slider), FadeOut(formula2), run_time=0.5)

        # 场景3：截距式 - 直线随截距变化
        # 清除其他元素
        self.clear()
        self.add(axes)
        
        # 公式显示
        formula3 = MathTex("\\frac{x}{a} + \\frac{y}{b} = 1", font_size=45, color=WHITE)
        formula3.to_corner(UL, buff=0.5)
        self.play(Write(formula3))
        
        # 参数跟踪器
        a_tracker = ValueTracker(2)
        b_tracker = ValueTracker(1.2)
        
        # 滑块
        a_slider = SliderComponent("a", a_tracker, 0.5, 3, [4.5, 2.8, 0])
        b_slider = SliderComponent("b", b_tracker, 0.5, 2, [4.5, 2.2, 0])
        self.play(Create(a_slider), Create(b_slider))
        
        # 使用always_redraw的截距式直线
        def get_intercept_line():
            a = a_tracker.get_value()
            b = b_tracker.get_value()
            if abs(a) < 0.1 or abs(b) < 0.1:
                return axes.plot(lambda x: max(-3, min(3, 0)), x_range=[-0.1, 0.1], color=BLUE, stroke_width=5)
            # 截距式: x/a + y/b = 1 => y = b(1 - x/a)
            def line_func(x):
                y = b * (1 - x/a)
                return max(-3, min(3, y))
            
            # 计算x范围，确保y在[-3,3]内
            # y = b(1 - x/a) = b - bx/a
            # 求解 b - bx/a = ±3
            if abs(b) > 0.001:
                x_at_y3 = a * (1 - 3/b) if b != 0 else a
                x_at_y_minus3 = a * (1 - (-3)/b) if b != 0 else a
                x_min = max(-5, min(x_at_y3, x_at_y_minus3, a))
                x_max = min(5, max(x_at_y3, x_at_y_minus3, 0))
            else:
                x_min, x_max = 0, a
                
            return axes.plot(line_func, x_range=[x_min, x_max], color=BLUE, stroke_width=5)
        
        intercept_line = always_redraw(get_intercept_line)
        
        # x轴截距点
        def get_x_intercept_point():
            return Dot(axes.c2p(a_tracker.get_value(), 0), color=YELLOW, radius=0.06)
        
        x_intercept_point = always_redraw(get_x_intercept_point)
        
        # y轴截距点
        def get_y_intercept_point():
            return Dot(axes.c2p(0, b_tracker.get_value()), color=YELLOW, radius=0.06)
        
        y_intercept_point = always_redraw(get_y_intercept_point)
        
        # x轴截距标签
        def get_x_intercept_label():
            a = a_tracker.get_value()
            label = MathTex("(a, 0)", font_size=40, color=YELLOW)
            label.next_to(axes.c2p(a, 0), DOWN, buff=0.1)
            return label
        
        x_intercept_label = always_redraw(get_x_intercept_label)
        
        # y轴截距标签
        def get_y_intercept_label():
            b = b_tracker.get_value()
            label = MathTex("(0, b)", font_size=40, color=YELLOW)
            label.next_to(axes.c2p(0, b), RIGHT, buff=0.1)
            return label
        
        y_intercept_label = always_redraw(get_y_intercept_label)
        
        self.play(Create(intercept_line), Create(x_intercept_point), Create(y_intercept_point), 
                  Create(x_intercept_label), Create(y_intercept_label), run_time=0.5)
        
        # 参数变化 - 截距式核心演示 (总共约45秒)
        # 展示x截距快速变化
        self.play(a_tracker.animate.set_value(3), run_time=3)
        self.play(a_tracker.animate.set_value(0.5), run_time=3)
        self.play(a_tracker.animate.set_value(2.5), run_time=3)
        self.play(a_tracker.animate.set_value(1), run_time=3)
        
        # 展示y截距快速变化
        self.play(b_tracker.animate.set_value(0.5), run_time=3)
        self.play(b_tracker.animate.set_value(2), run_time=3)
        self.play(b_tracker.animate.set_value(0.8), run_time=3)
        self.play(b_tracker.animate.set_value(1.8), run_time=3)
        
        # 综合快速变化
        self.play(a_tracker.animate.set_value(0.8), b_tracker.animate.set_value(0.6), run_time=3)
        self.play(a_tracker.animate.set_value(2.8), b_tracker.animate.set_value(1.8), run_time=3)
        self.play(a_tracker.animate.set_value(2), b_tracker.animate.set_value(1.2), run_time=6)
        
        self.wait(0.8)
        self.play(FadeOut(intercept_line), FadeOut(x_intercept_point), FadeOut(y_intercept_point), 
                  FadeOut(x_intercept_label), FadeOut(y_intercept_label), FadeOut(a_slider), FadeOut(b_slider), FadeOut(formula3), run_time=0.5)
        
        # 场景4：一般式的复杂变化
        # 清除其他元素
        self.clear()
        self.add(axes)
        
        # 公式显示
        formula4 = MathTex("Ax + By + C = 0", font_size=45, color=WHITE)
        formula4.to_corner(UL, buff=0.5)
        self.play(Write(formula4))
        
        # 参数跟踪器
        A_tracker = ValueTracker(1)
        B_tracker = ValueTracker(1)
        C_tracker = ValueTracker(0)
        
        # 滑块
        A_slider = SliderComponent("A", A_tracker, 0.2, 2, [4.2, 2.8, 0])
        B_slider = SliderComponent("B", B_tracker, 0.2, 2, [4.2, 2.4, 0])
        C_slider = SliderComponent("C", C_tracker, -1.5, 1.5, [4.2, 2.0, 0])
        self.play(Create(A_slider), Create(B_slider), Create(C_slider))
        
        # 使用always_redraw的一般式直线
        def get_general_line():
            A = A_tracker.get_value()
            B = B_tracker.get_value()
            C = C_tracker.get_value()
            if abs(B) < 0.01:
                B = 0.01
            # 一般式: Ax + By + C = 0 => y = -(A/B)x - C/B
            def line_func(x):
                y = -(A/B)*x - C/B
                return max(-3, min(3, y))
            
            # 计算x范围，确保y在[-3,3]内
            # y = -(A/B)x - C/B
            # 求解 -(A/B)x - C/B = ±3
            slope = -A/B
            intercept = -C/B
            if abs(slope) > 0.001:
                x_at_y3 = (3 - intercept) / slope
                x_at_y_minus3 = (-3 - intercept) / slope
                x_min = max(-4.8, min(x_at_y3, x_at_y_minus3))
                x_max = min(4.8, max(x_at_y3, x_at_y_minus3))
            else:
                x_min, x_max = -4.8, 4.8
                
            return axes.plot(line_func, x_range=[x_min, x_max], color=BLUE, stroke_width=5)
        
        general_line = always_redraw(get_general_line)
        
        # 标记x轴截距点（当y=0时）
        def get_x_intercept_general():
            A = A_tracker.get_value()
            C = C_tracker.get_value()
            if abs(A) > 0.01:
                x_intercept = -C/A
                if abs(x_intercept) <= 5:
                    return Dot(axes.c2p(x_intercept, 0), color=YELLOW, radius=0.06)
            return Dot(ORIGIN, color=YELLOW, radius=0, fill_opacity=0)
        
        x_intercept_general = always_redraw(get_x_intercept_general)
        
        # x轴截距标签
        def get_x_intercept_general_label():
            A = A_tracker.get_value()
            C = C_tracker.get_value()
            if abs(A) > 0.01:
                x_intercept = -C/A
                if abs(x_intercept) <= 5:
                    label = MathTex("(-\\frac{C}{A}, 0)", font_size=30, color=YELLOW)
                    label.next_to(axes.c2p(x_intercept, 0), DOWN, buff=0.1)
                    return label
            return MathTex("", font_size=18, color=YELLOW)
        
        x_intercept_general_label = always_redraw(get_x_intercept_general_label)
        
        # 标记y轴截距点（当x=0时）
        def get_y_intercept_general():
            B = B_tracker.get_value()
            C = C_tracker.get_value()
            if abs(B) > 0.01:
                y_intercept = -C/B
                if abs(y_intercept) <= 3:
                    return Dot(axes.c2p(0, y_intercept), color=YELLOW, radius=0.06)
            return Dot(ORIGIN, color=YELLOW, radius=0, fill_opacity=0)
        
        y_intercept_general = always_redraw(get_y_intercept_general)
        
        # y轴截距标签
        def get_y_intercept_general_label():
            B = B_tracker.get_value()
            C = C_tracker.get_value()
            if abs(B) > 0.01:
                y_intercept = -C/B
                if abs(y_intercept) <= 3:
                    label = MathTex("(0, -\\frac{C}{B})", font_size=30, color=YELLOW)
                    label.next_to(axes.c2p(0, y_intercept), RIGHT, buff=0.1)
                    return label
            return MathTex("", font_size=18, color=YELLOW)
        
        y_intercept_general_label = always_redraw(get_y_intercept_general_label)
        
        self.play(Create(general_line), Create(x_intercept_general), Create(y_intercept_general),
                  Create(x_intercept_general_label), Create(y_intercept_general_label), run_time=0.5)
        
        # 参数变化 - 一般式核心演示 (总共约38秒)
        # 展示A参数快速变化
        self.play(A_tracker.animate.set_value(2), run_time=2)
        self.play(A_tracker.animate.set_value(0.2), run_time=2)
        self.play(A_tracker.animate.set_value(1.8), run_time=2)
        
        # 展示B参数快速变化  
        self.play(B_tracker.animate.set_value(0.5), run_time=2)
        self.play(B_tracker.animate.set_value(2), run_time=2)
        self.play(B_tracker.animate.set_value(0.3), run_time=2)
        
        # 展示C参数快速变化
        self.play(C_tracker.animate.set_value(1.5), run_time=2)
        self.play(C_tracker.animate.set_value(-1.5), run_time=2)
        self.play(C_tracker.animate.set_value(1), run_time=2)
        self.play(C_tracker.animate.set_value(-1), run_time=2)
        
        # 综合快速变化
        self.play(A_tracker.animate.set_value(0.5), B_tracker.animate.set_value(1.5), C_tracker.animate.set_value(0.8), run_time=3)
        self.play(A_tracker.animate.set_value(1.8), B_tracker.animate.set_value(0.4), C_tracker.animate.set_value(-0.8), run_time=3)
        
        # 复位
        self.play(A_tracker.animate.set_value(1), B_tracker.animate.set_value(1), C_tracker.animate.set_value(0), run_time=2)
        
        self.wait(0.8)
        self.play(FadeOut(general_line), FadeOut(x_intercept_general), FadeOut(y_intercept_general),
                  FadeOut(x_intercept_general_label), FadeOut(y_intercept_general_label),
                  FadeOut(A_slider), FadeOut(B_slider), FadeOut(C_slider), FadeOut(formula4), run_time=0.5)
        
        # 场景5：两点式 - 通过两点确定直线
        # 清除其他元素
        self.clear()
        self.add(axes)
        
        # 公式显示
        formula5 = MathTex("\\frac{y - y_1}{y_2 - y_1} = \\frac{x - x_1}{x_2 - x_1}", font_size=45, color=WHITE)
        formula5.to_corner(UL, buff=0.5)
        self.play(Write(formula5))
        
        # 参数跟踪器
        x1_tracker = ValueTracker(-1.5)
        y1_tracker = ValueTracker(-0.8)
        x2_tracker = ValueTracker(1.8)
        y2_tracker = ValueTracker(1.2)
        
        # 四个滑块
        x1_slider = SliderComponent("x_1", x1_tracker, -2.5, 2.5, [4.2, 2.8, 0])
        y1_slider = SliderComponent("y_1", y1_tracker, -1.8, 1.8, [4.2, 2.4, 0])
        x2_slider = SliderComponent("x_2", x2_tracker, -2.5, 2.5, [4.2, 2.0, 0])
        y2_slider = SliderComponent("y_2", y2_tracker, -1.8, 1.8, [4.2, 1.6, 0])
        self.play(Create(x1_slider), Create(y1_slider), Create(x2_slider), Create(y2_slider))
        
        # 使用always_redraw的两点式直线
        def get_two_point_line():
            x1 = x1_tracker.get_value()
            y1 = y1_tracker.get_value()
            x2 = x2_tracker.get_value()
            y2 = y2_tracker.get_value()
            
            # 避免两点重合
            if abs(x2 - x1) < 0.01 and abs(y2 - y1) < 0.01:
                def const_line_func(x):
                    return max(-3, min(3, y1))
                return axes.plot(const_line_func, x_range=[-4.8, 4.8], color=BLUE, stroke_width=5)
            elif abs(x2 - x1) < 0.01:  # 垂直线
                return Line(axes.c2p(x1, -3), axes.c2p(x1, 3), color=BLUE, stroke_width=5)
            else:  # 一般情况
                slope = (y2 - y1) / (x2 - x1)
                def line_func(x):
                    y = y1 + slope * (x - x1)
                    return max(-3, min(3, y))
                
                # 计算x范围，确保y在[-3,3]内
                if abs(slope) > 0.001:
                    x_at_y3 = (3 - y1) / slope + x1
                    x_at_y_minus3 = (-3 - y1) / slope + x1
                    x_min = max(-4.8, min(x_at_y3, x_at_y_minus3))
                    x_max = min(4.8, max(x_at_y3, x_at_y_minus3))
                else:
                    x_min, x_max = -4.8, 4.8
                    
                return axes.plot(line_func, x_range=[x_min, x_max], color=BLUE, stroke_width=5)
        
        two_point_line = always_redraw(get_two_point_line)
        
        # 第一个点
        def get_point1():
            return Dot(axes.c2p(x1_tracker.get_value(), y1_tracker.get_value()), color=YELLOW, radius=0.08)
        
        point1 = always_redraw(get_point1)
        
        # 第二个点
        def get_point2():
            return Dot(axes.c2p(x2_tracker.get_value(), y2_tracker.get_value()), color=YELLOW, radius=0.08)
        
        point2 = always_redraw(get_point2)
        
        # 第一个点标签
        def get_point1_label():
            x1 = x1_tracker.get_value()
            y1 = y1_tracker.get_value()
            label = MathTex("(x_1, y_1)", font_size=40, color=YELLOW)
            label.next_to(axes.c2p(x1, y1), DL, buff=0.1)
            return label
        
        point1_label = always_redraw(get_point1_label)
        
        # 第二个点标签
        def get_point2_label():
            x2 = x2_tracker.get_value()
            y2 = y2_tracker.get_value()
            label = MathTex("(x_2, y_2)", font_size=40, color=YELLOW)
            label.next_to(axes.c2p(x2, y2), UR, buff=0.1)
            return label
        
        point2_label = always_redraw(get_point2_label)
        
        self.play(Create(two_point_line), Create(point1), Create(point2), 
                  Create(point1_label), Create(point2_label), run_time=0.5)
        
        # 参数变化演示 - 两点式核心演示 (总共约30秒)
        # 快速移动第一个点
        self.play(x1_tracker.animate.set_value(-2), y1_tracker.animate.set_value(1.5), run_time=2)
        self.play(x1_tracker.animate.set_value(0.5), y1_tracker.animate.set_value(-1), run_time=2)
        self.play(x1_tracker.animate.set_value(-1), y1_tracker.animate.set_value(1), run_time=2)
        
        # 快速移动第二个点
        self.play(x2_tracker.animate.set_value(2), y2_tracker.animate.set_value(-1.5), run_time=2)
        self.play(x2_tracker.animate.set_value(-0.5), y2_tracker.animate.set_value(1.5), run_time=2)
        self.play(x2_tracker.animate.set_value(2.2), y2_tracker.animate.set_value(0.8), run_time=2)
        
        # 两点同时快速移动
        self.play(x1_tracker.animate.set_value(-2.2), y1_tracker.animate.set_value(-1.2), 
                  x2_tracker.animate.set_value(0.8), y2_tracker.animate.set_value(-0.5), run_time=3)
        self.play(x1_tracker.animate.set_value(0.2), y1_tracker.animate.set_value(1.5), 
                  x2_tracker.animate.set_value(-1.2), y2_tracker.animate.set_value(-1.8), run_time=3)
        
        # 复位
        self.play(x1_tracker.animate.set_value(-1.5), y1_tracker.animate.set_value(-0.8), 
                  x2_tracker.animate.set_value(1.8), y2_tracker.animate.set_value(1.2), run_time=4)
        
        self.wait(0.8)
        self.play(FadeOut(two_point_line), FadeOut(point1), FadeOut(point2), 
                  FadeOut(point1_label), FadeOut(point2_label), 
                  FadeOut(x1_slider), FadeOut(y1_slider), FadeOut(x2_slider), FadeOut(y2_slider), 
                  FadeOut(formula5), run_time=0.5)
        
        # 最终清理
        self.play(
            FadeOut(axes),
            run_time=0.5
        )
        
        self.wait(0.5) 