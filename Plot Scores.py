import matplotlib.pyplot as plt
import pickle
import sys
import os

if not os.path.isfile("data/curl_scores.pkl"):
    print("Run the calibration script first.")
    sys.exit(0)

with open("data/curl_scores.pkl", 'rb') as f:
    curl_scores = pickle.load(f)

with open("data/splay_scores.pkl", 'rb') as f:
    splay_scores = pickle.load(f)

c = 1
constraints = {"curls": {}, "splays": {}}
testing = True
for k in curl_scores:

    for i, j in enumerate(curl_scores[k]):
        plt.subplot(5, 4, c)

        plt.scatter(range(len(j)), j, c=j, cmap="coolwarm")
        plt.title(f"{k[0].capitalize()}{k[1:]} {i}")
        plt.xlabel("Reading")
        plt.ylabel("Angle")
        c += 1

    plt.subplot(5, 4, c)
    j = splay_scores[k]
    plt.scatter(range(len(j)), j, c=j, cmap="coolwarm")

    plt.title(f"{k[0].capitalize()}{k[1:]} Splay")
    plt.xlabel("Reading")
    plt.ylabel("Angle")
    c += 1

if not testing:

    for k in curl_scores.keys():
        constraints["curls"][k] = []

        for i in curl_scores[k]:
            mn, mx = min(i, default=0), max(i, default=0)
            constraints["curls"][k].append([mn, mx])

    for k in splay_scores.keys():
        i = splay_scores[k]
        mn, mx = min(i, default=0), max(i, default=0)
        constraints["splays"][k] = [mn, mx]

    with open("data/constraints.pkl", "wb") as f:
        pickle.dump(constraints, f)

plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.8)
plt.show()