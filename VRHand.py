from tools.HandTrackingModule import *
from tools.Calculations import *
from time import sleep
from tools import IPC
import numpy as np
import pickle
import atexit
import sys
import cv2
import os


#Takes all the joint angles (3 angles per finger) and store them in a way the OpenGloves driver can understand.
def encode_curls(curls, joints=3):
    result = []

    if joints == 2:
        result.extend([curls[2], curls[1], curls[2], 0.0])
        curls = curls[3:]

        for i, j, k in zip(curls[0::3], curls[1::3], curls[2::3]):
            result.extend([0.0, j, j, k])

    elif joints == 3:
        result.extend([curls[0], curls[1], curls[2], 0.0])
        curls = curls[3:]

        for i, j, k in zip(curls[0::3], curls[1::3], curls[2::3]):
            result.extend([0.0, i, j, k])

    return result


def clean():
    cap.release()
    cv2.destroyAllWindows()


atexit.register(clean)

if not os.path.isfile("data/constraints.pkl"):
    print("Run the calibration script first.")
    sys.exit(0)

with open("data/constraints.pkl", 'rb') as f:
    constraints = pickle.load(f)

cap = cv2.VideoCapture(1)
detector = HandDetector(detectionCon=0.8, minTrackCon=0.8, maxHands=1, stablizerVal=5)

l_controller = IPC.NamedPipe(right_hand=False)
r_controller = IPC.NamedPipe()

while True:
    _, frame = cap.read()
    hands, frame = detector.findHands(frame)

    for h in hands:
        points = np.array(h["lmList"])
        frame = draw_curls(frame, points)

        if h["type"] == "Left":
            l_hand_curls = calc_curls(points, c=constraints)
            l_controller.send(encode_curls(l_hand_curls))

        else:
            r_hand_curls = calc_curls(points, c=constraints)
            r_controller.send(encode_curls(r_hand_curls))

        sleep(0.01)

    cv2.imshow("Image", frame)
    cv2.waitKey(1)
