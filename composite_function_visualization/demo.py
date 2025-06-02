from composite_function_animation import CompositeFunctionAnimation
import numpy as np

# 示例1：原来的例子 f(x) = e^(x²-1)
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

# 示例2：简单的二次函数复合 f(x) = (x+1)²
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

# 示例3：三角函数复合 f(x) = sin(2x)
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

# 示例4：对数函数复合 f(x) = ln(x²+1)
class Example4(CompositeFunctionAnimation):
    def __init__(self):
        def inner_function(x):
            return x**2 + 1
        
        def outer_function(u):
            return np.log(u)
        
        super().__init__(
            inner_func=inner_function,
            outer_func=outer_function,
            x_range=[-2, 2, 1],
            y_range=[-1, 3, 1],
            x_start=-2,
            x_end=2,
            title_text="f(x) = \\ln(x^2+1)"
        ) 