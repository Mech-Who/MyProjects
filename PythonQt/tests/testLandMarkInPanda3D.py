from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
import cv2
import mediapipe as mp


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Load image
        img = cv2.imread("C:/Users/HP/Pictures/Camera Roll/test2.jpg")

        # Initialize holistic module
        mp_holistic = mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        # Detect pose landmarks
        results = mp_holistic.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # Get pose landmarks
        pose_landmarks = results.pose_landmarks
        if pose_landmarks is None:
            print("No pose landmarks detected.")
            return

        # Convert pose landmarks to world landmarks
        pose_world_landmark = [LVecBase3f(lm.x, lm.z, -lm.y) for lm in results.pose_world_landmarks.landmark]

        # Create a NodePath to hold the line segments
        line_segments = GeomNode("line_segments")

        # Create a white material for the lines
        white = Material()
        white.setDiffuse((1, 1, 1, 1))
        white.setSpecular((1, 1, 1, 1))
        white.setShininess(1)

        # Add line segments between adjacent pose landmarks
        for i in range(len(pose_world_landmark) - 1):
            line = LineSegs()
            line.setThickness(5)
            line.setColor(1, 1, 1, 1)
            line.moveTo(pose_world_landmark[i])
            line.drawTo(pose_world_landmark[i + 1])
            line_geom = line.create()
            # line_geom_node = GeomNode("line_geom")
            # line_geom_node.addGeom(line_geom)
            # line_geom_node.setMaterial(white)
            # line_segments.addGeom(line_geom.getGeom(0))

            # Create a NodePath to hold the line segments and attach it to the render
            # line_segments_np = self.render.attachNewNode(line_segments)
            line_segments_np = self.render.attachNewNode(line_geom)

            # Set the camera position and look at the center of the line segments
            # center = line_segments_np.getCenter()
            bounds = line_segments_np.getTightBounds(self.render)
            center = (bounds[0] + bounds[1]) / 2

            self.camera.setPos(center.getX(), center.getY() - 20, center.getZ())
            self.camera.lookAt(center)

        # Run the Panda3D main loop
        self.run()

if __name__ == "__main__":
    # Start the application
    app = MyApp()
