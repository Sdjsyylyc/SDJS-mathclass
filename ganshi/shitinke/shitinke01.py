from manim import *
import numpy as np
from scipy.optimize import fsolve

class ConicSectionSolution(ThreeDScene):
    def construct(self):
        # 配置3D相机
        self.set_camera_orientation(phi=70*DEGREES, theta=45*DEGREES, zoom=0.8)
        axes = ThreeDAxes()
        self.add(axes)

        # 创建双圆锥（高度范围[-2,2]，半顶角α=45°）
        cone_group = self.create_double_cone()
        self.add(cone_group)
        
        # 创建可移动的切割平面（法向量控制倾角）
        plane = Rectangle(width=5, height=5, fill_opacity=0.3, fill_color=GREY)
        plane.rotate(PI/6, axis=RIGHT).shift(DOWN*3)
        self.add(plane)
        
        # 动态展示平面移动与交线生成
        self.show_dynamic_section(cone_group, plane)

    def create_double_cone(self):
        """创建分离式双圆锥，返回包含上下锥的VGroup"""
        # 上半锥 (z ∈ [0,2])
        upper_cone = Surface(
            lambda u, v: [u*np.cos(v), u*np.sin(v), u],
            u_range=[0, 2], v_range=[0, 2*PI],
            resolution=(20, 50),
            fill_opacity=0.5, 
            stroke_width=0
        ).set_fill(BLUE)
        
        # 下半锥 (z ∈ [-2,0])
        lower_cone = Surface(
            lambda u, v: [abs(u)*np.cos(v), abs(u)*np.sin(v), u],
            u_range=[-2, 0], v_range=[0, 2*PI],
            resolution=(20, 50),
            fill_opacity=0.5,
            stroke_width=0
        ).set_fill(BLUE)
        
        return VGroup(upper_cone, lower_cone)

    def calculate_conic_section(self, plane_normal, plane_point):
        """计算平面与圆锥的交线解析解
        Args:
            plane_normal: 平面法向量 [a,b,c]
            plane_point: 平面上一点 [x0,y0,z0]
        Returns:
            ParametricFunction: 交线的参数方程对象
        """
        a, b, c = plane_normal
        x0, y0, z0 = plane_point
        
        # 核心数学原理：二次曲线统一方程[3,5](@ref)
        # 圆锥方程: x² + y² - z² = 0 (半顶角α=45°时cotα=1)
        # 平面方程: a(x-x0) + b(y-y0) + c(z-z0) = 0
        # 联立得二次曲线: Ax² + Bxy + Cy² + Dx + Ey + F = 0
        
        # 计算平面与轴线夹角β
        cone_axis = np.array([0,0,1])  # 圆锥轴线(Z轴)
        cosβ = abs(np.dot(plane_normal, cone_axis) / (np.linalg.norm(plane_normal) * np.linalg.norm(cone_axis)))
        β = np.arccos(cosβ)
        α = PI/4  # 圆锥半顶角45°
        
        # 根据β与α关系选择曲线类型[4](@ref)
        if abs(β - α) < 0.1:  # 抛物线(β=α)
            # 参数方程: z = t, x = (a²t² + ...), y = (b²t² + ...)
            return self.build_parabola_eq(plane_normal, plane_point)
            
        elif β > α:  # 椭圆(β>α)
            return self.build_ellipse_eq(plane_normal, plane_point)
            
        elif β < α:  # 双曲线(β<α)
            return self.build_hyperbola_eq(plane_normal, plane_point)
            
        else:  # 退化情况（平面过顶点）
            return self.build_triangle_section()

    def build_parabola_eq(self, n, p):
        """生成抛物线参数方程（平面平行于母线）[1](@ref)"""
        a, b, c = n
        return ParametricFunction(
            lambda t: np.array([
                t,  # x
                (b**2 * t**2 - 2*a*c*t - 2*a*p[0]) / (2*b),  # y
                (c**2 * t**2 + 2*a*b*t) / (2*a) + p[2]  # z
            ]),
            t_range=[-2, 2],
            color=RED,
            stroke_width=4
        )

    def build_ellipse_eq(self, n, p):
        """生成椭圆参数方程（平面倾斜较小）[3](@ref)"""
        a, b, c = n
        # 椭圆参数计算（半长轴a_axis, 半短轴b_axis）
        a_axis = 2.0 / abs(c)  # 半长轴与平面高度相关
        b_axis = a_axis * np.sqrt(1 - (np.dot(n, [0,0,1])**2))
        
        return ParametricFunction(
            lambda θ: np.array([
                a_axis * np.cos(θ),  # x
                b_axis * np.sin(θ),  # y
                p[2] + (a*a_axis*np.cos(θ) + b*b_axis*np.sin(θ)) / c  # z
            ]),
            t_range=[0, 2*PI],
            color=GREEN,
            stroke_width=4
        )

    def build_hyperbola_eq(self, n, p):
        """生成双曲线参数方程（平面倾斜较大）[4](@ref)"""
        return ParametricFunction(
            lambda t: np.array([
                np.cosh(t),  # x
                0,  # y（简化计算，假设对称）
                np.sinh(t)  # z
            ]),
            t_range=[-2, 2],
            color=YELLOW,
            stroke_width=4
        )

    def build_triangle_section(self):
        """生成退化三角形（平面过顶点）[4](@ref)"""
        # 返回两条直线段
        line1 = Line(start=[-1.5, -1.5, -2], end=[0,0,0], color=PURPLE, stroke_width=4)
        line2 = Line(start=[1.5, 1.5, -2], end=[0,0,0], color=PURPLE, stroke_width=4)
        return VGroup(line1, line2)

    def show_dynamic_section(self, cone, plane):
        """动态展示平面移动和交线变化"""
        # 初始位置交线
        section = self.calculate_conic_section(
            plane_normal=[0,1,1], 
            plane_point=plane.get_center()
        )
        self.add(section)
        
        # 动画：平面移动并实时更新交线
        for height in np.linspace(-1, 1, 5):
            new_plane = plane.copy().shift(UP * height)
            new_section = self.calculate_conic_section(
                plane_normal=new_plane.get_normal_vector(),
                plane_point=new_plane.get_center()
            )
            
            self.play(
                Transform(plane, new_plane),
                Transform(section, new_section),
                run_time=2,
                rate_func=smooth
            )
            self.wait(0.5)

        # 相机自动旋转展示3D效果
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(3)