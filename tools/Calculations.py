from math import ceil
import numpy as np
import cv2
from matplotlib import pyplot as plt


class Vector3DPlotter:

    def __init__(self, split_3d=False):
        self.local_axis = []
        self.vectors = []

        self.head_color = "blue"
        self.tail_color = "deepskyblue"
        self.title = "Vector Visualization"

        self.normalize = True
        self.split_3d = split_3d
        self.scaler = 30

        fig = plt.figure(figsize=(5, 5))
        fig.suptitle(self.title)
        if not self.split_3d:
            self.ax = fig.add_subplot(1, 1, 1, projection='3d')

        else:
            self.axx = fig.add_subplot(1, 3, 1)
            self.axy = fig.add_subplot(1, 3, 2)
            self.axz = fig.add_subplot(1, 3, 3)

    def add_local_axis(self, a, b, start=np.array([0, 0, 0])):
        lx, ly, lz = calc_axis(a, b, scaler=self.scaler)
        self.local_axis.append([[lx, ly, lz], start])

    def add_vector(self, v, start=np.array([0, 0, 0])):
        self.vectors.append([v, start])

    def plot(self):

        if not self.split_3d:
            self.ax.margins(0.1, 0.1, 0.1)

            for la, s in self.local_axis:
                color_map = {0: "red", 1: "green", 2: "blue"}

                for i, axis in enumerate(la):
                    x, y, z = list(zip(s, axis + s))
                    self.ax.scatter(x, y, z, c=color_map[i], marker="o")
                    self.ax.plot(x, y, z, c=color_map[i])

                    x, y, z = axis + s
                    self.ax.text(x, y, z, "+", color=color_map[i])

                    x, y, z = list(zip(s, -axis + s))
                    self.ax.scatter(x, y, z, c=color_map[i], marker="o")
                    self.ax.plot(x, y, z, c=color_map[i])

                    x, y, z = -axis + s
                    self.ax.text(x, y, z, "-", color=color_map[i])

            for v, s in self.vectors:

                if self.normalize:
                    v = v / np.linalg.norm(v) * self.scaler

                x, y, z = list(zip(s, v + s))
                self.ax.scatter(x, y, z, c="blue", marker=".")
                self.ax.plot(x, y, z, c="deepskyblue")

            plt.pause(0.01)
            self.local_axis = []
            self.vectors = []
            self.ax.cla()

        else:

            for i, ax in enumerate([self.axx, self.axy, self.axz]):

                for la, s in self.local_axis:
                    color_map = {0: "red", 1: "green", 2: "blue"}

                    if i == 0:
                        la = np.delete(la, 1, 1)
                        s = np.delete(s, 1, 0)

                    elif i == 1:
                        la = np.delete(la, 0, 1)
                        s = np.delete(s, 0, 0)

                    elif i == 2:
                        la = np.delete(la, 2, 1)
                        s = np.delete(s, 2, 0)

                    for j, axis in enumerate(la):
                        x, y = list(zip(s, axis + s))
                        ax.scatter(x, y, c=color_map[j], marker="o")
                        ax.plot(x, y, c=color_map[j])

                        x, y = axis + s
                        ax.text(x, y, "+", color=color_map[j])

                        x, y = list(zip(s, -axis + s))
                        ax.scatter(x, y, c=color_map[j], marker="o")
                        ax.plot(x, y, c=color_map[j])

                        x, y = -axis + s
                        ax.text(x, y, "-", color=color_map[j])

                for v, s in self.vectors:

                    if i == 0:
                        v = np.delete(v, 1, 0)
                        s = np.delete(s, 1, 0)

                    elif i == 1:
                        v = np.delete(v, 0, 0)
                        s = np.delete(s, 0, 0)

                    elif i == 2:
                        v = np.delete(v, 2, 0)
                        s = np.delete(s, 2, 0)

                    if self.normalize:
                        v = v / np.linalg.norm(v) * self.scaler

                    x, y = list(zip(s, v + s))
                    ax.scatter(x, y, c="blue", marker=".")
                    ax.plot(x, y, c="deepskyblue")

            plt.pause(0.01)
            self.local_axis = []
            self.vectors = []
            self.axx.cla()
            self.axy.cla()
            self.axz.cla()


def rgb_to_bgr(rgb):
    return [rgb[2], rgb[1], rgb[0]]


def calc_axis(a, b, scaler=30):
    lz = np.cross(a, b)
    lz = (lz / np.linalg.norm(lz)) * scaler

    lx = np.cross(a, lz)
    lx = (lx / np.linalg.norm(lx)) * scaler

    ly = np.cross(lx, lz)
    ly = (ly / np.linalg.norm(ly)) * scaler

    return [lx, ly, lz]


def draw_curls(frame, points, fingers=None):
    color_map = {0: (223, 246, 255), 1: (93, 139, 244), 2: (45, 49, 250)}

    if fingers is None:
        fingers = [1, 1, 1, 1, 1]

    joints = [[x, y] for x, y, z in [p for i, p in enumerate(points) if i % 4 != 0]]
    curls = calc_curls(points)
    frame = frame.copy()

    for i, p in enumerate(joints):
        p1 = p.copy()
        p2 = p.copy()
        offset = 0

        if i in [0, 1, 2]:

            if not fingers[0]:
                continue

            if joints[2][0] - joints[12][0] > 0:
                p2[0] += 100 + (i % 3) * 15
            else:
                p2[0] -= 100 + (i % 3) * 15
                offset = -35

        elif i in [3, 4, 5]:

            if not fingers[1]:
                continue

            if joints[2][0] - joints[12][0] > 0:
                p2[0] += 100 + (i % 3) * 15
            else:
                p2[0] -= 100 + (i % 3) * 15
                offset = -35

        elif i in [6, 7, 8]:

            if not fingers[2]:
                continue

            if joints[2][0] - joints[12][0] > 0:
                p2[0] += 120 + (i % 3) * 15
                p2[1] -= 100 + (i % 3) * 15
            else:
                p2[0] -= 120 + (i % 3) * 15
                p2[1] -= 100 + (i % 3) * 15
                offset = -35

        elif i in [9, 10, 11]:

            if not fingers[3]:
                continue

            if joints[2][0] - joints[12][0] > 0:
                p2[0] -= 120 + (i % 3) * 15
                p2[1] -= 100 + (i % 3) * 15
                offset = -35
            else:
                p2[0] += 120 + (i % 3) * 15
                p2[1] -= 100 + (i % 3) * 15

        elif i in [12, 13, 14]:

            if not fingers[4]:
                continue

            if joints[2][0] - joints[12][0] > 0:
                p2[0] -= 100 + (i % 3) * 15
                offset = -35
            else:
                p2[0] += 100 + (i % 3) * 15

        p3 = p2.copy()
        p3[0] += offset

        cv2.line(frame, p1, p2, rgb_to_bgr(color_map[i % 3]), 2)
        cv2.putText(frame, str(ceil(curls[i])), p3, cv2.FONT_HERSHEY_DUPLEX, 0.5, rgb_to_bgr(color_map[i % 3]), 1, cv2.LINE_AA)

    return frame


def draw_splays(frame, points, fingers=None):

    if fingers is None:
        fingers = [1, 1, 1, 1, 1]

    joints = [[x, y] for x, y, z in [points[i] for i in range(1, 21, 4)]]
    splays = calc_splays(points)
    frame = frame.copy()

    for i, p in enumerate(joints):
        p1 = p.copy()
        p2 = p.copy()
        offset = 0

        if i == 0:

            if not fingers[0]:
                continue

            if joints[0][0] - joints[4][0] > 0:
                p2[0] += 100
            else:
                p2[0] -= 100
                offset = -35

        elif i == 1:

            if not fingers[1]:
                continue

            if joints[0][0] - joints[4][0] > 0:
                p2[0] += 100
            else:
                p2[0] -= 100
                offset = -35

        elif i == 2:

            if not fingers[2]:
                continue

            if joints[0][0] - joints[4][0] > 0:
                p2[0] += 120
                p2[1] -= 100
            else:
                p2[0] -= 120
                p2[1] -= 100
                offset = -35

        elif i == 3:

            if not fingers[3]:
                continue

            if joints[0][0] - joints[4][0] > 0:
                p2[0] -= 120
                p2[1] -= 100
                offset = -35
            else:
                p2[0] += 120
                p2[1] -= 100

        elif i == 4:

            if not fingers[4]:
                continue

            if joints[0][0] - joints[4][0] > 0:
                p2[0] -= 100
                offset = -35
            else:
                p2[0] += 100

        p3 = p2.copy()
        p3[0] += offset

        cv2.line(frame, p1, p2, rgb_to_bgr([223, 246, 255]), 2)
        cv2.putText(frame, str(ceil(splays[i])), p3, cv2.FONT_HERSHEY_DUPLEX, 0.5, rgb_to_bgr([223, 246, 255]), 1, cv2.LINE_AA)

    return frame


def scale(x, mn1, mx1, mn2, mx2, inverse=False):

    if mx1 == 0:
        mx1 = 1

    if inverse:
        result = 1 - ((mx2 - mn2) * ((x - mn1) / (mx1 - mn1)) + mn2)

    else:
        result = ((mx2 - mn2) * (x - mn1) / (mx1 - mn1)) + mn2

    # Remove outlines
    if result > mx2:
        result = 1

    elif result < mn2:
        result = 0

    return result


def calc_angle(a, b):
    radians = np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    degrees = (radians * 180) / np.pi

    # Eliminate NaNs.
    if np.isnan(degrees):
        degrees = 0

    # # Eliminate obvious errors.
    # if degrees > 180:
    #     degrees = 180
    #
    # elif degrees < 0:
    #     degrees = 0

    return degrees


def calc_curls(points, c=None):
    fingers = [[p[0] - points[0], p[1] - p[0], p[2] - p[1], p[3] - p[2]] for p in zip(points[1::4], points[2::4], points[3::4], points[4::4])]
    lx, ly, lz = calc_axis(points[5] - points[0], points[17] - points[0])

    angles = []
    for f in fingers:
        angles.append(calc_angle(f[0], f[1]))
        angles.append(calc_angle(f[1], f[2]))
        angles.append(calc_angle(f[2], f[3]))

    if c is not None:
        flattened = [j for i in c["curls"].values() for j in i]
        angles = [scale(angles[i], j[0], j[1], 0, 1) for i, j in enumerate(flattened)]

    return angles


def calc_splays(points, c=None):
    points = np.array(points)
    fingers = [[p[0] - points[0], p[1] - p[0], p[2] - p[1], p[3] - p[2]] for p in zip(points[1::4], points[2::4], points[3::4], points[4::4])]
    lx, ly, lz = calc_axis(points[5] - points[0], points[17] - points[0])

    angles = [calc_angle(f[1], lx) for f in fingers]

    if c is not None:
        angles = [scale(angles[i], j[0], j[1], -1, 1) for i, j in enumerate(c["splays"].values())]

    return angles
