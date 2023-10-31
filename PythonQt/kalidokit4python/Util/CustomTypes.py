from typing import Literal, Dict, TypedDict
from collections import namedtuple

XYZ = Literal["x", "y", "z"]
RotationOrder = Literal["XYZ", "YZX", "ZXY", "XZY", "YXZ", "ZYX"]
AxisMap = Dict[Literal["x", "y", "z"], Literal["x", "y", "z"]]
Runtime = namedtuple("Runtime", ['runtime', 'imageSize', 'enableLegs'])


class EulerRotation:
    x: float
    y: float
    z: float
    rotationOrder: RotationOrder

