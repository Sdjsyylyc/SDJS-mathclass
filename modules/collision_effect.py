from manim import *
import numpy as np


class CollisionEffect:
    """
    创建碰撞特效的类，用于在指定位置生成散开的直线动画效果。
    
    该类可以在指定的点创建一个碰撞特效，表现为多条直线从中心向外扩散。
    适用于表示数学概念中的"接触"、"相切"或"碰撞"等情况。
    """
    
    def __init__(self, center_point, outer_radius=0.2, inner_radius=0.03, 
                 stroke_width=2, color=YELLOW, num_lines=12, duration=1.0):
        """
        初始化碰撞特效。
        
        参数:
            center_point: 碰撞中心点的坐标 (manim坐标)
            outer_radius: 外扩散半径
            inner_radius: 内部起始半径
            stroke_width: 直线宽度
            color: 直线颜色
            num_lines: 直线数量
            duration: 动画持续时间
        """
        self.center_point = center_point
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius
        self.stroke_width = stroke_width
        self.color = color
        self.num_lines = num_lines
        self.duration = duration
        
        # 创建ValueTracker用于动画控制
        self.end_radius = ValueTracker(inner_radius + 0.01)
        self.start_radius = ValueTracker(inner_radius)
        
        # 创建直线组
        self.lines = VGroup()
        self._create_lines()
        
        # 创建动画组
        self.animation = AnimationGroup(
            self.end_radius.animate.set_value(outer_radius - 0.01),
            self.start_radius.animate.set_value(outer_radius),
            lag_ratio=0.5,
            run_time=duration
        )
    
    def _create_lines(self):
        """创建所有的散开直线。"""
        for i in range(self.num_lines):
            angle = i * 2 * PI / self.num_lines  # 均匀分布角度
            
            # 使用闭包正确捕获angle值
            def make_line(angle_val):
                def get_line():
                    # 在每次重绘时重新计算位置
                    start_r = self.start_radius.get_value()
                    end_r = self.end_radius.get_value()
                    
                    start_pos = (self.center_point + 
                               start_r * np.cos(angle_val) * RIGHT + 
                               start_r * np.sin(angle_val) * UP)
                    end_pos = (self.center_point + 
                             end_r * np.cos(angle_val) * RIGHT + 
                             end_r * np.sin(angle_val) * UP)
                    
                    return Line(start_pos, end_pos, 
                              color=self.color, 
                              stroke_width=self.stroke_width)
                return get_line
            
            line = always_redraw(make_line(angle))
            self.lines.add(line)
    
    def get_lines(self):
        """获取直线组，用于添加到场景中。"""
        return self.lines
    
    def get_animation(self):
        """获取动画对象，用于播放特效。"""
        return self.animation
    
    def reset(self):
        """重置特效到初始状态。"""
        self.end_radius.set_value(self.inner_radius + 0.01)
        self.start_radius.set_value(self.inner_radius)
    
    @staticmethod
    def create_simple_effect(scene, center_point, outer_radius=0.1, **kwargs):
        """
        静态方法：创建并播放一个简单的碰撞特效。
        
        参数:
            scene: Manim场景对象
            center_point: 碰撞中心点
            outer_radius: 外扩散半径
            **kwargs: 其他可选参数
        
        返回:
            CollisionEffect对象
        """
        effect = CollisionEffect(center_point, outer_radius, **kwargs)
        scene.add(effect.get_lines())
        scene.play(effect.get_animation())
        scene.remove(effect.get_lines())
        return effect