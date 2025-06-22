from manim import *  # 导入 Manim 模块，包含场景、图形、动画等常用类和函数
import math  # 导入数学模块，用于数学计算

LITTLE_BLOCK_COLOR = "#51463E"  # 定义一个常量，表示"小方块"的颜色十六进制值
class StateTracker(ValueTracker):
    """
    将方块碰撞过程的状态跟踪为4维向量
    [
        x1 * sqrt(m1),
        x2 * sqrt(m2),
        v1 * sqrt(m1),
        v2 * sqrt(m2),
    ]
    """

    def __init__(self, blocks, initial_positions=[8, 5], initial_velocities=[-1, 0]):
        sqrt_m1, sqrt_m2 = self.sqrt_mass_vect = np.sqrt([b.mass for b in blocks])
        # 计算各方块质量的平方根，用于状态空间缩放
        self.theta = math.atan2(sqrt_m2, sqrt_m1)
        # theta 为质量比对应的角度，用于反射计算

        self.state0 = np.array([
            *np.array(initial_positions) * self.sqrt_mass_vect,
            *np.array(initial_velocities) * self.sqrt_mass_vect,
        ])
        # 初始状态向量：位置和速度都乘上相应的 sqrt(m)

        super().__init__(self.state0.copy())
        # 调用父类构造器，将初始状态作为 ValueTracker 的值

    def set_time(self, t):
        pos0 = self.state0[0:2]
        vel0 = self.state0[2:4]
        # 拆分出初始位置和速度

        self.set_value([*(pos0 + t * vel0), *vel0])
        # 根据时间 t 更新状态：位置 = 初始位置 + 速度 * t，速度不变

    def reflect_vect(self, vect):
        n_reflections = self.get_n_collisions()
        # 已发生碰撞次数

        rot_angle = -2 * self.theta * ((n_reflections + 1) // 2)
        # 旋转角度，基于碰撞次数和 theta

        result = rotate_vector_2d(vect, rot_angle)
        # 将向量在 2D 平面中旋转

        result[1] *= (-1)**(n_reflections % 2)
        # 每两次碰撞在第二分量上取反，实现反射效果

        return result

    def get_block_positions(self):
        scaled_pos = self.get_value()[0:2]
        # 获取当前缩放后的位置分量

        rot_scaled_pos = self.reflect_vect(scaled_pos)
        # 对位置进行反射变换

        return rot_scaled_pos / self.sqrt_mass_vect
        # 缩放回真实物理空间的坐标

    def get_scaled_block_velocities(self):
        return self.reflect_vect(self.get_value()[2:4])
        # 获取缩放后的速度，并做反射

    def get_block_velocities(self):
        return self.get_scaled_block_velocities() / self.sqrt_mass_vect
        # 缩放回真实速度

    def get_kinetic_energy(self):
        v1, v2 = self.get_value()[2:4]
        return v1**2 + v2**2  # 返回系统总动能（已含 1/2，因缩放关系）

    def get_momentum(self):
        v1, v2 = self.get_block_velocities()
        m1, m2 = self.sqrt_mass_vect**2
        return m1 * v1 + m2 * v2  # 返回系统动量

    def get_n_collisions(self):
        state = self.get_value()  # 当前状态向量
        angle = math.atan2(state[1], state[0])
        return int(angle / self.theta)  # 碰撞次数来自状态向量的角度整除 theta

    def time_from_last_collision(self):
        state = self.get_value()
        angle = math.atan2(state[1], state[0])
        n_collisions = int(angle / self.theta)
        if n_collisions == 0:
            return 0  # 若还未碰撞，时间差为 0
        collisions_angle = n_collisions * self.theta
        rot_state = rotate_vector_2d(state[:2], collisions_angle - angle)
        # 将状态向量旋转到碰撞瞬间的方向

        collision_state = rot_state * (state[1] / rot_state[1])
        # 重新缩放以匹配 y 分量

        return (collision_state[0] - state[0]) / state[2]
        # 计算距离上次碰撞所需的时间差
