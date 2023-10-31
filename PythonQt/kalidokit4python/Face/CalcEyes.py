import kalidokit4python.Util.Vector as Vec
from kalidokit4python.Util.Vector import Vector
from kalidokit4python.Util.Helper import clamp, remap
from kalidokit4python.Util.Constants import RIGHT, LEFT

# Landmark points labeled for eye, brow, and pupils
points = {
    "eye": {
        LEFT: [130, 133, 160, 159, 158, 144, 145, 153],
        RIGHT: [263, 362, 387, 386, 385, 373, 374, 380]
    },
    "brow": {
        LEFT: [35, 244, 63, 105, 66, 229, 230, 231],
        RIGHT: [265, 464, 293, 334, 296, 449, 450, 451]
    },
    "pupil": {
        LEFT: [468, 469, 470, 471, 472],
        RIGHT: [473, 474, 475, 476, 477]
    }
}


def eyeLidRatio(
        eyeOuterCorner,
        eyeInnerCorner,
        eyeOuterUpperLid,
        eyeMidUpperLid,
        eyeInnerUpperLid,
        eyeOuterLowerLid,
        eyeMidLowerLid,
        eyeInnerLowerLid
                ):
    """
    Calculate eyelid distance ratios based on landmarks on the face
    """
    eyeOuterCorner = Vector(eyeOuterCorner)
    eyeInnerCorner = Vector(eyeInnerCorner)

    eyeOuterUpperLid = Vector(eyeOuterUpperLid)
    eyeMidUpperLid = Vector(eyeMidUpperLid)
    eyeInnerUpperLid = Vector(eyeInnerUpperLid)

    eyeOuterLowerLid = Vector(eyeOuterLowerLid)
    eyeMidLowerLid = Vector(eyeMidLowerLid)
    eyeInnerLowerLid = Vector(eyeInnerLowerLid)

    # use 2D Distances instead of 3D for less jitter
    eyeWidth = eyeOuterCorner.distance(eyeInnerCorner, 2)
    eyeOuterLidDistance = eyeOuterUpperLid.distance(eyeOuterLowerLid, 2)
    eyeMidLidDistance = eyeMidUpperLid.distance(eyeMidLowerLid, 2)
    eyeInnerLidDistance = eyeInnerUpperLid.distance(eyeInnerLowerLid, 2)
    eyeLidAvg = (eyeOuterLidDistance + eyeMidLidDistance + eyeInnerLidDistance) / 3
    ratio = eyeLidAvg / eyeWidth

    return ratio


def getEyeOpen(lm, side=RIGHT, high=0.85, low=0.55):
    """
    Calculate eye open ratios and remap to 0-1
    :param lm: array of results from tfjs or mediapipe
    :param side: designate left or right
    :param high: ratio at which eye is considered open
    :param low: ratio at which eye is comsidered closed
    """
    eyePoints = points["eye"][side]
    eyeDistance = eyeLidRatio(
        lm[eyePoints[0]],
        lm[eyePoints[1]],
        lm[eyePoints[2]],
        lm[eyePoints[3]],
        lm[eyePoints[4]],
        lm[eyePoints[5]],
        lm[eyePoints[6]],
        lm[eyePoints[7]]
    )
    # human eye width to height ratio is roughly .3
    maxRatio = 0.285
    # compare ratio against max ratio
    ratio = clamp(eyeDistance / maxRatio, 0, 2)
    # remap eye open and close ratios to increase sensitivity
    eyeOpenRatio = remap(ratio, low, high)
    return {
        # remapped ratio
        "norm": eyeOpenRatio,
        # unmapped ratio
        "raw": ratio
    }


def pupilPos(lm, side=LEFT):
    """
    Calculate pupil position [-1,1]
    :param lm: array of results from tfjs or mediapipe
    :param side: left or right
    """
    eyeOuterCorner = Vector(lm[points["eye"][side][0]])
    eyeInnerCorner = Vector(lm[points["eye"][side][1]])
    eyeWidth = eyeOuterCorner.distance(eyeInnerCorner, 2)
    midPoint = eyeOuterCorner.lerp(eyeInnerCorner, 0.5)
    pupil = Vector(lm[points["pupil"][side][0]])
    dx = midPoint.x - pupil.x
    # eye center y is slightly above midpoint
    dy = midPoint.y - eyeWidth * 0.075 - pupil.y
    ratioX = dx / (eyeWidth / 2)
    ratioY = dy / (eyeWidth / 4)

    ratioX *= 4
    ratioY *= 4

    return {"x": ratioX, "y": ratioY}


def stabilizeBlink(eye, headY, enableWink=True, maxRot=0.5):
    """
    Method to stabilize blink speeds to fix inconsistent eye open/close timing
    :param eye: object with left and right eye values
    :param headY: head Y axis rotation in radians
    :param enableWink: Enable wink detection
    :param maxRot: Maximum rotation of head to trigger wink
    """
    eye.r = clamp(eye.r, 0, 1)
    eye.l = clamp(eye.l, 0, 1)
    # difference between each eye
    blinkDiff = abs(eye.l - eye.r)
    # threshold to which difference is considered a wink
    blinkThresh = 0.8 if enableWink else 1.2
    # detect when both eyes are closing
    isClosing = eye.l < 0.3 and eye.r < 0.3
    # detect when both eyes are opening
    isOpen = eye.l > 0.6 and eye.r > 0.6

    # sets obstructed eye to the opposite eye value
    if headY > maxRot:
        return {"l": eye.r, "r": eye.r}
    if headY < -maxRot:
        return {"l": eye.l, "r": eye.l}

    # returns either a wink or averaged blink values
    return {
        "l":
            eye.l if (blinkDiff >= blinkThresh) and (not isClosing) and (not isOpen) else (
                Vector.lerp(eye.r, eye.l, 0.95) if eye.r > eye.l else Vector.lerp(eye.r, eye.l, 0.05)),
        "r":
            eye.r if (blinkDiff >= blinkThresh) and (not isClosing) and (not isOpen) else (
                Vector.lerp(eye.r, eye.l, 0.95) if eye.r > eye.l else Vector.lerp(eye.r, eye.l, 0.05))
    }


def calcEyes(lm, high=0.85, low=0.55):
    """
    Calculate Eyes
    :param lm: array of results from tfjs or mediapipe
    :param high: Upper bound for eye open ratio
    :param low: Lower bound for eye open ratio
    """
    # return early if no iris tracking
    if lm.length != 478:
        return {
            "l": 1,
            "r": 1,
        }
    # open [0,1]
    leftEyeLid = getEyeOpen(lm, LEFT, high, low)
    rightEyeLid = getEyeOpen(lm, RIGHT, high, low)

    return {
        "l": leftEyeLid["norm"] or 0,
        "r": rightEyeLid["norm"] or 0
    }


def calcPupils(lm):
    """
    Calculate pupil location normalized to eye bounds
    :param lm: array of results from tfjs or mediapipe
    """
    if lm.length != 478:
        return {"x": 0, "y": 0}
    else:
        # track pupils using left eye
        pupilL = pupilPos(lm, LEFT)
        pupilR = pupilPos(lm, RIGHT)

    return {
        'x': (pupilL['x'] + pupilR['x']) * 0.5 or 0,
        'y': (pupilL['y'] + pupilR['y']) * 0.5 or 0,
    }


def getBrowRaise(lm, side=LEFT):
    """
    Calculate brow raise
    :param lm: array of results from tfjs or mediapipe
    :param side: designate left or right
    """
    browPoints = points["brow"][side]
    browDistance = eyeLidRatio(
        lm[browPoints[0]],
        lm[browPoints[1]],
        lm[browPoints[2]],
        lm[browPoints[3]],
        lm[browPoints[4]],
        lm[browPoints[5]],
        lm[browPoints[6]],
        lm[browPoints[7]]
    )
    maxBrowRatio = 1.15
    browHigh = 0.125
    browLow = 0.07
    browRatio = browDistance / maxBrowRatio - 1
    browRaiseRatio = (clamp(browRatio, browLow, browHigh) - browLow) / (browHigh - browLow)
    return browRaiseRatio


def calcBrow(lm):
    """
    Take the average of left and right eyebrow raise values
    :param lm: array of results from tfjs or mediapipe
    """
    if lm.length != 478:
        return 0
    else:
        leftBrow = getBrowRaise(lm, LEFT)
        rightBrow = getBrowRaise(lm, RIGHT)
        return (leftBrow + rightBrow) / 2 or 0
