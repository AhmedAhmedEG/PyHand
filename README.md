# Included Files
Calibration.py : You run this first, put your hand(s) in front of the camera until it detects it and keep flexing your fingers a couple of times, It will visualize and collect info about the max/min angles of all your finger joints and save it for correct scaling for OpenGloves driver input.

Plot Scores.py : Draws scatter plots for the angles of all your joints that was captured in the latest run of the calibration script.

VRHand.py : the main script, it visualizes and tracks your hand and talks directly to OpenGloves driver via NamedPipes.

# Requirements
Python 3.7+

pip install matplotlib numpy mediapipe cvzone

OpenGloves driver installed

# Note
Change the camera index in the scripts you want to use if your camera didn't work with them.
