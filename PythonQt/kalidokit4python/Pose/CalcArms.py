import math
import kalidokit4python.Util.Vector as Vec
from kalidokit4python.Util.Vector import Vector
from kalidokit4python.Util.Constants import RIGHT, LEFT
from kalidokit4python.Util.Helper import clamp, remap


def deg2rad(degree):
    return degree*math.pi/180


def rigArm(UpperArm: Vector, LowerArm: Vector, Hand: Vector, side=RIGHT):
    """
    Converts normalized rotation values into radians clamped by human limits
    :param: Vector UpperArm: normalized rotation values
    :param: Vector LowerArm: normalized rotation values
    :param: Vector Hand: normalized rotation values
    :param: str side: left or right
    """
    # Invert modifier based on left vs right side
    invert = -1 if side == LEFT else 1
    UpperArm.z *= -2.3 * invert
    # Modify UpperArm rotationY  by lowerarm X and Z rotations
    UpperArm.y *= math.pi * invert
    UpperArm.y -= LowerArm.x
    UpperArm.y -= -invert * max(LowerArm.z, 0)
    UpperArm.x -= 0.3 * invert

    UpperArm.z *= -0.14 * invert
    UpperArm.y *= 0.14 * invert
    UpperArm.x *= 2.14 * invert

    # Clamp values to human limits
    UpperArm.x = clamp(UpperArm.x, -0.5, math.pi)
    UpperArm.x = clamp(LowerArm.x, -0.3, 0.3)

    Hand.y = clamp(Hand.z * 2, -0.6, 0.6)  # side to side
    Hand.z = Hand.z * -0.3 * invert  # up down

    return {
        "UpperArm": UpperArm,
        "LowerArm": LowerArm,
        "Hand": Hand
    }


def calcArms(lm3d: list):
    """
    Calculates arm rotation as euler angles(in radians)
    :param list lm3d: array of 3D pose vectors from mediapipe
    """
    # Pure Rotation Calculations
    # 计算空间角,左右是指观察者的左右(镜像后的左右)
    UpperArm = {
        "r": Vec.findRotation(Vec.fromArray(lm3d[11]), Vec.fromArray(lm3d[13])),
        "l": Vec.findRotation(Vec.fromArray(lm3d[12]), Vec.fromArray(lm3d[14])),
    }
    # 计算上臂相对肩膀的偏移角度
    UpperArm["r"].y = Vec.angleBetween3DCoords(Vec.fromArray(lm3d[12]), Vec.fromArray(lm3d[11]),
                                               Vec.fromArray(lm3d[13]))
    UpperArm["l"].y = Vec.angleBetween3DCoords(Vec.fromArray(lm3d[11]), Vec.fromArray(lm3d[12]),
                                               Vec.fromArray(lm3d[14]))
    # print(f"left upper arm: Vector({UpperArm['l'].x}, {UpperArm['l'].y}, {UpperArm['l'].z})")
    # print(f"left upper arm: Vector({UpperArm['l'].x*180/math.pi}, {UpperArm['l'].y*180/math.pi}, {UpperArm['l'].z*180/math.pi})")
    UpperArm["l"].x += 0
    UpperArm["l"].y += 8
    UpperArm["l"].z += 10
    # print(f"left upper arm: Vector({UpperArm['l'].x}, {UpperArm['l'].y}, {UpperArm['l'].z})")
    # print(f"left upper arm: Vector({UpperArm['l'].x * 180 / math.pi}, {UpperArm['l'].y * 180 / math.pi}, {UpperArm['l'].z * 180 / math.pi})")

    LowerArm = {
        "r": Vec.findRotation(Vec.fromArray(lm3d[13]), Vec.fromArray(lm3d[15])),
        "l": Vec.findRotation(Vec.fromArray(lm3d[14]), Vec.fromArray(lm3d[16])),
    }
    # 计算上臂相对肩膀的偏移角度
    LowerArm["r"].y = Vec.angleBetween3DCoords(Vec.fromArray(lm3d[11]), Vec.fromArray(lm3d[13]),
                                               Vec.fromArray(lm3d[15]))
    LowerArm["l"].y = Vec.angleBetween3DCoords(Vec.fromArray(lm3d[12]), Vec.fromArray(lm3d[14]),
                                               Vec.fromArray(lm3d[16]))

    # 把z的值卡在[-1, 0]之间，下臂不可倒弯，到底应该负还是正？
    LowerArm["r"].z = clamp(LowerArm["r"].z, -2.14, 0)
    LowerArm["l"].z = clamp(LowerArm["l"].z, -2.14, 0)
    # LowerArm["r"].z = clamp(LowerArm["r"].z, 0, 2.14)
    # LowerArm["l"].z = clamp(LowerArm["l"].z, 0, 2.14)
    Hand = {
        "r": Vec.findRotation(
            Vec.fromArray(lm3d[15]),
            Vec.lerp(Vec.fromArray(lm3d[17]), Vec.fromArray(lm3d[19]), 0.5)
        ),
        "l": Vec.findRotation(
            Vec.fromArray(lm3d[16]),
            Vec.lerp(Vec.fromArray(lm3d[18]), Vec.fromArray(lm3d[20]), 0.5)
        ),
    }

    # Modify Rotations slightly for more natural movement
    rightArmRig = rigArm(UpperArm["r"], LowerArm["r"], Hand["r"], RIGHT)
    leftArmRig = rigArm(UpperArm["l"], LowerArm["l"], Hand["l"], LEFT)

    # print(f"left upper arm: Vector({leftArmRig['UpperArm'].x}, {leftArmRig['UpperArm'].y}, {leftArmRig['UpperArm'].z})")
    # print(f"left upper arm: Vector({leftArmRig['UpperArm'].x * 180 / math.pi}, {leftArmRig['UpperArm'].y * 180 / math.pi}, {leftArmRig['UpperArm'].z * 180 / math.pi})")

    return {
        # Scaled
        "UpperArm": {
            "r": rightArmRig["UpperArm"],
            "l": leftArmRig["UpperArm"]
        },
        "LowerArm": {
            "r": rightArmRig["LowerArm"],
            "l": leftArmRig["LowerArm"]
        },
        "Hand": {
            "r": rightArmRig["Hand"],
            "l": leftArmRig["Hand"]
        },
        # Unscaled
        "Unscaled": {
            "UpperArm": UpperArm,
            "LowerArm": LowerArm,
            "Hand": Hand
        }
    }
