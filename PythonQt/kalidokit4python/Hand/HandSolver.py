import kalidokit4python.Util.Vector as Vec
from kalidokit4python.Util.Vector import Vector
from kalidokit4python.Util.Helper import clamp
from kalidokit4python.Util.Constants import RIGHT, LEFT, PI


class HandSolver:
    @staticmethod
    def rigFingers(hand, side=RIGHT):
        """
        Converts normalized rotation values into radians clamped by human limits
        :param {Object} hand : object of labeled joint with normalized rotation values
        :param {Side} side : left or right
        """
        # Invert modifier based on left vs right side
        invert = 1 if side == RIGHT else -1
        digits = ["Ring", "Index", "Little", "Thumb", "Middle"]
        segments = ["Proximal", "Intermediate", "Distal"]

        hand[side + "Wrist"].x = clamp(hand[side + "Wrist"].x * 2 * invert, -0.3, 0.3)  # twist
        hand[side + "Wrist"].y = clamp(
            hand[side + "Wrist"].y * 2.3,
            -1.2 if side == RIGHT else -0.6,
            0.6 if side == RIGHT else 1.6
        )
        hand[side + "Wrist"].z = hand[side + "Wrist"].z * -2.3 * invert  # left right

        for e in digits:
            for j in segments:
                trackedFinger = hand[side + e + j]
                if e == "Thumb":
                    # dampen thumb rotation depending on segment
                    dampener = Vector(
                        2.2 if j == "Proximal" else (0 if j == "Intermediate" else 0),
                        2.2 if j == "Proximal" else (0.7 if j == "Intermediate" else 1),
                        0.5 if j == "Proximal" else (0.5 if j == "Intermediate" else 0.5)
                    )

                    startPos = Vector(
                        1.2 if j == "Proximal" else (-0.2 if j == "Distal" else -0.2),
                        1.1 * invert if j == "Proximal" else (0.1 * invert if j == "Distal" else 0.1 * invert),
                        0.2 * invert if j == "Proximal" else (0.2 * invert if j == "Distal" else 0.2 * invert)
                    )
                    newThumb = Vector(0, 0, 0)
                    if j == "Proximal":
                        newThumb.z = clamp(
                            startPos.z + trackedFinger.z * -PI * dampener.z * invert,
                            -0.6 if side == RIGHT else -0.3,
                            0.3 if side == RIGHT else 0.6
                        )
                        newThumb.x = clamp(startPos.x + trackedFinger.z * -PI * dampener.x, -0.6, 0.3)
                        newThumb.y = clamp(
                            startPos.y + trackedFinger.z * -PI * dampener.y * invert,
                            -1 if side == RIGHT else -0.3,
                            0.3 if side == RIGHT else 1
                        )
                    else:
                        newThumb.z = clamp(startPos.z + trackedFinger.z * -PI * dampener.z * invert, -2, 2)
                        newThumb.x = clamp(startPos.x + trackedFinger.z * -PI * dampener.x, -2, 2)
                        newThumb.y = clamp(startPos.y + trackedFinger.z * -PI * dampener.y * invert, -2, 2)
                    trackedFinger.x = newThumb.x
                    trackedFinger.y = newThumb.y
                    trackedFinger.z = newThumb.z
                else:
                    # will document human limits later
                    trackedFinger.z = clamp(
                        trackedFinger.z * -PI * invert,
                        -PI if side == RIGHT else 0,
                        0 if side == RIGHT else PI
                    )
        return hand

    @staticmethod
    def solve(lm, side=RIGHT):
        """
        Calculates finger and wrist as euler rotations
        :param {Array} lm : array of 3D hand vectors from tfjs or mediapipe
        :param {Side} side: left or right
        """
        if lm is None:
            print("Need Hand landmarks!")
            return

        palm = (
            Vector(lm[0]),
            Vector(lm[17 if side == RIGHT else 5]),
            Vector(lm[5 if side == RIGHT else 17]),
        )
        hand_rotation = Vec.rollPitchYaw(palm[0], palm[1], palm[2])
        hand_rotation.y = hand_rotation.z
        hand_rotation.y -= 0.4

        Hand = {
            side + "Wrist": {"x": hand_rotation.x, "y": hand_rotation.y, "z": hand_rotation.z},
            side + "RingProximal": {"x": 0, "y": 0, "z": Vec.angleBetween3DCoords(lm[0], lm[13], lm[14])},
            side + "RingIntermediate": {"x": 0, "y": 0, "z": Vec.angleBetween3DCoords(lm[13], lm[14], lm[15])},
            side + "RingDistal": {"x": 0, "y": 0, "z": Vec.angleBetween3DCoords(lm[14], lm[15], lm[16])},
            side + "IndexProximal": {"x": 0, "y": 0, "z": Vec.angleBetween3DCoords(lm[0], lm[5], lm[6])},
            side + "IndexIntermediate": {"x": 0, "y": 0, "z": Vec.angleBetween3DCoords(lm[5], lm[6], lm[7])},
            side + "IndexDistal": {"x": 0, "y": 0, "z": Vec.angleBetween3DCoords(lm[6], lm[7], lm[8])},
            side + "MiddleProximal": {"x": 0, "y": 0, "z": Vec.angleBetween3DCoords(lm[0], lm[9], lm[10])},
            side + "MiddleIntermediate": {"x": 0, "y": 0, "z": Vec.angleBetween3DCoords(lm[9], lm[10], lm[11])},
            side + "MiddleDistal": {"x": 0, "y": 0, "z": Vec.angleBetween3DCoords(lm[10], lm[11], lm[12])}
        }

        Hand = HandSolver.rigFingers(Hand, side)

        return Hand

