from math import ceil
import numpy as np
import cv2


def draw_angles(frame, hand, fingers=None):
    color_map = {0: (255, 172, 166), 1: (114, 0, 4), 2: (47, 0, 2)}

    if fingers is None:
        fingers = [1, 1, 1, 1, 1]

    joints = [[x, y] for x, y, z in [p for i, p in enumerate(hand["lmList"]) if i % 4 != 0]]
    angles = get_curls_using_angles(hand)
    frame = frame.copy()

    for i, p in enumerate(joints):
        p1 = p.copy()
        p2 = p.copy()
        offset = 0

        if i in [0, 1, 2]:

            if not fingers[0]:
                continue

            if joints[2][0] - joints[12][0] > 0:
                p2[0] += 100
            else:
                p2[0] -= 100
                offset = -35

        elif i in [3, 4, 5]:

            if not fingers[1]:
                continue

            if joints[2][0] - joints[12][0] > 0:
                p2[0] += 100
            else:
                p2[0] -= 100
                offset = -35

        elif i in [6, 7, 8]:

            if not fingers[2]:
                continue

            if joints[2][0] - joints[12][0] > 0:
                p2[0] += 120
                p2[1] -= 100
            else:
                p2[0] -= 120
                p2[1] -= 100
                offset = -35

        elif i in [9, 10, 11]:

            if not fingers[3]:
                continue

            if joints[2][0] - joints[12][0] > 0:
                p2[0] -= 120
                p2[1] -= 100
                offset = -35
            else:
                p2[0] += 120
                p2[1] -= 100

        elif i in [12, 13, 14]:

            if not fingers[4]:
                continue

            if joints[2][0] - joints[12][0] > 0:
                p2[0] -= 100
                offset = -35
            else:
                p2[0] += 100

        p3 = p2.copy()
        p3[0] += offset

        cv2.line(frame, p1, p2, color_map[i % 3], 2)
        cv2.putText(frame, str(ceil(angles[i])), p3, cv2.FONT_HERSHEY_DUPLEX, 0.5, color_map[i % 3], 1, cv2.LINE_AA)

    return frame


def scale(x, mn, mx, inverse=False):

    if inverse:
        result = 1 - ((x - mn) / (mx - mn))

    else:
        result = (x - mn) / (mx - mn)

    #Remove outlines
    if result > 1:
        result = 180

    elif result < 0:
        result = 0

    return result


def calc_angle(a, b, c):

    #From https://stackoverflow.com/a/1354158/11769578
    ba = np.array([a[0] - b[0], a[1] - b[1], a[2] - b[2]])
    bc = np.array([c[0] - b[0], c[1] - b[1], c[2] - b[2]])

    radians = np.arccos(np.dot(ba, bc) / (np.sqrt(ba.dot(ba)) * np.sqrt(bc.dot(bc))))
    degrees = (radians * 180) / np.pi

    #Eliminate NaNs.
    if np.isnan(degrees):
        degrees = 0

    #Eliminate obvious errors.
    if degrees > 180:
        degrees = 180

    elif degrees < 0:
        degrees = 0

    # #From https://stackoverflow.com/a/31334882/11769578
    # a = np.array(a)
    # b = np.array(b)
    # c = np.array(c)
    #
    # radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    # degrees = (radians * 180) / np.pi
    #
    # #From https://stackoverflow.com/a/39673693/11769578
    # ba = np.array([a[0] - b[0], a[1] - b[1]])
    # bc = np.array([c[0] - b[0], c[1] - b[1]])
    #
    # numerator = ba[0] * bc[1] + ba[1] * bc[0]
    # denominator = ba[0] * bc[0] - ba[1] * bc[1]
    #
    # radians = np.arctan(numerator / denominator)
    # degrees = (radians * 180) / np.pi


    return degrees


def get_curls_using_angles(h, c=None):
    joints = h["lmList"]

    joint_groups = [[1, 0, 5], [1, 2, 3], [2, 3, 4],
                     [0, 5, 6], [5, 6, 7], [6, 7, 8],
                     [0, 9, 10], [9, 10, 11], [10, 11, 12],
                     [0, 13, 14], [13, 14, 15], [14, 15, 16],
                     [0, 17, 18], [17, 18, 19], [18, 19, 20]]

    angles = [calc_angle(joints[i], joints[j], joints[k]) for i, j, k in joint_groups]

    if c is not None:
        flattened = [j for i in c.values() for j in i]

        angles = [scale(angles[i], j[0], j[1], inverse=True) for i, j in enumerate(flattened)]

    return angles


def calc_splay(h):
    joints = h["lmList"]
    angles = scale(calc_angle(joints[1], joints[0], joints[5]), 40, 50)

    return [angles, angles, angles, angles, angles]


# def get_curls_using_distances(h, hd, c=None):
#     joints = h["lmList"]
#
#     distances = [hd.findDistance(joints[i], joints[i + 3]) for i in [1, 5, 9, 13, 17]]
#
#     if c is not None:
#         distances = [scale(distances[i], c[k][0], c[k][1], inverse=True) for i, k in enumerate(c.keys())]
#
#     return distances