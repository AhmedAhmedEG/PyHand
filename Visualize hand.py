from tools.HandTrackingModule import *
from Calculations import *

cap = cv2.VideoCapture(1)
detector = HandDetector(detectionCon=0.9, maxHands=1, stablizerVal=5)
plotter = Vector3DPlotter()
plotter.normalize = False
plotter.title = "Hand Visualization"

while True:
    _, frame = cap.read()
    hands, frame = detector.findHands(frame)

    if hands:
        points = np.array(hands[0]["lmList"])
        frame = draw_curls(frame, points, fingers=[1, 1, 1, 1, 1])

        fingers = [f for f in zip(points[1::4], points[2::4], points[3::4], points[4::4])]

        #Drawing the hand
        for f in fingers:
            plotter.add_vector(f[0] - points[0], start=points[0])
            plotter.add_vector(f[1] - f[0], start=f[0])
            plotter.add_vector(f[2] - f[1], start=f[1])
            plotter.add_vector(f[3] - f[2], start=f[2])

        for i in range(1, 4):
            plotter.add_vector(fingers[i][0] - fingers[i + 1][0], start=fingers[i + 1][0])

        #Draw Hand Relative Axis
        plotter.add_local_axis(fingers[1][0] - points[0], fingers[4][0] - points[0], start=points[0])

        plotter.plot()

    cv2.imshow("Image", frame)
    cv2.waitKey(1)