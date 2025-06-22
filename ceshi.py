from manim import *
import numpy as np
from modules import SliderComponent, CustomAxes, CollisionEffect

class ElectricPotentialVisualization(ThreeDScene):
    def construct(self):
        # 设置相机
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1], 
            z_range=[-2, 2, 0.5],
            x_length=8,
            y_length=8,
            z_length=4,
            axis_config={"color": GRAY}
        )
        
        # 定义电势函数 - 类似双极子的电势分布
        def potential_function(x, y):
            # 两个点电荷的位置
            charge1_pos = np.array([1.5, 0])
            charge2_pos = np.array([-1.5, 0])
            
            # 计算到两个电荷的距离
            r1 = np.sqrt((x - charge1_pos[0])**2 + (y - charge1_pos[1])**2 + 0.1)
            r2 = np.sqrt((x - charge2_pos[0])**2 + (y - charge2_pos[1])**2 + 0.1)
            
            # 电势：正电荷和负电荷
            potential = 2/r1 - 2/r2
            
            # 限制幅度
            return np.clip(potential, -3, 3)
        
        # 创建网格平面
        grid_plane = NumberPlane(
            x_range=[-4, 4, 0.5],
            y_range=[-4, 4, 0.5],
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            }
        ).rotate(PI/2, axis=RIGHT).shift(DOWN * 2)
        
        # 创建3D表面
        surface = Surface(
            lambda u, v: np.array([
                u, v, potential_function(u, v) * 0.3
            ]),
            u_range=[-3.5, 3.5],
            v_range=[-3.5, 3.5],
            resolution=(40, 40),
            stroke_width=0.5,
            fill_opacity=0.8,
            checkerboard_colors=[RED_D, ORANGE, YELLOW, GREEN_D, BLUE_D, PURPLE_D]
        )
        
        # 为表面添加渐变色
        surface.set_fill_by_checkerboard(RED_E, BLUE_E, opacity=0.7)
        surface.set_stroke(color=WHITE, width=0.2, opacity=0.5)
        
        # 创建等势线
        contours = VGroup()
        levels = [-2, -1, 0, 1, 2]
        colors = [BLUE, BLUE_C, GREEN, RED_C, RED]
        
        for level, color in zip(levels, colors):
            contour_points = []
            for i in range(100):
                for j in range(100):
                    x = -3.5 + i * 7/99
                    y = -3.5 + j * 7/99
                    z = potential_function(x, y) * 0.3
                    
                    if abs(z - level * 0.3) < 0.1:
                        contour_points.append([x, y, -2])
            
            if contour_points:
                # 简化等势线绘制
                for i in range(0, len(contour_points), 5):
                    if i + 4 < len(contour_points):
                        line = Line(
                            contour_points[i],
                            contour_points[i+4],
                            color=color,
                            stroke_width=2
                        )
                        contours.add(line)
        
        # 添加标题
        title = Text("电势图像 Electric Potential", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        
        # 添加公式
        formula = MathTex(
            r"\Phi(x,y) = \frac{kQ_+}{r_+} + \frac{kQ_-}{r_-}",
            font_size=28,
            color=YELLOW
        )
        formula.to_edge(UR)
        self.add_fixed_in_frame_mobjects(formula)
        
        # 创建点电荷标记
        charge_positive = Sphere(radius=0.1, color=RED).move_to([1.5, 0, 0])
        charge_negative = Sphere(radius=0.1, color=BLUE).move_to([-1.5, 0, 0])
        
        # 电荷标签
        plus_label = MathTex("+", color=RED, font_size=24).move_to([1.5, 0, 0.3])
        minus_label = MathTex("-", color=BLUE, font_size=24).move_to([-1.5, 0, 0.3])
        
        # 动画序列
        self.play(
            Create(axes),
            Write(title),
            run_time=2
        )
        
        self.play(
            Create(grid_plane),
            run_time=1.5
        )
        
        self.play(
            Create(surface),
            run_time=3
        )
        
        self.play(
            Create(contours),
            Create(charge_positive),
            Create(charge_negative),
            Write(plus_label),
            Write(minus_label),
            Write(formula),
            run_time=2
        )
        
        # 丝滑的相机旋转动画
        self.play(
            Rotate(
                VGroup(axes, surface, grid_plane, contours, charge_positive, charge_negative),
                angle=PI/4,
                axis=UP,
                run_time=3
            )
        )
        
        # 相机视角变化
        self.move_camera(phi=60 * DEGREES, theta=60 * DEGREES, run_time=3)
        
        # 再次旋转
        self.play(
            Rotate(
                VGroup(axes, surface, grid_plane, contours, charge_positive, charge_negative),
                angle=PI/2,
                axis=OUT,
                run_time=4
            )
        )
        
        # 最终相机位置
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, run_time=2)
        
        # 表面动画 - 振动效果
        def surface_wave(mob, dt):
            t = self.renderer.time
            for i, point in enumerate(mob.points):
                if i % 4 == 0:  # 只修改部分点以提高性能
                    x, y, z = point
                    new_z = z + 0.05 * np.sin(2 * t + x + y)
                    mob.points[i] = np.array([x, y, new_z])
        
        # surface.add_updater(surface_wave)
        
        self.wait(2)
        
        # 添加说明文字（固定在屏幕上）
        explanation = Text("我们再回过头来看以前学的电势图像", font_size=28, color=WHITE)
        explanation.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(explanation)
        
        self.play(Write(explanation), run_time=2)
        self.wait(3)

if __name__ == "__main__":
    # 运行动画
    pass
