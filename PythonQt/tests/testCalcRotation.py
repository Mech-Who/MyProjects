import numpy as np
from scipy.spatial.transform import Rotation

vector = np.array([1, 2, 3])
rotation = Rotation.from_rotvec(vector)
euler_angles = rotation.as_euler('xyz', degrees=True)
print(f"euler_angles:{euler_angles}")