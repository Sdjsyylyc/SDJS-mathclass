# 复合函数动画类

这个项目提供了一个封装好的复合函数动画类，可以轻松创建复合函数的可视化动画。

## 功能特点

- 四象限显示：内函数、外函数、复合函数、反函数
- 动态绘制：x值匀速增长，函数同步绘制
- 动态点和连接线：显示函数间的对应关系
- 高度可定制：可自定义函数、坐标系范围、标题等

## 安装依赖

```bash
pip install manim scipy numpy
```

## 使用方法

### 基本用法

```python
from composite_function_animation import CompositeFunctionAnimation
import numpy as np

class MyAnimation(CompositeFunctionAnimation):
    def __init__(self):
        # 定义内函数 g(x)
        def inner_function(x):
            return x**2 - 1
        
        # 定义外函数 f(u)
        def outer_function(u):
            return np.exp(u) * 2 / np.exp(3)
        
        # 调用父类构造函数
        super().__init__(
            inner_func=inner_function,
            outer_func=outer_function,
            title_text="f(x) = e^{x^2-1}"
        )
```

### 运行动画

```bash
manim demo.py Example1 -p
```

## 参数说明

### CompositeFunctionAnimation 参数

- `inner_func`: 内函数 g(x)，必需参数
- `outer_func`: 外函数 f(u)，必需参数
- `x_range`: x轴范围，格式 [min, max, step]，默认 [-1, 2, 1]
- `y_range`: y轴范围，格式 [min, max, step]，默认 [-1, 2, 1]
- `x_start`: 动画起始x值，默认 -1
- `x_end`: 动画结束x值，默认 2
- `title_text`: 标题文本，默认 None（不显示标题）

## 示例

### 示例1：指数函数复合
```python
class Example1(CompositeFunctionAnimation):
    def __init__(self):
        def inner_function(x):
            return x**2 - 1
        
        def outer_function(u):
            return np.exp(u) * 2 / np.exp(3)
        
        super().__init__(
            inner_func=inner_function,
            outer_func=outer_function,
            title_text="f(x) = e^{x^2-1}"
        )
```

### 示例2：二次函数复合
```python
class Example2(CompositeFunctionAnimation):
    def __init__(self):
        def inner_function(x):
            return x + 1
        
        def outer_function(u):
            return u**2
        
        super().__init__(
            inner_func=inner_function,
            outer_func=outer_function,
            x_range=[-2, 2, 1],
            y_range=[-1, 4, 1],
            x_start=-2,
            x_end=2,
            title_text="f(x) = (x+1)^2"
        )
```

### 示例3：三角函数复合
```python
class Example3(CompositeFunctionAnimation):
    def __init__(self):
        def inner_function(x):
            return 2 * x
        
        def outer_function(u):
            return np.sin(u)
        
        super().__init__(
            inner_func=inner_function,
            outer_func=outer_function,
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_start=-1.5,
            x_end=1.5,
            title_text="f(x) = \\sin(2x)"
        )
```

## 四象限说明

- **左上角**：内函数 g(x)
- **右上角**：外函数的反函数 f^(-1)(y)（xy轴交换）
- **左下角**：复合函数 f(g(x))
- **右下角**：外函数 f(u)

## 注意事项

1. 函数定义域应与坐标系范围匹配
2. 外函数的反函数使用数值方法计算，可能需要适当的定义域
3. 函数应当连续且在给定范围内有定义
4. 复杂函数可能需要调整坐标系范围以获得最佳显示效果

## 文件结构

```
inverse_function_visualization/
├── composite_function_animation.py  # 主动画类
├── demo.py                         # 使用示例
├── README.md                       # 说明文档
└── example.py                      # 原始示例（已废弃）
``` 