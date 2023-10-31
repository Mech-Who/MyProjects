from panda3d.core import *
from direct.actor.Actor import Actor
from direct.directbase import TestStart

from math import sin, pi

from mocap import MotionCapture

panda = Actor("panda-model.egg")
panda.reparent_to(base.render)
panda.set_scale(0.05)
panda.list_joints()

hips = panda.control_joint(None, "modelRoot", "Dummy_hips")

mocap = MotionCapture(panda)

# Capture the hips rotating
for i in range(100):
    t = (i / 100.0) * pi * 2

    hips.set_h(sin(t) * 45)
    mocap.capture_frame()

# Release the joint so we will see our new animation on it
panda.release_joint("modelRoot", "Dummy_hips")

# Package it up in an animation and load it into the Actor
node = AnimBundleNode("twerk", mocap.make_anim_bundle("twerk", fps=48))
panda.load_anims({"twerk": NodePath(node)})

panda.loop("twerk")

base.cam.set_y(-100)
base.run()
