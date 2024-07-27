import numpy as np
import math


class Quaternion:
    def __init__(self, w=None, x=None, y=None, z=None):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def updateFromRawData(self, data=None):
        self.w = data["Quat1"]
        self.x = data["Quat2"]
        self.y = data["Quat3"]
        self.z = data["Quat4"]

    def __str__(self):
        return f"Quaternion({self.w}, {self.x}, {self.y}, {self.z})"

    def TrunkSwayAngle(self):
        """
        This will calculate the Rotation Z->Y->Z for a node that that is switch pointing up.
        Note: This is about the z-axis (axis out of IMU board)
        """
        # case zyz, Rotation sequence: Z->Y->Z
        t0 = 2 * (self.y * self.z + self.w * self.x)
        t1 = -2 * (self.x * self.z - self.w * self.y)

        sway = np.arctan2(t0, t1)  # in radians
        verticalsway = (sway * 180 / 3.14159 + 90)  # in deg and adjusted for keeping the sensor vertical

        # this_angle is corresponding to the sway angle when the sensor is kept vertical with switch pointing up
        return verticalsway
