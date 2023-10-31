from kalidokit4python.Util.CustomTypes import EulerRotation, RotationOrder


class Euler:
    x: float
    y: float
    z: float
    rotationOrder: RotationOrder

    def __init__(self, a: EulerRotation | float=None, b: float=None, c: float=None, rotationOrder: RotationOrder=None):
        if isinstance(a, EulerRotation):
            self.x = a.x if a.x is not None else 0
            self.y = a.y if a.y is not None else 0
            self.z = a.z if a.z is not None else 0
            self.rotationOrder = a.rotationOrder if a.rotationOrder is not None else "XYZ"
            return

        self.x = a if a is not None else 0
        self.y = b if b is not None else 0
        self.z = c if c is not None else 0
        self.rotationOrder = rotationOrder if rotationOrder is not None else "XYZ"

    def multiply(self, v):
        """
        Multiplies a number to an Euler.
        :param a: Number to multiply
        """
        return Euler(self.x * v, self.y * v, self.z * v, self.rotationOrder)
    