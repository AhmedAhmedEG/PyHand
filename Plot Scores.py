from matplotlib import pyplot as plt
import pickle
import sys
import os

if not os.path.isfile("data/constraints.pkl"):
    print("Run the calibration script first.")
    sys.exit(0)

with open("data/angle_scores.pkl", 'rb') as f:
    angle_scores = pickle.load(f)

c = 1
for k in angle_scores:

    for i, j in enumerate(angle_scores[k]):
        plt.subplot(3, 5, c)
        plt.scatter(range(len(j)), j, c=j, cmap="coolwarm")

        plt.title(f"{k[0].capitalize()}{k[1:]} {i}")
        plt.xlabel("Reading")
        plt.ylabel("Angle")
        # plt.ylim(0, 180)
        c += 1

plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.6)
plt.show()