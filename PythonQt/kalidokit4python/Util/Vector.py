import math
import random
import numpy as np
from kalidokit4python.Util.CustomTypes import EulerRotation
from kalidokit4python.Util.Constants import TWO_PI, PI


class Vector:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __init__(self, a=None, b=None, c=None):
        if isinstance(a, (list, tuple)):
            self.x = a[0] if len(a) > 0 else 0
            self.y = a[1] if len(a) > 1 else 0
            self.z = a[2] if len(a) > 2 else 0
            return

        if isinstance(a, (Vector, EulerRotation)):
            self.x = a.x
            self.y = a.y
            self.z = a.z
            return

        self.x = a if a is not None else 0
        self.y = b if b is not None else 0
        self.z = c if c is not None else 0

    def __str__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise IndexError("Index out of range")

    def toDegree(self, factor=180/PI):
        return Vector(self.x*factor, self.y*factor, self.z*factor)

    # Methods
    def negative(self):
        # Returns the negative of this vector.
        return Vector(-self.x, -self.y, -self.z)

    def add(self, v):
        """
        Add a vector or number to this vector.
        :param {Vector | number} v: Vector or number to add
        :returns {Vector} New vector
        """
        if isinstance(v, Vector):
            return Vector(self.x + v.x, self.y + v.y, self.z + v.z)
        else:
            return Vector(self.x + v, self.y + v, self.z + v)

    def subtract(self, v):
        """
        Subtracts a vector or number from this vector.
        :param {Vector | number} v: Vector or number to subtract
        :returns {Vector} New vector
        """
        if isinstance(v, Vector):
            return Vector(self.x - v.x, self.y - v.y, self.z - v.z)
        else:
            return Vector(self.x - v, self.y - v, self.z - v)

    def multiply(self, v):
        """
        Multiplies a vector or a number to a vector.
        :param {Vector | number} v: Vector or number to multiply
        """
        if isinstance(v, Vector):
            return Vector(self.x * v.x, self.y * v.y, self.z * v.z)
        else:
            return Vector(self.x * v, self.y * v, self.z * v)

    def divide(self, v):
        """
        Divide this vector by a vector or a number.
        :param: {Vector | number} a: Vector or number to divide
        :returns: {Vector} New vector
        """
        if isinstance(v, Vector):
            return Vector(self.x / v.x, self.y / v.y, self.z / v.z)
        else:
            return Vector(self.x / v, self.y / v, self.z / v)

    def equals(self, v) -> bool:
        """
        Check if the given vector is equal to this vector.
        :param: {Vector} v: Vector to compare
        :returns: {boolean} True if equal
        """
        return self.x == v.x and self.y == v.y and self.z == v.z

    def dot(self, v) -> float:
        """
        Returns the dot product of this vector and another vector.
        :param: {Vector} v: Vector to dot
        :returns: {number} Dot product
        """
        return self.x * v.x + self.y * v.y + self.z * v.z

    def cross(self, v):
        """
        Cross product of two vectors.
        :param: {Vector} a: Vector to cross
        :param: {Vector} b: Vector to cross
        """
        return Vector(
            self.y * v.z - self.z * v.y,
            self.z * v.x - self.x * v.z,
            self.x * v.y - self.y * v.x,
        )

    def length(self) -> float:
        """
        Get the length of the Vector
        :returns: {number} Length
        """
        return math.sqrt(self.dot(self))

    def distance(self, v, d=3):
        """
        Find the distance between this and another vector.
        :param: {Vector} v: Vector to find distance to
        :param: {2 | 3} d: 2D or 3D distance
        :returns: {number} Distance
        """
        if d == 2:
            return math.sqrt(
                math.pow(self.x - v.x, 2) + math.pow(self.y - v.y, 2)
            )
        else:
            return math.sqrt(
                math.pow(self.x - v.x, 2)
                + math.pow(self.y - v.y, 2)
                + math.pow(self.z - v.z, 2)
            )

    def lerp(self, v, fraction):
        """
        Lerp between this vector and another vector.
        :param: {Vector} v: Vector to lerp to
        :param: {number} fraction: Fraction to lerp
        :returns: {Vector}
        """
        return v.subtract(self).multiply(fraction).add(self)

    def unit(self):
        """
        Returns the unit vector of this vector.
        :returns: {Vector} Unit vector
        """
        return self.divide(self.length())

    def min(self):
        return min(min(self.x, self.y), self.z)

    def max(self):
        return max(max(self.x, self.y), self.z)

    def toSphericalCoords(self, axis_map=None):
        """
        To Angles
        :param axis_map: {"x": "x", "y": "y", "z": "z"}
        :returns: theta: 极角,表示从正z轴的方向到向量的方向所需旋转的角度;
        phi: 方位角,表示从正x轴的方向逆时针旋转到向量在x-y平面上的投影所需的角度
        """
        if axis_map is None:
            axis_map = {"x": "x", "y": "y", "z": "z"}
        x, y, z = self.x, self.y, self.z
        a = eval(axis_map["x"])
        b = eval(axis_map["y"])
        c = eval(axis_map["z"])
        theta = math.atan2(b, a)
        phi = math.acos(c / self.length())
        return theta, phi

    def angleTo(self, a):
        """
        Returns the angle between this vector and vector 'a' in radians.
        :param a: Vector
        :returns: angle between this vector and vector 'a' in radians.
        """
        return math.acos(self.dot(a) / (self.length() * a.length()))

    def toArray(self, n=None):
        """
        Array representation of the vector.
        :param n: Array length
        :returns: Array
        :example: Vector(1, 2, 3).toArray(); // [1, 2, 3]
        """
        return [self.x, self.y, self.z][:n or 3]

    def clone(self):
        """
        Clone the vector.
        :returns: New vector
        """
        return Vector(self.x, self.y, self.z)

    def init(self, x, y, z):
        """
        Init this Vector with explicit values
        :param x: X value
        :param y: Y value
        :param z: Z value
        """
        self.x = x
        self.y = y
        self.z = z
        return self


# static methods
def negative(a, b=None):
    if b is None:
        b = Vector()
    b.x = -a.x
    b.y = -a.y
    b.z = -a.z
    return b


def add(a, b, c=None):
    if c is None:
        c = Vector()
    if isinstance(b, Vector):
        c.x = a.x + b.x
        c.y = a.y + b.y
        c.z = a.z + b.z
    else:
        c.x = a.x + b
        c.y = a.y + b
        c.z = a.z + b
    return c


def subtract(a, b, c=None):
    if c is None:
        c = Vector()
    if isinstance(b, Vector):
        c.x = a.x - b.x
        c.y = a.y - b.y
        c.z = a.z - b.z
    else:
        c.x = a.x - b
        c.y = a.y - b
        c.z = a.z - b
    return c


def multiply(a, b, c=None):
    if c is None:
        c = Vector()
    if isinstance(b, Vector):
        c.x = a.x * b.x
        c.y = a.y * b.y
        c.z = a.z * b.z
    else:
        c.x = a.x * b
        c.y = a.y * b
        c.z = a.z * b
    return c


def divide(a, b, c=None):
    if c is None:
        c = Vector()
    if isinstance(b, Vector):
        c.x = a.x / b.x
        c.y = a.y / b.y
        c.z = a.z / b.z
    else:
        c.x = a.x / b
        c.y = a.y / b
        c.z = a.z / b
    return c


def cross(a, b, c=None):
    if c is None:
        c = Vector()
    c.x = a.y * b.z - a.z * b.y
    c.y = a.z * b.x - a.x * b.z
    c.z = a.x * b.y - a.y * b.x
    return c


def unit(a, b):
    length = a.length()
    b.x = a.x / length
    b.y = a.y / length
    b.z = a.z / length
    return b


def fromAngles(theta: float, phi: float):
    """
    Create new vector from angles
    :param theta: Theta angle
    :param phi: Phi angle
    :returns: New vector
    """
    return Vector(math.cos(theta) * math.cos(phi), math.sin(phi), math.sin(theta) * math.cos(phi))


def randomDirection():
    return fromAngles(random.random() * TWO_PI, math.asin(random.random() * 2 - 1))


def min(a, b):
    return Vector(min(a.x, b.x), min(a.y, b.y), min(a.z, b.z))


def max(a, b):
    return Vector(max(a.x, b.x), max(a.y, b.y), max(a.z, b.z))


def lerp(a, b, fraction):
    """
    Lerp between two vectors
    :param a: Vector a
    :param b: Vector b
    :param fraction: Fraction
    """
    return b.subtract(a).multiply(fraction).add(a)


def fromArray(a):
    """
    Create a new vector from an Array

    :param a: Array
    :return: New vector
    """
    if isinstance(a, list):
        return Vector(a[0], a[1], a[2])
    return Vector(a.x, a.y, a.z)


def angleBetween(a, b):
    """
    Angle between two vectors
    :param a: Vector a
    :param b: Vector b
    :returns: Angle between two vectors
    """
    return a.angleTo(b)


def distance(a, b, d):
    if d == 2:
        return math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
    else:
        return math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2) + math.pow(a.z - b.z, 2))


def toDegrees(a):
    return a * (180 / PI)


def normalizeAngle(radians):
    """
    确保角度的范围在[-π, π]内，并将其归一化到[-1, 1]的范围内
    :param radians: Radians value
    """
    angle = radians % TWO_PI
    if angle > PI:
        angle = angle - TWO_PI
    elif angle < -PI:
        angle = TWO_PI + angle
    # returns normalized values to -1,1
    return angle / PI


def normalizeRadians(radians):
    """
    确保角度的范围在[-π/2, π/2]内，并将其归一化到[-1, 1]的范围内
    Normalize radians to -1,1
    :param radians: Radians value
    """
    # Normalize radians to -pi,pi
    if radians >= PI / 2:
        radians -= TWO_PI
    if radians <= -PI / 2:
        radians += TWO_PI
        radians = PI - radians
    # returns normalized values to -1,1
    return radians / PI


def find2DAngle(ax, ay, bx, by, az=None, bz=None):
    """
    Find 2D angle between two points, vector a -> b, x -> y
    """
    if az is None and bz is None:
        dy = by - ay
        dx = bx - ax
        theta = math.atan2(dy, dx)
        return theta
    else:
        dz = bz - az
        dy = by - ay
        dx = bx - ax
        projection = np.sqrt(dx ** 2 + dy ** 2)
        theta = np.arctan2(dz, projection)
        return theta


def findRotation(a, b, normalize=True):
    """
    Find 3D rotation of vector between two point, (绕z, 饶x, 绕y)
    xy: x->y
    yz: z->y => y->z
    xz: z->x
    @param {Vector} a: Start point vector
    @param {Vector} b: End point vector
    @param {boolean} normalize: Normalize the result or not
    """
    if normalize:
        return Vector(
            normalizeRadians(find2DAngle(a.x, a.y, b.x, b.y)),
            normalizeRadians(find2DAngle(a.y, a.z, b.y, b.z)),
            normalizeRadians(find2DAngle(a.z, a.x, b.z, b.x))
        )
    else:
        return Vector(
            find2DAngle(a.x, a.y, b.x, b.y),
            find2DAngle(a.y, a.z, b.y, b.z),
            find2DAngle(a.z, a.x, b.z, b.x)
        )


def rollPitchYaw(a, b, c=None):
    """
    Find roll pitch yaw of plane formed by 3 points
    :param a: Vector
    :param b: Vector
    :param c: Vector
    """
    # return roll, pitch, yaw
    if c is None:
        return Vector(
            normalizeAngle(find2DAngle(a.x, a.y, b.x, b.y)),
            normalizeAngle(find2DAngle(a.y, a.z, b.y, b.z)),
            normalizeAngle(find2DAngle(a.z, a.x, b.z, b.x)),
        )
    qb = b.subtract(a)
    qc = c.subtract(a)
    n = qb.cross(qc)
    unitZ = n.unit()
    unitX = qb.unit()
    unitY = unitZ.cross(unitX)
    beta = math.asin(unitZ.x) or 0
    alpha = math.atan2(-unitZ.y, unitZ.z) or 0
    gamma = math.atan2(-unitY.x, unitX.x) or 0
    return Vector(
        normalizeAngle(alpha),
        normalizeAngle(beta),
        normalizeAngle(gamma)
    )


def angleBetween3DCoords(a, b, c):
    """
    Find angle between 3 3D Coordinates
    :param a: Vector or Number
    :param b: Vector or Number, coord between a and c
    :param c: Vector or Number
    """
    if not isinstance(a, Vector):
        a = Vector(a)
        b = Vector(b)
        c = Vector(c)

    # Calculate vector between points 1 and 2
    v1 = a.subtract(b)

    # Calculate vector between points 2 and 3
    v2 = c.subtract(b)

    # The dot product of vectors v1 & v2 is a function of the cosine of the
    # angle between them (it's scaled by the product of their magnitudes).
    v1norm = v1.unit()
    v2norm = v2.unit()

    # Calculate the dot products of vectors v1 and v2
    dotProducts = v1norm.dot(v2norm)

    # Extract the angle from the dot products
    angle = math.acos(dotProducts)

    # return single angle Normalized to 1
    return normalizeAngle(angle)


def getRelativeSphericalCoords(a, b, c, axis_map=None):
    """
    Get normalized, spherical coordinates for the vector bc, relative to vector ab
    :param a: Vector or Number
    :param b: Vector or Number
    :param c: Vector or Number
    :param axis_map: Mapped axis to get the right spherical coords
    :returns: theta: 极角,表示从正z轴的方向到向量的方向所需旋转的角度;
        phi: 方位角,表示从正x轴的方向逆时针旋转到向量在x-y平面上的投影所需的角度
    """
    if axis_map is None:
        axis_map = {"x": "x", "y": "y", "z": "z"}

    if not isinstance(a, Vector):
        a = Vector(a)
        b = Vector(b)
        c = Vector(c)

    # Calculate vector between points 1 and 2
    v1 = b.subtract(a)

    # Calculate vector between points 2 and 3
    v2 = c.subtract(b)

    v1norm = v1.unit()
    v2norm = v2.unit()

    theta1, phi1 = v1norm.toSphericalCoords(axis_map)
    theta2, phi2 = v2norm.toSphericalCoords(axis_map)

    theta = theta1 - theta2
    phi = phi1 - phi2

    return normalizeAngle(theta), normalizeAngle(phi)


def getSphericalCoords(a, b, axis_map=None):
    """
    Get normalized, spherical coordinates for the vector bc
    :param a: Vector or Number
    :param b: Vector or Number
    :param axis_map: Mapped axis to get the right spherical coords
    :return: theta, phi
    """
    if axis_map is None:
        axis_map = {"x": "x", "y": "y", "z": "z"}
    if not isinstance(a, Vector):
        a = Vector(a)
        b = Vector(b)

    # Calculate vector between points 1 and 2
    v1 = subtract(b, a)

    v1norm = v1.unit()
    theta, phi = v1norm.toSphericalCoords(axis_map)

    return normalizeAngle(-theta), normalizeAngle(PI / 2 - phi)
