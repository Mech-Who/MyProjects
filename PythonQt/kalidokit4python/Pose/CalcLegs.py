import math
import kalidokit4python.Util.Vector as Vec
from kalidokit4python.Util.Vector import Vector
from kalidokit4python.Util.Constants import RIGHT, LEFT
from kalidokit4python.Util.Helper import clamp, remap

offsets = {
    "upperLeg": {
        "z": 0.5
    }
}


def rigLeg(UpperLeg, LowerLeg, side=RIGHT):
    """
    Converts normalized rotation values into radians clamped by human limits
    :param Object UpperLeg: normalized rotation values
    :param Object LowerLeg: normalized rotation values
    :param str side: left or right
    :return: dict[str, Vector]
    """
    invert = 1 if side == LEFT else -1
    riggedUpperLeg = Vector(
        clamp(UpperLeg.x, 0, 0.5) * math.pi,
        clamp(UpperLeg.y, -0.2, 0.2) * math.pi,
        clamp(UpperLeg.z, -0.3, 0.3) * math.pi + invert * offsets["upperLeg"]["z"]
    )
    riggedLowerLeg = Vector(
        LowerLeg.x * math.pi,
        LowerLeg.y * math.pi,
        LowerLeg.z * math.pi
    )
    return {
        "UpperLeg": riggedUpperLeg,
        "LowerLeg": riggedLowerLeg,
    }


def calcLegs(lm):
    """
    Calculates leg rotation angles
    :param Results lm: array of 3D pose vectors from tfjs or mediapipe
    :return: dict[str, any]
    """
    rightUpperLeg_theta, rightUpperLeg_phi = Vec.getSphericalCoords(Vec.fromArray(lm[23]), Vec.fromArray(lm[25]))
    leftUpperLeg_theta, leftUpperLeg_phi = Vec.getSphericalCoords(Vec.fromArray(lm[24]), Vec.fromArray(lm[26]))
    rightLowerLeg_theta, rightLowerLeg_phi = Vec.getRelativeSphericalCoords(Vec.fromArray(lm[23]),
                                                                            Vec.fromArray(lm[25]),
                                                                            Vec.fromArray(lm[27]))
    leftLowerLeg_theta, leftLowerLeg_phi = Vec.getRelativeSphericalCoords(Vec.fromArray(lm[24]), Vec.fromArray(lm[26]),
                                                                          Vec.fromArray(lm[28]))
    hipRotation = Vec.findRotation(Vec.fromArray(lm[23]), Vec.fromArray(lm[24]))

    UpperLeg = {
        'r': Vector(
            rightUpperLeg_theta,
            rightLowerLeg_phi,
            rightUpperLeg_phi
        ),
        'l': Vector(
            leftUpperLeg_theta,
            leftLowerLeg_phi,
            leftUpperLeg_phi
        )
    }

    LowerLeg = {
        'r': Vector(
            -abs(rightLowerLeg_theta),
            0,  # not relevant
            0  # not relevant
        ),
        'l': Vector(
            -abs(leftLowerLeg_theta),
            0,  # not relevant
            0  # not relevant
        )
    }

    # Modify Rotations slightly for more natural movement
    rightLegRig = rigLeg(UpperLeg["r"], LowerLeg["r"], RIGHT)
    leftLegRig = rigLeg(UpperLeg["l"], LowerLeg["l"], LEFT)
    return {
        # Scaled
        "UpperLeg": {
            "r": rightLegRig["UpperLeg"],
            "l": leftLegRig["UpperLeg"]
        },
        "LowerLeg": {
            "r": rightLegRig["LowerLeg"],
            "l": leftLegRig["LowerLeg"]
        },
        # Unscaled
        "Unscaled": {
            "UpperLeg": UpperLeg,
            "LowerLeg": LowerLeg
        }
    }
