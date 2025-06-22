"""
Modules package for reusable Manim components.

This package contains various reusable components for Manim animations,
including UI elements, mathematical visualizations, and interactive components.
"""

from .slider_component import SliderComponent
from .custom_axes import CustomAxes
from .collision_effect import CollisionEffect
from .function_definitions import (
    LinearFunctionTwoPoints,
    LinearFunctionPointSlope,
    LinearFunctionGeneral,
    ExponentialFunction,
    LogarithmicFunction,
    PowerFunction,
)

__all__ = [
    "SliderComponent",
    "CustomAxes",
    "CollisionEffect",
    "LinearFunctionTwoPoints",
    "LinearFunctionPointSlope",
    "LinearFunctionGeneral",
    "ExponentialFunction",
    "LogarithmicFunction",
    "PowerFunction",
]

__version__ = "1.0.0"
__author__ = "SDJS Math Class"
__description__ = "Reusable Manim components for mathematical animations"
