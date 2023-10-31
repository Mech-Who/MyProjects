import kalidokit4python.Util.Vector as Vec
from kalidokit4python.Util.Vector import Vector
from kalidokit4python.Util.Constants import PI


def createEulerPlane(lm):
    """
    Calculate stable plane (triangle) from 4 face landmarks
    :param lm: array of results from tfjs or mediapipe
    """
    # create face detection square bounds
    p1 = Vector(lm[21])  # top left
    p2 = Vector(lm[251])  # top right
    p3 = Vector(lm[397])  # bottom right
    p4 = Vector(lm[172])  # bottom left
    p3mid = p3.lerp(p4, 0.5)  # bottom midpoint
    return {
        "vector": [p1, p2, p3mid],
        "points": [p1, p2, p3, p4]
    }

def calcHead(lm):
    """
    Calculate roll, pitch, yaw, centerpoint, and rough dimentions of face plane
    :param lm: array of results from tfjs or mediapipe
    """
    # find 3 vectors that form a plane to represent the head
    plane = createEulerPlane(lm)["vector"]
    # calculate roll pitch and yaw from vectors
    rotate = Vec.rollPitchYaw(plane[0], plane[1], plane[2])
    # find the center of the face detection box
    midPoint = plane[0].lerp(plane[1], 0.5)
    # find the dimensions roughly of the face detection box
    width = plane[0].distance(plane[1])
    height = midPoint.distance(plane[2])
    # flip
    rotate.x *= -1
    rotate.z *= -1

    return {
        # defaults to radians for rotation around x,y,z axis
        "y": rotate.y * PI,  # left right
        "x": rotate.x * PI,  # up down
        "z": rotate.z * PI,  # side to side
        "width": width,
        "height": height,
        # center of face detection square
        "position": midPoint.lerp(plane[2], 0.5),
        # returns euler angles normalized between -1 and 1
        "normalized": {
            "y": rotate.y,
            "x": rotate.x,
            "z": rotate.z,
        },
        "degrees": {
            "y": rotate.y * 180,
            "x": rotate.x * 180,
            'z': rotate.z * 180,
        }
    }
