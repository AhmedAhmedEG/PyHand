from cvzone.HandTrackingModule import HandDetector
from tools.PyCurl import *
from time import sleep
from tools import IPC
import numpy as np
import pickle
import atexit
import sys
import cv2
import os


#Takes all the joint angles (3 angles per finger) and store them in a way the OpenGloves driver can understand.
def encode_curls(curls, joints=2):
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
detector = HandDetector(detectionCon=0.95, maxHands=2)

previous_l_hand_curls = [0] * 15
previous_r_hand_curls = [0] * 15

l_controller = IPC.NamedPipe(right_hand=False)
r_controller = IPC.NamedPipe()

while True:
    success, frame = cap.read()
    hands, frame = detector.findHands(frame)

    for h in hands:
        frame = draw_angles(frame, h)

        if h["type"] == "Left":
            l_hand_curls = get_curls_using_angles(h, c=constraints)

            #Eliminate micro moves
            if not np.allclose(l_hand_curls, previous_l_hand_curls, atol=0.11):
                l_controller.send(encode_curls(l_hand_curls), splays=calc_splay(h))

            previous_l_hand_curls = l_hand_curls

        else:
            r_hand_curls = get_curls_using_angles(h, c=constraints)

            #Eliminate micro moves
            if not np.allclose(r_hand_curls, previous_r_hand_curls, atol=0.11):
                r_controller.send(encode_curls(r_hand_curls), splays=calc_splay(h))

            previous_r_hand_curls = r_hand_curls

        sleep(0.01)

    cv2.imshow("Image", frame)
    cv2.waitKey(1)

