from manim import *
import numpy as np

class TriangleAreaScene(Scene):
    def construct(self):
        # 先实现第一问的子动画
        self.solve_part_one()
        self.wait(1)
        
        # 然后实现第二问的主动画
        self.solve_part_two()
    
    def solve_part_one(self):
        # 创建标题 - 纯数学符号
        title = MathTex("(1):\\, B = ?", font_size=48).to_edge(UP+LEFT, buff=0.5)
        
        # 创建箭头 - 水平指向
        arrow = MathTex("\\Rightarrow", font_size=60, color=YELLOW).move_to(RIGHT)
        
        # 创建核心条件 - 放在左侧
        conditions = VGroup(
            MathTex("\\sin C = \\sqrt{2}\\cos B", font_size=36),
            MathTex("a^2 + b^2 - c^2 = \\sqrt{2}ab", font_size=36),
            MathTex("A+B+C=\\pi", font_size=36)
        ).arrange(DOWN, buff=0.3)
        conditions.next_to(arrow, LEFT, buff=0.5)
        
        # 添加大括号
        brace = Brace(conditions, LEFT)
        
        # 结论区域 - 放在右侧，包含三个角度
        results = VGroup(
            MathTex("A = 75^{\\circ}", font_size=40, color=GREEN),
            MathTex("B = 60^{\\circ}", font_size=40, color=YELLOW),
            MathTex("C = 45^{\\circ}", font_size=40, color=BLUE)
        ).arrange(DOWN, buff=0.3)
        results.next_to(arrow, RIGHT, buff=0.5)
        
        # 添加大括号
        brace2 = Brace(results, LEFT)
        
        # 对B角度添加高亮框
        box = SurroundingRectangle(results[1], color=YELLOW, buff=0.2)
        
        # 简化的动画序列
        self.play(Write(title), run_time=0.5)
        self.play(Write(conditions), run_time=1)
        self.play(Create(brace), run_time=0.5)
        self.wait(0.5)
        self.play(Create(arrow), run_time=0.5)
        self.play(Create(brace2), run_time=0.5)
        self.play(Write(results), run_time=1)
        self.play(Create(box), run_time=0.5)
        self.wait(4)
        
        # 淡出所有元素
        all_objects = VGroup(title, conditions, brace, arrow, results, box, brace2)
        self.play(FadeOut(all_objects), run_time=1)
    
    def solve_part_two(self):
        # 设置画面分区 - 左侧2/3为动画区，右侧1/3为公式区
        animation_area = Rectangle(
            width=config.frame_width * 2/3,
            height=config.frame_height,
            stroke_opacity=0,
            fill_opacity=0
        ).to_edge(LEFT, buff=0)
        
        formula_area = Rectangle(
            width=config.frame_width * 1/3,
            height=config.frame_height,
            stroke_opacity=0,
            fill_opacity=0
        ).to_edge(RIGHT, buff=0)
        
        # 创建一个坐标系，方便定位(不会显示)
        axes = Axes(
            x_range=[-4, 4],
            y_range=[-4, 4],
            x_length=7,
            y_length=7,
        ).move_to(animation_area.get_center() + LEFT * 0)
        
        # 初始值设置
        c_length = ValueTracker(3)  # 边c的初始长度，增大初始尺寸
 
        # 创建标题 - 纯数学符号
        title = MathTex("(2):\\, S_{\\triangle ABC} = 3 + \\sqrt{3} \\Rightarrow c = ?", font_size=40).to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)
        
        # 创建一个特定角度的三角形(C=45°, B=60°)
        def create_triangle(c_val):
            # 点C固定在左下位置
            point_C = axes.c2p(-3.5, -3.5)
 
            triangle_scale = 1.5
            
            # 明确定义角度
            angle_C_rad = PI * 45/180  # 45度
            angle_B_rad = PI * 60/180  # 60度
            angle_A_rad = PI - angle_B_rad - angle_C_rad  # 75度
            
            # 计算边长比例 - 使用正弦定理
            sin_A = np.sin(angle_A_rad)
            sin_B = np.sin(angle_B_rad)
            sin_C = np.sin(angle_C_rad)
            
            # 计算边长，确保与c比例正确
            a = c_val * sin_A / sin_C * triangle_scale
            b = c_val * sin_B / sin_C * triangle_scale
            
            # 重新绘制三角形方向以强调角度
            # 让点C在底部，A在右下，B在左上
            
            # 计算向量CA角度 (使其沿水平方向)
            CA_angle = 0  # 水平向右
            
            # 计算点A位置
            point_A = axes.c2p(-3.5 + b * np.cos(CA_angle), 
                             -3.5 + b * np.sin(CA_angle))
            
            # 计算点B位置 - 使用角C和角B来确定
            CB_angle = angle_C_rad  # 角C
            point_B = axes.c2p(-3.5 + a * np.cos(CB_angle), 
                             -3.5 + a * np.sin(CB_angle))
            
            # 绘制三角形
            triangle = Polygon(
                point_A, point_B, point_C,
                color=BLUE_A,
                fill_opacity=0.2,
                stroke_width=2
            )
            
            return triangle, point_A, point_B, point_C
        
        # 动态更新三角形
        triangle = always_redraw(
            lambda: create_triangle(c_length.get_value())[0]
        )
        
        # 动态标记角度和边
        def get_angle_marks():
            _, point_A, point_B, point_C = create_triangle(c_length.get_value())
            
            # 计算角度值
            angle_C_rad = PI * 45/180
            angle_B_rad = PI * 60/180
            angle_A_rad = PI - angle_B_rad - angle_C_rad  # 75度
            
            # 为角C创建角度标记 (45°)
            # 角C由CA和CB两边构成
            angle_C_mark = Arc(
                radius=0.5,
                angle=angle_C_rad,
                color=YELLOW,
                stroke_width=3
            ).move_arc_center_to(point_C)
            
            # 角A由AC和AB构成
            # 计算AB和AC的角度
            AC_angle = np.arctan2(point_C[1] - point_A[1], point_C[0] - point_A[0])
            AB_angle = np.arctan2(point_B[1] - point_A[1], point_B[0] - point_A[0])
            
            # 确保角度是按正确方向测量的
            if AB_angle < AC_angle:
                AB_angle += 2*PI
            
            angle_A_arc = Arc(
                radius=0.5,
                angle=-angle_A_rad,
                color=GREEN,
                stroke_width=3
            ).shift(point_A)
            
            # 旋转到正确位置
            angle_A_arc.rotate(angle=AC_angle, about_point=point_A)
            
            # 角B由BA和BC构成
            # 计算BA和BC的角度
            BA_angle = np.arctan2(point_A[1] - point_B[1], point_A[0] - point_B[0])
            BC_angle = np.arctan2(point_C[1] - point_B[1], point_C[0] - point_B[0])
            
            # 确保角度是按正确方向测量的
            if BC_angle < BA_angle:
                BC_angle += 2*PI
            
            angle_B_arc = Arc(
                radius=0.5,
                angle=-angle_B_rad,
                color=BLUE,
                stroke_width=3
            ).shift(point_B)
            
            # 旋转到正确位置
            angle_B_arc.rotate(angle=BA_angle, about_point=point_B)
            
            return VGroup(angle_C_mark, angle_A_arc, angle_B_arc)
        
        angle_marks = always_redraw(get_angle_marks)
        
        # 动态标注边c
        def get_edge_c():
            _, point_A, point_B, _ = create_triangle(c_length.get_value())
            
            edge_c = Line(point_A, point_B, color=BLUE_B, stroke_width=4)  # 增大线条宽度
            
            # 添加边c的标签
            edge_c_label = MathTex(f"c = {c_length.get_value():.2f}", color=BLUE_B, font_size=48).next_to(  # 增大标签
                edge_c.get_center(),
                UP + RIGHT,
                buff=0.2
            )
            
            return VGroup(edge_c, edge_c_label)
        
        edge_c = always_redraw(get_edge_c)
        
        # 添加角度标签
        def get_angle_labels():
            _, point_A, point_B, point_C = create_triangle(c_length.get_value())
            
            label_A = MathTex("A=75^{\\circ}", color=GREEN, font_size=36).next_to(point_A, DOWN, buff=0.3)
            label_B = MathTex("B=60^{\\circ}", color=BLUE, font_size=36).next_to(point_B, UP + LEFT, buff=0.3)
            label_C = MathTex("C=45^{\\circ}", color=YELLOW, font_size=36).next_to(point_C, DOWN + LEFT, buff=0.3)
            
            return VGroup(label_A, label_B, label_C)
        
        angle_labels = always_redraw(get_angle_labels)
        
        # 计算并显示三角形面积，使用亮度变化来表示强调
        def calculate_area():
            c_val = c_length.get_value()
            
            # 使用海伦公式计算面积
            angle_C = PI * 45/180  # 45度
            angle_B = PI * 60/180  # 60度
            angle_A = PI - angle_B - angle_C  # 75度
            
            # 使用正弦定理计算所有边
            sin_A = np.sin(angle_A)
            sin_B = np.sin(angle_B)
            sin_C = np.sin(angle_C)
            
            a = c_val * sin_A / sin_C
            b = c_val * sin_B / sin_C
            
            # 计算面积 - 使用S = (1/2)ab·sinC公式
            area = 0.5 * a * b * sin_C
            
            # 验证：当c=2√2时，应得到面积S=3+√3
            # 当c=2√2=2.83时，a≈2.17, b≈2.83，代入公式得S≈3+√3≈4.73
            
            # 计算高亮颜色 - 当c值接近目标值时增加亮度
            target_c = 2*np.sqrt(2)
            highlight_intensity = 1 - min(1, abs(c_val - target_c) / 2)
            highlight_color = interpolate_color(WHITE, YELLOW, highlight_intensity)
            
            area_formula = MathTex(
                "S", "=", f"{area:.2f}",
                tex_to_color_map={
                    "S": highlight_color,
                    f"{area:.2f}": highlight_color
                },
                font_size=36
            )
            area_formula.move_to(axes.c2p(3, 3))
            
            return area_formula
        
        area_display = always_redraw(calculate_area)
        
        # 创建右侧的公式说明（全部使用符号）
        formula_title = MathTex("\\triangle ABC:", font_size=36)
        formula_title.to_edge(UP+RIGHT, buff=1.2)
        
        # 条件说明 - 特定角度三角形
        conditions = VGroup(
            MathTex("\\angle C = 45^{\\circ}", font_size=32),
            MathTex("\\angle B = 60^{\\circ}", font_size=32),
            MathTex("\\angle A = 75^{\\circ}", font_size=32)
        ).arrange(DOWN, buff=0.3)
        conditions.next_to(formula_title, DOWN, buff=0.5)
        
        # 面积公式
        area_formula = MathTex(
            "S = \\frac{1}{2}ab\\sin C", 
            font_size=32
        )
        area_formula.next_to(conditions, DOWN, buff=0.6)
        
        # 使用大型MathTex箭头替代DoubleArrow
        arrow1 = MathTex("\\Downarrow", font_size=60, color=YELLOW)
        arrow1.next_to(conditions, DOWN, buff=0.2)
        
        # 题目条件和结论
        problem_condition = MathTex("S = 3 + \\sqrt{3}", font_size=32)
        problem_condition.next_to(area_formula, DOWN, buff=0.6)
        
        solution = MathTex("c = 2\\sqrt{2}", font_size=36, color=YELLOW)
        solution.next_to(problem_condition, DOWN, buff=0.6)
        
        # 使用大型MathTex箭头替代DoubleArrow
        arrow2 = MathTex("\\Downarrow", font_size=60, color=YELLOW)
        arrow2.next_to(problem_condition, DOWN, buff=0.2)
        
        # 高亮显示目标c值和对应面积
        target_c_value = 2*np.sqrt(2)
        
        # 动画序列
        # 1. 显示三角形和标签
        self.play(
            Create(triangle),
            Create(angle_marks),
            Write(angle_labels),
            run_time=1.5
        )
        self.wait(0.5)
        
        # 2. 标记边c
        self.play(Create(edge_c))
        self.wait(0.5)
        
        # 3. 显示面积计算
        self.play(Write(area_display))
        self.wait(0.5)
        
        # 4. 右侧公式区域
        self.play(Write(formula_title))
        self.play(Write(conditions))
        self.wait(2)
        
        # 5. 显示推导过程
        self.play(Write(arrow1))
        self.play(Write(area_formula))
        self.wait(2)
        
        # 6. 变化边c的长度，观察面积的变化
        self.play(c_length.animate.set_value(2), run_time=1.5)
        self.wait(2)
        self.play(c_length.animate.set_value(4), run_time=1.5)
        self.wait(2)
        self.play(c_length.animate.set_value(3), run_time=1.2)
        self.wait(2)
        
        # 7. 题目条件
        self.play(Write(problem_condition))
        self.wait(3)
        
        # 8. 展示解决过程
        self.play(Write(arrow2))
        self.play(Write(solution))
        self.wait(1)
        
        # 9. 变化c值到正确答案，高亮显示
        self.play(
            c_length.animate.set_value(target_c_value), 
            run_time=2
        )
        
        # 创建最终高亮效果
        final_area = MathTex(
            "S", "=", "3 + \\sqrt{3}",
            tex_to_color_map={
                "S": YELLOW,
                "3 + \\sqrt{3}": YELLOW
            },
            font_size=36
        ).move_to(area_display.get_center())
        
        final_c = MathTex(
            "c", "=", "2\\sqrt{2}", "\\approx", f"{target_c_value:.2f}",
            tex_to_color_map={
                "c": YELLOW,
                "2\\sqrt{2}": YELLOW,
                f"{target_c_value:.2f}": YELLOW
            },
            font_size=36
        ).next_to(final_area, DOWN, buff=0.5)
        
        self.play(
            Transform(area_display, final_area),
            FadeIn(final_c),
            run_time=1.5
        )
 
        self.add(final_area)
        self.remove(area_display)
        
        self.wait(4)
        
        # 淡出所有对象
        self.play(FadeOut(*self.mobjects), run_time=1.5) 