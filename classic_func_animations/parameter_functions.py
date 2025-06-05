from manim import *
import numpy as np

class PowerFunction(Scene):
    def construct(self):
        # 创建坐标系 - 两轴尺度完全一致，只显示x正半轴
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": WHITE},
        )
        
        # 创建参数跟踪器
        a_tracker = ValueTracker(-3)
        
        # 左上角函数形式显示
        func_form = MathTex("f(x) = x^a", color=WHITE, font_size=32).to_corner(UL, buff=0.5)
        
        # 创建滑轨（白线）
        slider_line = Line(
            start=ORIGIN, end=2.5*RIGHT, color=WHITE, stroke_width=2
        ).to_corner(UR, buff=0.5)
        
        # 创建滑块（圆形白色）
        slider_dot = Dot(color=WHITE, radius=0.1)
        
        # 创建参数显示
        a_display = MathTex("a = ", color=WHITE, font_size=24).next_to(slider_line, UP, buff=0.2)
        a_value = DecimalNumber(
            -3, num_decimal_places=1, color=WHITE, font_size=24
        ).next_to(a_display, RIGHT, buff=0.1)
        
        # 创建函数图像 - 只在x正半轴
        def power_func(x):
            a = a_tracker.get_value()
            if x <= 0:
                return 0
            try:
                if a == 0:
                    return 1
                elif a < 0:
                    return np.power(x, a) if x > 0 else 0
                else:
                    return np.power(x, a)
            except:
                return 0
        
        graph = always_redraw(
            lambda: axes.plot(
                power_func,
                x_range=[0.1, 5.5],
                color=BLUE_A,
                stroke_width=3,
                dt=0.01
            )
        )

        r_line = axes.plot(
            lambda x: x,
            x_range=[0, 6],
            color=GREEN_A,
            stroke_width=1
        )

        zero_dot = Dot(color=GREEN_A, radius=0.1).move_to(axes.c2p(0, 0))
        one_dot = Dot(color=GREEN_A, radius=0.1).move_to(axes.c2p(1, 1))
        
        # 更新滑块位置
        def update_slider():
            a = a_tracker.get_value()
            progress = (a - (-3)) / (6 - (-3))
            slider_dot.move_to(
                slider_line.get_left() + progress * (slider_line.get_right() - slider_line.get_left())
            )
        
        slider_dot.add_updater(lambda m: update_slider())
        a_value.add_updater(lambda m: m.set_value(a_tracker.get_value()))
        
        # 添加所有对象
        self.add(axes, func_form, slider_line, slider_dot, a_display, a_value, graph, zero_dot, one_dot, r_line)
        
        # 动画：a从-3变化到7
        self.play(
            a_tracker.animate.set_value(6),
            run_time=60,
            rate_func=linear
        )

class ExponentialFunction(Scene):
    def construct(self):
        # 创建坐标系
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1, 6, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": WHITE},
        )
        
        # 创建参数跟踪器
        t_tracker = ValueTracker(-1)
        
        # 左上角函数形式显示
        func_form = MathTex("f(x) = a^x", color=WHITE, font_size=32).to_corner(UL, buff=0.5)
        
        # 创建滑轨（白线）
        slider_line = Line(
            start=ORIGIN, end=2.5*RIGHT, color=WHITE, stroke_width=2
        ).to_corner(UR, buff=0.5)
        
        # 创建滑块（圆形白色）
        slider_dot = Dot(color=WHITE, radius=0.1)
        
        # 创建参数显示
        a_display = MathTex("a = ", color=WHITE, font_size=24).next_to(slider_line, UP, buff=0.2)
        a_value = DecimalNumber(
            10**t_tracker.get_value(), num_decimal_places=1, color=WHITE, font_size=24
        ).next_to(a_display, RIGHT, buff=0.1)
        
        # 创建函数图像
        def exp_func(x):
            a = 10**t_tracker.get_value()
            try:
                return np.power(a, x)
            except:
                return 0
        
        graph = always_redraw(
            lambda: axes.plot(
                exp_func,
                x_range=[-4, 4],
                color=BLUE_A,
                stroke_width=3,
                dt=0.01
            )
        )

        v_line = Line(
            start=axes.c2p(1, 0),
            end=axes.c2p(1, 10),
            color=GREEN_A,
            stroke_width=1
        )

        zero_dot = Dot(color=GREEN_A, radius=0.1).move_to(axes.c2p(0, 1))
        one_dot = always_redraw(lambda: Dot(color=GREEN_A, radius=0.1).move_to(axes.c2p(1, exp_func(1))))
        
        # 更新滑块位置
        def update_slider():
            t = t_tracker.get_value()
            # 将a从[1.5, 3]映射到滑块位置
            progress = (t - (-1)) / (1 - (-1))
            slider_dot.move_to(
                slider_line.get_left() + progress * (slider_line.get_right() - slider_line.get_left())
            )
        
        slider_dot.add_updater(lambda m: update_slider())
        a_value.add_updater(lambda m: m.set_value(10**t_tracker.get_value()))
        
        # 添加所有对象
        self.add(axes, func_form, slider_line, slider_dot, a_display, a_value, graph, v_line, zero_dot, one_dot)
        
        # 动画：a从1.5变化到3
        self.play(
            t_tracker.animate.set_value(1),
            run_time=60,
            rate_func=linear
        )

class LogarithmicFunction(Scene):
    def construct(self):
        # 创建坐标系
        axes = Axes(
            x_range=[-1, 8, 1],
            y_range=[-3, 3, 1],
            x_length=9,
            y_length=6,
            axis_config={"color": WHITE},
        )
        
        # 创建参数跟踪器
        t_tracker = ValueTracker(-1)
        
        # 左上角函数形式显示
        func_form = MathTex("f(x) = \\log_a x", color=WHITE, font_size=32).to_corner(UL, buff=0.5)
        
        # 创建滑轨（白线）
        slider_line = Line(
            start=ORIGIN, end=2.5*RIGHT, color=WHITE, stroke_width=2
        ).to_corner(UR, buff=0.5)
        
        # 创建滑块（圆形白色）
        slider_dot = Dot(color=WHITE, radius=0.1)
        
        # 创建参数显示
        a_display = MathTex("a = ", color=WHITE, font_size=24).next_to(slider_line, UP, buff=0.2)
        a_value = DecimalNumber(
            10**t_tracker.get_value(), num_decimal_places=1, color=WHITE, font_size=24
        ).next_to(a_display, RIGHT, buff=0.1)
        
        # 创建函数图像
        def log_func(x):
            a = 10**t_tracker.get_value()
            if x <= 0 or a <= 0 or a == 1:
                return 0
            try:
                return np.log(x) / np.log(a)
            except:
                return 0
        
        graph = always_redraw(
            lambda: axes.plot(
                log_func,
                x_range=[0.1, 10],
                color=BLUE_A,
                stroke_width=3,
                dt=0.01
            )
        )        

        h_line = axes.plot(
            lambda x: 1,
            x_range=[-1, 10],
            color=GREEN_A,
            stroke_width=1
        )

        zero_dot = always_redraw(lambda: Dot(color=GREEN_A, radius=0.1).move_to(axes.c2p(1, 0)))
        one_dot = always_redraw(lambda: Dot(color=GREEN_A, radius=0.1).move_to(axes.c2p(10**t_tracker.get_value(), 1)))
        
        # 更新滑块位置
        def update_slider():
            t = t_tracker.get_value()
            # 将a从[1.5, 5]映射到滑块位置
            progress = (t - (-1)) / (1 - (-1))
            slider_dot.move_to(
                slider_line.get_left() + progress * (slider_line.get_right() - slider_line.get_left())
            )
        
        slider_dot.add_updater(lambda m: update_slider())
        a_value.add_updater(lambda m: m.set_value(10**t_tracker.get_value()))
        
        # 添加所有对象
        self.add(axes, func_form, slider_line, slider_dot, a_display, a_value, graph, h_line, zero_dot, one_dot)
        
        # 动画：a从1.5变化到5
        self.play(
            t_tracker.animate.set_value(1),
            run_time=60,
            rate_func=linear
        )

class TrigonometricFunction(Scene):
    def construct(self):
        # 创建坐标系
        axes = Axes(
            x_range=[-8, 8, 2],
            y_range=[-4, 4, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": WHITE},
        )
        
        # 创建参数跟踪器
        A_tracker = ValueTracker(1)      # 振幅
        omega_tracker = ValueTracker(1)  # 角频率
        phi_tracker = ValueTracker(0)    # 相位
        
        # 左上角函数形式显示
        func_form = MathTex("f(x) = A \\sin(\\omega x + \\varphi)", color=WHITE, font_size=28).to_corner(UL, buff=0.5)
        
        # 创建三个滑轨（白线）- 垂直排列
        slider_line_A = Line(
            start=ORIGIN, end=2*RIGHT, color=WHITE, stroke_width=2
        ).to_corner(UR, buff=0.5)
        
        slider_line_omega = Line(
            start=ORIGIN, end=2*RIGHT, color=WHITE, stroke_width=2
        ).next_to(slider_line_A, DOWN, buff=0.8)
        
        slider_line_phi = Line(
            start=ORIGIN, end=2*RIGHT, color=WHITE, stroke_width=2
        ).next_to(slider_line_omega, DOWN, buff=0.8)
        
        # 创建三个滑块（圆形白色）
        slider_dot_A = Dot(color=WHITE, radius=0.08)
        slider_dot_omega = Dot(color=WHITE, radius=0.08)
        slider_dot_phi = Dot(color=WHITE, radius=0.08)
        
        # 创建参数显示
        A_display = MathTex("A = ", color=WHITE, font_size=20).next_to(slider_line_A, LEFT, buff=0.3)
        A_value = DecimalNumber(
            1, num_decimal_places=1, color=WHITE, font_size=20
        ).next_to(A_display, RIGHT, buff=0.1)
        
        omega_display = MathTex("\\omega = ", color=WHITE, font_size=20).next_to(slider_line_omega, LEFT, buff=0.3)
        omega_value = DecimalNumber(
            1, num_decimal_places=1, color=WHITE, font_size=20
        ).next_to(omega_display, RIGHT, buff=0.1)
        
        phi_display = MathTex("\\varphi = ", color=WHITE, font_size=20).next_to(slider_line_phi, LEFT, buff=0.3)
        phi_value = DecimalNumber(
            0, num_decimal_places=1, color=WHITE, font_size=20
        ).next_to(phi_display, RIGHT, buff=0.1)
        
        # 创建函数图像
        def trig_func(x):
            A = A_tracker.get_value()
            omega = omega_tracker.get_value()
            phi = phi_tracker.get_value()
            try:
                return A * np.sin(omega * x + phi)
            except:
                return 0
        
        graph = always_redraw(
            lambda: axes.plot(
                trig_func,
                x_range=[-8, 8],
                color=BLUE_A,
                stroke_width=3,
                dt=0.01
            )
        )
        
        # 参考线
        x_axis_line = axes.plot(
            lambda x: 0,
            x_range=[-8, 8],
            color=GREEN_A,
            stroke_width=1
        )
        
        # 更新滑块位置
        def update_slider_A():
            A = A_tracker.get_value()
            progress = (A - 0.5) / (3 - 0.5)
            slider_dot_A.move_to(
                slider_line_A.get_left() + progress * (slider_line_A.get_right() - slider_line_A.get_left())
            )
        
        def update_slider_omega():
            omega = omega_tracker.get_value()
            progress = (omega - 0.5) / (3 - 0.5)
            slider_dot_omega.move_to(
                slider_line_omega.get_left() + progress * (slider_line_omega.get_right() - slider_line_omega.get_left())
            )
        
        def update_slider_phi():
            phi = phi_tracker.get_value()
            progress = phi / (2 * np.pi)
            slider_dot_phi.move_to(
                slider_line_phi.get_left() + progress * (slider_line_phi.get_right() - slider_line_phi.get_left())
            )
        
        slider_dot_A.add_updater(lambda m: update_slider_A())
        slider_dot_omega.add_updater(lambda m: update_slider_omega())
        slider_dot_phi.add_updater(lambda m: update_slider_phi())
        
        A_value.add_updater(lambda m: m.set_value(A_tracker.get_value()))
        omega_value.add_updater(lambda m: m.set_value(omega_tracker.get_value()))
        phi_value.add_updater(lambda m: m.set_value(phi_tracker.get_value()))
        
        # 添加所有对象
        self.add(
            axes, func_form, 
            slider_line_A, slider_line_omega, slider_line_phi,
            slider_dot_A, slider_dot_omega, slider_dot_phi,
            A_display, A_value, omega_display, omega_value, phi_display, phi_value,
            graph, x_axis_line
        )
        
        # 动画序列：先变A，再变ω，最后变φ
        self.play(
            A_tracker.animate.set_value(3),
            run_time=20,
            rate_func=smooth
        )
        self.play(
            omega_tracker.animate.set_value(3),
            run_time=20,
            rate_func=smooth
        )
        self.play(
            phi_tracker.animate.set_value(2 * np.pi),
            run_time=20,
            rate_func=smooth
        )
        
        # 三个快速的美观变化，三个参数同时变化
        
        # 第一个变化：小振幅高频率 - 紧密波动
        self.play(
            A_tracker.animate.set_value(1),
            omega_tracker.animate.set_value(2.5),
            phi_tracker.animate.set_value(np.pi/4),
            run_time=3,
            rate_func=smooth
        )
        
        # 第二个变化：大振幅低频率 - 舒缓大波
        self.play(
            A_tracker.animate.set_value(2.5),
            omega_tracker.animate.set_value(0.8),
            phi_tracker.animate.set_value(np.pi),
            run_time=3,
            rate_func=smooth
        )
        
        # 第三个变化：中等振幅中等频率 - 平衡波形
        self.play(
            A_tracker.animate.set_value(1.8),
            omega_tracker.animate.set_value(1.5),
            phi_tracker.animate.set_value(3*np.pi/2),
            run_time=3,
            rate_func=smooth
        ) 