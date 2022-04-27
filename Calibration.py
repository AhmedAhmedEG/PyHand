from cvzone.HandTrackingModule import HandDetector
from tools.PyCurl import *
import atexit
import pickle
import cv2


def finish():
    cap.release()
    cv2.destroyAllWindows()

    with open("data/constraints.pkl", "wb") as f:
        pickle.dump(constraints, f)

    with open("data/angle_scores.pkl", "wb") as f:
        pickle.dump(angle_scores, f)


atexit.register(finish)

angle_scores = {"thumb": [[], [], []], "index": [[], [], []], "middle": [[], [], []], "ring": [[], [], []], "pinky": [[], [], []]}
distance_scores = {"thumb": [], "index": [], "middle": [], "ring": [], "pinky": []}
constraints = {}

cap = cv2.VideoCapture(1)
detector = HandDetector(detectionCon=0.9, maxHands=2)

while True:
    success, frame = cap.read()
    hands, frame = detector.findHands(frame)

    if hands:

        for h in hands:
            angles = get_curls_using_angles(h)
            frame = draw_angles(frame, h)

            for key, i, j, k in zip(angle_scores.keys(), angles[0::3], angles[1::3], angles[2::3]):
                angle_scores[key][0].append(i)
                angle_scores[key][1].append(j)
                angle_scores[key][2].append(k)

        for k in angle_scores.keys():

            constraints[k] = []
            for i in angle_scores[k]:
                mn, mx = min(i), max(i)
                constraints[k].append([mn, mx])

        # for h in hands:
        #     distances = get_curls_using_distances(h, detector)
        #
        #     for i, k in enumerate(distance_scores.keys()):
        #         distance_scores[k].append(distances[i])
        #
        # for k in distance_scores.keys():
        #     mn, mx = min(distance_scores[k]), max(distance_scores[k])
        #     constrains[k] = [mn, mx]

    cv2.imshow("Image", frame)
    cv2.waitKey(1)