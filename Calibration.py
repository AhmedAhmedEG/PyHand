from tools.HandTrackingModule import *
from tools.Calculations import *
from datetime import datetime
from scipy.stats import stats
import cvzone
import pickle
import cv2

curl_scores = {"thumb": [[], [], []], "index": [[], [], []], "middle": [[], [], []], "ring": [[], [], []], "pinky": [[], [], []]}
splay_scores = {"thumb": [], "index": [], "middle": [], "ring": [], "pinky": []}
constraints = {"curls": {}, "splays": {}}

cap = cv2.VideoCapture(1)
detector = HandDetector(detectionCon=0.8, minTrackCon=0.8, maxHands=1)
testing = False

previous_time = datetime.now()
while True:
    _, frame = cap.read()
    hands, frame = detector.findHands(frame)

    if hands:

        for h in hands:
            points = np.array(h["lmList"])
            curls = calc_curls(points)
            splays = calc_splays(points)

            curls_frame = draw_curls(frame, points, fingers=[1, 1, 1, 1, 1])
            splays_frame = draw_splays(frame, points, fingers=[1, 1, 1, 1, 1])

            for key, i, j, k in zip(curl_scores.keys(), curls[0::3], curls[1::3], curls[2::3]):
                curl_scores[key][0].append(i)
                curl_scores[key][1].append(j)
                curl_scores[key][2].append(k)

            for key, i in zip(splay_scores.keys(), splays):
                splay_scores[key].append(i)

        if not testing and (datetime.now() - previous_time).seconds > 10:
            cap.release()
            cv2.destroyAllWindows()

            for k in curl_scores.keys():
                constraints["curls"][k] = []

                for i in curl_scores[k]:
                    z = np.abs(stats.zscore(i))
                    i = np.array(i)[z < 0.6]
                    mn, mx = min(i, default=0), max(i, default=0)
                    constraints["curls"][k].append([mn, mx])

            for k in splay_scores.keys():
                i = splay_scores[k]
                z = np.abs(stats.zscore(i))
                i = np.array(i)[z < 0.6]
                mn, mx = min(i, default=0), max(i, default=0)
                constraints["splays"][k] = [mn, mx]

            with open("data/constraints.pkl", "wb") as f:
                pickle.dump(constraints, f)

            with open("data/curl_scores.pkl", "wb") as f:
                pickle.dump(curl_scores, f)

            with open("data/splay_scores.pkl", "wb") as f:
                pickle.dump(splay_scores, f)

        frame = cvzone.stackImages([curls_frame, splays_frame], cols=2, scale=1)

    cv2.imshow("Curls", frame)
    cv2.waitKey(1)