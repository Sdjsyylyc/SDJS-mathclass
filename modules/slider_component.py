from manim import *
import numpy as np

class SliderComponent(VGroup):
    def __init__(self, 
                 param_name,
                 value_tracker, 
                 min_val, 
                 max_val, 
                 position,
                 track_color=WHITE, 
                 slider_color=WHITE,
                 use_modulo=True,  # 新增参数：是否使用取模功能
                 **kwargs):
        super().__init__(**kwargs)
        
        self.value_tracker = value_tracker
        self.min_val = min_val
        self.max_val = max_val
        self.use_modulo = use_modulo
        self.range_length = max_val - min_val
        
        # 滑轨 - 使用细线
        self.track = Line(start=[-1, 0, 0], end=[1, 0, 0], color=track_color, stroke_width=2)
        self.track.move_to(position)
        
        # 滑块 - 实心圆形
        self.slider = Circle(radius=0.08, color=slider_color, fill_opacity=1.0, stroke_width=0)
        
        # 滑块位置更新函数
        def update_slider_position(mob):
            raw_value = self.value_tracker.get_value()
            
            if self.use_modulo and (raw_value > self.max_val or raw_value < self.min_val):
                # 使用取模来计算滑块位置
                # 将值映射到[min_val, max_val]区间内
                modulo_value = ((raw_value - self.min_val) % self.range_length) + self.min_val
                progress = (modulo_value - self.min_val) / self.range_length
            else:
                # 正常模式
                progress = (raw_value - self.min_val) / (self.max_val - self.min_val)
                # 限制progress在[0,1]范围内
                progress = max(0, min(1, progress))
            
            slider_x = self.track.get_start()[0] + progress * (self.track.get_end()[0] - self.track.get_start()[0])
            mob.move_to([slider_x, self.track.get_y(), 0])
        
        self.slider.add_updater(update_slider_position)
        
        # 参数标签 - 使用MathTex
        self.label = MathTex(param_name, font_size=28, color=WHITE)
        self.label.next_to(self.track, UP, buff=0.1)
        
        # 将所有组件添加到VGroup
        self.add(self.track, self.slider, self.label)
        
    def get_track(self):
        return self.track
        
    def get_slider(self):
        return self.slider
        
    def get_label(self):
        return self.label 