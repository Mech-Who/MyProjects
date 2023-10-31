import math
from kalidokit4python.Util.CustomTypes import Runtime
from kalidokit4python.Util.Vector import Vector
from kalidokit4python.Pose.CalcLegs import calcLegs
from kalidokit4python.Pose.CalcArms import calcArms
from kalidokit4python.Pose.CalcHips import calcHips

# A set of default pose values in radians to serve as "rest" values
RestingDefault = {
    "Face": {
        "eye": {
            "l": 1,
            "r": 1,
        },
        "mouth": {
            "x": 0,
            "y": 0,
            "shape": {
                "A": 0,
                "E": 0,
                "I": 0,
                "O": 0,
                "U": 0,
            },
        },
        "head": {
            "x": 0,
            "y": 0,
            "z": 0,
            "width": 0.3,
            "height": 0.6,
            "position": Vector(0.5, 0.5, 0),
        },
        "brow": 0,
        "pupil": {
            "x": 0,
            "y": 0,
        }
    },
    "Pose": {
        "RightUpperArm": Vector(0, 0, -1.25),
        "LeftUpperArm": Vector(0, 0, 1.25),  # y: 0 > -.5 # z: -.5>.5
        "RightLowerArm": Vector(0, 0, 0),
        "LeftLowerArm": Vector(0, 0, 0),  # x: 0 > -4, z: 0 to -.9
        "LeftUpperLeg": Vector(0, 0, 0),
        "RightUpperLeg": Vector(0, 0, 0),
        "RightLowerLeg": Vector(0, 0, 0),
        "LeftLowerLeg": Vector(0, 0, 0),
        "LeftHand": Vector(0, 0, 0),
        "RightHand": Vector(0, 0, 0),
        "Spine": Vector(0, 0, 0),
        "Hips": {
            "position": Vector(0, 0, 0),
            "rotation": Vector(0, 0, 0)
        }
    },
    "RightHand": {
        "RightWrist": Vector(-0.13, -0.07, -1.04),
        "RightRingProximal": Vector(0, 0, -0.13),
        "RightRingIntermediate": Vector(0, 0, -0.4),
        "RightRingDistal": Vector(0, 0, -0.04),
        "RightIndexProximal": Vector(0, 0, -0.24),
        "RightIndexIntermediate": Vector(0, 0, -0.25),
        "RightIndexDistal": Vector(0, 0, -0.06),
        "RightMiddleProximal": Vector(0, 0, -0.09),
        "RightMiddleIntermediate": Vector(0, 0, -0.44),
        "RightMiddleDistal": Vector(0, 0, -0.06),
        "RightThumbProximal": Vector(-0.23, -0.33, -0.12),
        "RightThumbIntermediate": Vector(-0.2, -0.199, -0.0139),
        "RightThumbDistal": Vector(-0.2, 0.002, 0.15),
        "RightLittleProximal": Vector(0, 0, -0.09),
        "RightLittleIntermediate": Vector(0, 0, -0.225),
        "RightLittleDistal": Vector(0, 0, -0.1)
    },
    "LeftHand": {
        "LeftWrist": Vector(-0.13, -0.07, -1.04),
        "LeftRingProximal": Vector(0, 0, 0.13),
        "LeftRingIntermediate": Vector(0, 0, 0.4),
        "LeftRingDistal": Vector(0, 0, 0.049),
        "LeftIndexProximal": Vector(0, 0, 0.24),
        "LeftIndexIntermediate": Vector(0, 0, 0.25),
        "LeftIndexDistal": Vector(0, 0, 0.06),
        "LeftMiddleProximal": Vector(0, 0, 0.09),
        "LeftMiddleIntermediate": Vector(0, 0, 0.44),
        "LeftMiddleDistal": Vector(0, 0, 0.066),
        "LeftThumbProximal": Vector(-0.23, 0.33, 0.12),
        "LeftThumbIntermediate": Vector(-0.2, 0.25, 0.05),
        "LeftThumbDistal": Vector(-0.2, 0.17, -0.06),
        "LeftLittleProximal": Vector(0, 0, 0.17),
        "LeftLittleIntermediate": Vector(0, 0, 0.4),
        "LeftLittleDistal": Vector(0, 0, 0.1)
    }
}


class PoseSolver:
    """
    这个动作是镜像动作！
    所以左右手是反过来计算的
    """
    @staticmethod
    def solve(lm3d, lm2d, runtime=None):
        """
        Combines arm, hips, and leg calcs into one method
        :param Array lm3d: array of 3D pose vectors from tfjs or mediapipe
        :param Array lm2d: array of 2D pose vectors from tfjs or mediapipe
        :param namedtuple runtime: 
            runtime: set as either "tfjs" or "mediapipe"
            imageSize: dom element's size (width, height)
            enableLegs: if the leg usable, leg data should be calculated
        """
        if runtime is None:
            runtime = Runtime(runtime="mediapipe", imageSize=None, enableLegs=True)

        if not lm3d or not lm2d:
            print("Need both World Pose and Pose Landmarks")
            return

        Arms = calcArms(lm3d)
        Hips = calcHips(lm3d, lm2d)
        Legs = calcLegs(lm3d) if runtime.enableLegs else None

        # DETECT OFFSCREEN AND RESET VALUES TO DEFAULTS
        rightHandOffscreen = lm3d[15].y > 0.1 or lm3d[15].visibility < 0.23 or 0.995 < lm2d[15].y
        leftHandOffscreen = lm3d[16].y > 0.1 or lm3d[16].visibility < 0.23 or 0.995 < lm2d[16].y

        leftFootOffscreen = lm3d[23].y > 0.1 or lm3d[23].visibility < 0.63 or Hips["Hips"]["position"].z > -0.4
        rightFootOffscreen = lm3d[24].y > 0.1 or lm3d[24].visibility < 0.63 or Hips["Hips"]["position"].z > -0.4

        # Reset to default if offscreen
        Arms["UpperArm"]["l"] = Arms["UpperArm"]["l"].multiply(0 if leftHandOffscreen else 1)
        Arms["UpperArm"]["r"] = Arms["UpperArm"]["r"].multiply(0 if rightHandOffscreen else 1)

        Arms["LowerArm"]["l"] = Arms["LowerArm"]["l"].multiply(0 if leftHandOffscreen else 1)
        Arms["LowerArm"]["r"] = Arms["LowerArm"]["r"].multiply(0 if rightHandOffscreen else 1)

        Arms["Hand"]["l"] = Arms["Hand"]["l"].multiply(0 if leftHandOffscreen else 1)
        Arms["Hand"]["r"] = Arms["Hand"]["r"].multiply(0 if rightHandOffscreen else 1)

        # skip calculations if disable legs
        if Legs:
            Legs["UpperLeg"]["l"] = Legs["UpperLeg"]["l"].multiply(0 if rightFootOffscreen else 1)
            Legs["UpperLeg"]["r"] = Legs["UpperLeg"]["r"].multiply(0 if leftFootOffscreen else 1)
            Legs["LowerLeg"]["l"] = Legs["LowerLeg"]["l"].multiply(0 if rightFootOffscreen else 1)
            Legs["LowerLeg"]["r"] = Legs["LowerLeg"]["r"].multiply(0 if leftFootOffscreen else 1)

        return {
            # RightArm
            'RightUpperArm': Arms['UpperArm']['r'],  # Vector
            'RightLowerArm': Arms['LowerArm']['r'],  # Vector
            'RightHand': Arms['Hand']['r'],  # Vector
            # LeftArm
            'LeftUpperArm': Arms['UpperArm']['l'],  # Vector
            'LeftLowerArm': Arms['LowerArm']['l'],  # Vector
            'LeftHand': Arms['Hand']['l'],  # Vector
            # RightLeg
            'RightUpperLeg': Legs['UpperLeg']['r'] if Legs else RestingDefault['Pose']['RightUpperLeg'],  # Vector
            'RightLowerLeg': Legs['LowerLeg']['r'] if Legs else RestingDefault['Pose']['RightLowerLeg'],  # Vector
            # LeftLeg
            'LeftUpperLeg': Legs['UpperLeg']['l'] if Legs else RestingDefault['Pose']['LeftUpperLeg'],  # Vector
            'LeftLowerLeg': Legs['LowerLeg']['l'] if Legs else RestingDefault['Pose']['LeftLowerLeg'],  # Vector
            # Hips
            'Hips': Hips['Hips'],  # dict{ position: Vector, worldPosition: Vector, rotation: Vector}
            'Spine': Hips['Spine'],  # Vector
            'Unscaled': {
                # RightArm
                'RightUpperArm': Arms['Unscaled']['UpperArm']['l'],  # Vector
                'RightLowerArm': Arms['Unscaled']['LowerArm']['l'],  # Vector
                'RightHand': Arms['Unscaled']['Hand']['l'],  # Vector
                # LeftArm
                'LeftUpperArm': Arms['Unscaled']['UpperArm']['r'],  # Vector
                'LeftLowerArm': Arms['Unscaled']['LowerArm']['r'],  # Vector
                'LeftHand': Arms['Unscaled']['Hand']['r'],  # Vector
                # RightLeg
                'RightUpperLeg': Legs['Unscaled']['UpperLeg']['l'] if Legs else RestingDefault['Pose']['RightUpperLeg'],  # Vector
                'RightLowerLeg': Legs['Unscaled']['LowerLeg']['l'] if Legs else RestingDefault['Pose']['RightLowerLeg'],  # Vector
                # LeftLeg
                'LeftUpperLeg': Legs['Unscaled']['UpperLeg']['r'] if Legs else RestingDefault['Pose']['LeftUpperLeg'],  # Vector
                'LeftLowerLeg': Legs['Unscaled']['LowerLeg']['r'] if Legs else RestingDefault['Pose']['LeftLowerLeg'],  # Vector
            }
        }
