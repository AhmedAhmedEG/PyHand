from tools.HandTrackingModule import *
from tools.Calculations import *

cap = cv2.VideoCapture(1)
detector = HandDetector(detectionCon=0.9, maxHands=1, stablizerVal=5)
plotter = Vector3DPlotter()

while True:
    _, frame = cap.read()
    hands, frame = detector.findHands(frame)

    if hands:
        points = np.array(hands[0]["lmList"])
        fingers = [f for f in zip(points[1::4], points[2::4], points[3::4], points[4::4])]

        frame = draw_curls(frame, points, fingers=[1, 1, 1, 1, 1])

        plotter.add_local_axis(fingers[1][0] - points[0], fingers[4][0] - points[0])

        a, b = fingers[1][0:2]
        ab = b - a
        plotter.add_vector(ab)

        plotter.plot()


    cv2.imshow("Image", frame)
    cv2.waitKey(1)