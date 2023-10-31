import math
import pprint

import kalidokit4python.Util.Vector as Vec
from kalidokit4python.Util.Vector import Vector
from kalidokit4python.Util.Helper import clamp, remap


def rigHips(hips: dict, spine: Vector):
    """
    Converts normalized rotations to radians and estimates world position of hips
    :param dict hips: hip's position and rotation values
    :param Vector spine: spine position and rotation values
    :return: dict[str, any]
    """
    # # convert normalized values to radians
    # if hips["rotation"] is not None:
    #     hips["rotation"].x *= math.pi
    #     hips["rotation"].y *= math.pi
    #     hips["rotation"].z *= math.pi
    #
    # spine.x *= math.pi
    # spine.y *= math.pi
    # spine.z *= math.pi

    return {
        "Hips": hips,
        "Spine": spine
    }


def calcHips(lm3d, lm2d):
    """
    Calculates Hip rotation and world position
    :param {Array} lm3d: array of 3D pose vectors from mediapipe
    :param {Array} lm2d: array of 2D pose vectors from mediapipe
    :return: dict[str, any]
    """
    # Find 2D normalized Hip and Shoulder Joint Positions/Distances
    hipLeft2d = Vec.fromArray(lm2d[23])
    hipRight2d = Vec.fromArray(lm2d[24])
    shoulderLeft2d = Vec.fromArray(lm2d[11])
    shoulderRight2d = Vec.fromArray(lm2d[12])
    hipCenter2d = hipLeft2d.lerp(hipRight2d, 0.5)
    shoulderCenter2d = shoulderLeft2d.lerp(shoulderRight2d, 0.5)
    spineLength = hipCenter2d.distance(shoulderCenter2d)

    hips = {
        "position": Vector(clamp(hipCenter2d.x - 0.4, -1, 1), 0, clamp(spineLength - 1, -2, 0))
    }
    hips["worldPosition"] = Vector(hips["position"].x, 0, hips["position"].z * math.pow(hips["position"].z * -2, 2))
    hips["worldPosition"].x *= hips["worldPosition"].z

    hips["rotation"] = Vec.rollPitchYaw(lm3d[23], lm3d[24])
    # fix -PI, PI jumping
    if hips["rotation"].y > 0.5:
        hips["rotation"].y -= 2
    hips["rotation"].y += 0.5
    # Stop jumping between left and right shoulder tilt
    if hips["rotation"].z > 0:
        hips["rotation"].z = 1 - hips["rotation"].z
    if hips["rotation"].z < 0:
        hips["rotation"].z = -1 - hips["rotation"].z
    turnAroundAmountHips = remap(abs(hips["rotation"].y), 0.2, 0.4)
    hips["rotation"].z *= 1 - turnAroundAmountHips
    hips["rotation"].x = 0  # temp fix for inaccurate X axis

    spine = Vec.rollPitchYaw(lm3d[11], lm3d[12])
    # fix -PI, PI jumping
    if spine.y > 0.5:
        spine.y -= 2
    spine.y += 0.5
    # Stop jumping between left and right shoulder tilt
    if spine.z > 0:
        spine.z = 1 - spine.z
    if spine.z < 0:
        spine.z = -1 - spine.z
    # fix weird large numbers when 2 shoulder points get too close
    turnAroundAmount = remap(abs(spine.y), 0.2, 0.4)
    spine.z *= 1 - turnAroundAmount
    spine.x = 0  # temp fix for inaccurate X axis

    return rigHips(hips, spine)
