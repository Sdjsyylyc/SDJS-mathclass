# 数学函数参数动画

这个文件包含三个manim动画场景，展示带参数的数学函数图像随参数变化的过程。

## 场景说明

### 1. PowerFunction - 幂函数
- 函数：y = x^a
- 参数范围：a从0.5变化到3
- 图像颜色：黄色

### 2. ExponentialFunction - 指数函数  
- 函数：y = a^x
- 参数范围：a从1.5变化到3
- 图像颜色：绿色

### 3. LogarithmicFunction - 对数函数
- 函数：y = log_a(x)
- 参数范围：a从0.1变化到10
- 图像颜色：蓝色

### 4. TrigonometricFunction - 三角函数
- 函数：y = A sin(ωx + φ)
- 参数：A(振幅): 1→3, ω(角频率): 1→3, φ(相位): 0→2π
- 图像颜色：蓝色
- 动画分三阶段：先变振幅，再变频率，最后变相位

## 特点

- 每个动画持续60秒
- 右上角显示滑块和参数数值
- 使用ValueTracker实现参数跟踪
- 图像实时跟随参数变化
- 无文字标签，纯图像展示

## 运行方法

```bash
# 渲染单个场景
manim parameter_functions.py PowerFunction
manim parameter_functions.py ExponentialFunction
manim parameter_functions.py LogarithmicFunction
manim parameter_functions.py TrigonometricFunction

# 渲染所有场景
manim parameter_functions.py
```

## 输出

每个场景将生成一个60秒的动画视频，展示对应函数图像随参数缓慢变化的过程。 