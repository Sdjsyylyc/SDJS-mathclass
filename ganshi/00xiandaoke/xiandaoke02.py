from manim import *
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules import SliderComponent, CustomAxes, CollisionEffect

class Xiandaoke02(Scene):
    def construct(self):
                # 创建分段的数学公式，将需要标记的部分单独分离
        func_text = MathTex(
            "f(x) = ", 
            "e^{x} \\cdot (2x-1)", 
            " - ", 
            "a(x-1)",
            font_size=54
        )
        
        # 标记两个重要部分以便后续变色
        self.part1 = func_text[1]  # e^{x} \cdot (2x-1) 部分
        self.part2 = func_text[3]  # a(x-1) 部分
        
        # 将函数文本放置在画面正上方
        func_text.to_edge(UP, buff=0.5)
        
        # 显示函数文本
        self.play(Write(func_text), run_time=2)
        self.wait(2)
        
        # 创建自定义坐标系
        axes = CustomAxes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": WHITE, "stroke_width": 2, "tip_length": 0.2},
        )
        axes.shift(DOWN * 0.5)  # 向下移动以给题目留出空间
        self.play(Create(axes), run_time=0.2)
        self.wait(2)
        
        # 让第一部分函数闪烁2次，提示即将绘制这部分图像
        for _ in range(2):
            self.play(self.part1.animate.set_color(BLUE), run_time=0.3)
            self.play(self.part1.animate.set_color(WHITE), run_time=0.3)
            self.play(self.part1.animate.set_color(BLUE), run_time=0.3)
        self.wait(0.5)
        
        
        # 创建函数图像
        func_graph = axes.plot(lambda x: np.exp(x) * (2*x-1), x_range=[-4, 4], color=BLUE)
        self.play(Create(func_graph), run_time=2)
        self.wait(2)
        
        # 使用倾斜角参数 theta 来控制斜率 a = tan(theta)
        theta_tracker = ValueTracker(PI/3)  # 初始角度60度
        
        def get_rotating_line():
            theta = theta_tracker.get_value()
            a = np.tan(theta)  # 斜率 = tan(倾斜角)
            # 直线方程：y = a(x-1)  (通过定点(1,0))
            return axes.plot(lambda x: a * (x-1), x_range=[-3, 3], color=YELLOW)
        
        # 让第二部分函数闪烁，提示即将绘制直线
        for _ in range(2):
            self.play(self.part2.animate.set_color(YELLOW), run_time=0.3)
            self.play(self.part2.animate.set_color(WHITE), run_time=0.3)
            self.play(self.part2.animate.set_color(YELLOW), run_time=0.3)
        self.wait(0.5)
         
        
        # 创建初始的旋转直线
        rotating_line = always_redraw(get_rotating_line)
        
        # 显示旋转直线
        self.play(Create(rotating_line), run_time=1)
        self.wait(0.5)
        
        # 计算两函数交点
        from scipy.optimize import fsolve
        
        def find_all_intersections():
            theta = theta_tracker.get_value()
            a = np.tan(theta)
            
            # 定义方程：e^x * (2x-1) - a(x-1) = 0
            def equation(x):
                return np.exp(x) * (2*x - 1) - a * (x - 1)
            
            try:
                # 尝试在更多的初始猜测点求解
                solutions = []
                # 扩大搜索范围，使用更多初始点
                initial_guesses = [-4, -3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3, 4]
                
                for initial_guess in initial_guesses:
                    try:
                        sol = fsolve(equation, initial_guess)[0]
                        # 验证解的有效性且在可视范围内
                        if abs(equation(sol)) < 1e-6 and -4 <= sol <= 4:
                            solutions.append(sol)
                    except:
                        continue
                
                # 去重：只保留距离大于0.01的解
                unique_solutions = []
                for sol in solutions:
                    is_unique = True
                    for existing_sol in unique_solutions:
                        if abs(sol - existing_sol) < 0.01:
                            is_unique = False
                            break
                    if is_unique:
                        unique_solutions.append(sol)
                
                # 返回所有有效的唯一解
                valid_intersections = []
                for x_intersect in unique_solutions:
                    y_intersect = np.exp(x_intersect) * (2*x_intersect - 1)
                    # 检查y值是否在可视范围内
                    if -3 <= y_intersect <= 3:
                        valid_intersections.append((x_intersect, y_intersect))
                
                return valid_intersections if valid_intersections else []
            except:
                return []
        
        # 创建动态交点组
        def get_intersection_dots():
            intersections = find_all_intersections()
            dots = VGroup()
            
            for i, (x_int, y_int) in enumerate(intersections):
                # 为不同的交点使用不同的颜色
                colors = [RED, ORANGE, PURPLE, GREEN, PINK]
                color = colors[i % len(colors)]
                
                dot = Dot(color=color, radius=0.1)
                dot.move_to(axes.c2p(x_int, y_int))
                dots.add(dot)
            
            return dots
        
        intersection_dots = always_redraw(get_intersection_dots)
        
        # 显示交点
        self.play(Create(intersection_dots), run_time=0.5)
        self.wait(0.5)
        
        # 创建斜率滑块显示器
        # 滑块轨道 - 位置在右上角
        slider_track = Line(LEFT * 0.5, RIGHT * 0.5, color=WHITE, stroke_width=3)
        slider_track.move_to(UR * 2.5 + RIGHT * 2.5)  # 右上角位置
        
        # 滑块标签
        slider_label = MathTex("a", font_size=54, color=WHITE)
        slider_label.next_to(slider_track, UP, buff=0.3)
        
        
        
        # 使用对数映射函数来将斜率映射到滑块位置
        def slope_to_position(slope):
            # 使用arctan函数将无穷范围映射到有限范围 [-π/2, π/2]
            # 然后缩放到滑块轨道长度
            normalized = np.arctan(slope) / (PI/2)  # 范围 [-1, 1]
            return normalized * 0.5  # 滑块轨道半长度是0.5
        
        # 创建动态滑块圆点
        def get_slider_dot():
            theta = theta_tracker.get_value()
            a = np.tan(theta)
            pos_x = slope_to_position(a)
            dot = Dot(color=YELLOW, radius=0.08)
            dot.move_to(slider_track.get_center() + RIGHT * pos_x)
            return dot
        
        slider_dot = always_redraw(get_slider_dot)
        
        # 显示滑块组件
        slider_group = VGroup(slider_track, slider_label)
        self.play(
            Create(slider_track),
            Create(slider_dot),
            Write(slider_label),
            run_time=1
        )
        self.wait(0.5)
        
        
        # 添加旋转动画 - 让直线从60度旋转到不同角度
        self.play(
            theta_tracker.animate.set_value(5*PI/6),  # 150度
            run_time=2,
            rate_func=smooth
        )
        self.wait(1)

        self.play(
            theta_tracker.animate.set_value(0.15*PI/2),  # 90度
            run_time=2,
            rate_func=smooth
        )
        self.wait(1)
        