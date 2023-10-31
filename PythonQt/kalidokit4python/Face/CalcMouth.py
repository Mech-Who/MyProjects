import kalidokit4python.Util.Vector as Vec
from kalidokit4python.Util.Vector import Vector
from kalidokit4python.Util.Helper import clamp, remap


def calcMouth(lm):
    """
    Calculate Mouth Shape
    :param lm: array of results from tfjs or mediapipe
    """
    # eye keypoints
    eyeInnerCornerL = Vector(lm[133])
    eyeInnerCornerR = Vector(lm[362])
    eyeOuterCornerL = Vector(lm[130])
    eyeOuterCornerR = Vector(lm[263])

    # eye keypoint distances
    eyeInnerDistance = eyeInnerCornerL.distance(eyeInnerCornerR)
    eyeOuterDistance = eyeOuterCornerL.distance(eyeOuterCornerR)

    # mouth keypoints
    upperInnerLip = Vector(lm[13])
    lowerInnerLip = Vector(lm[14])
    mouthCornerLeft = Vector(lm[61])
    mouthCornerRight = Vector(lm[291])

    # mouth keypoint distances
    mouthOpen = upperInnerLip.distance(lowerInnerLip)
    mouthWidth = mouthCornerLeft.distance(mouthCornerRight)

    # mouth open and mouth shape ratios
    # ratioXY = mouthWidth / mouthOpen
    ratioY = mouthOpen / eyeInnerDistance
    ratioX = mouthWidth / eyeOuterDistance

    # normalize and scale mouth open
    ratioY = remap(ratioY, 0.15, 0.7)

    # normalize and scale mouth shape
    ratioX = remap(ratioX, 0.45, 0.9)
    ratioX = (ratioX - 0.3) * 2

    # mouthX = remap(ratioX - 0.4, 0, 0.5)
    mouthX = ratioX
    mouthY = remap(mouthOpen / eyeInnerDistance, 0.17, 0.5)

    # Depricated: Change sensitivity due to facemesh and holistic have different point outputs.
    # fixFacemesh = 1.3 if runtime == "tfjs" else 0

    # ratioI = remap(mouthXY, 1.3 + fixFacemesh * 0.8, 2.6 + fixFacemesh) * remap(mouthY, 0, 1)
    ratioI = clamp(remap(mouthX, 0, 1) * 2 * remap(mouthY, 0.2, 0.7), 0, 1)
    ratioA = mouthY * 0.4 + mouthY * (1 - ratioI) * 0.6
    ratioU = mouthY * remap(1 - ratioI, 0, 0.3) * 0.1
    ratioE = remap(ratioU, 0.2, 1) * (1 - ratioI) * 0.3
    ratioO = (1 - ratioI) * remap(mouthY, 0.3, 1) * 0.4

    return {
        "x": ratioX or 0,
        "y": ratioY or 0,
        "shape": {
            "A": ratioA or 0,
            "E": ratioE or 0,
            "I": ratioI or 0,
            "O": ratioO or 0,
            "U": ratioU or 0
        }
    }
