# Included Files
Calibration.py : You run this first, put your hand(s) in front of the camera until it detects it and keep flexing your fingers a couple of times, It will visualize and collect info about the max/min angles of all your finger joints and save it for correct scaling for OpenGloves driver input.

Plot Scores.py : Draws scatter plots for the angles of all your joints that was captured in the latest run of the calibration script.

VRHand.py : the main script, it visualizes and tracks your hand and talks directly to OpenGloves driver via NamedPipes.

PyCurls.py : It holds all functions that are responsible for angle calculation and visualization.

IPC.py : It hold the code used to send data to OpenGloves's NamedPipe.

# Requirements
Python 3.7+

pip install matplotlib numpy mediapipe cvzone

OpenGloves driver installed

# Notes
Change the camera index in the scripts you want to use if your camera didn't work with them.

In the main VRHand.py, you can change the "joints" parameter in the "encode_curls()" function to 3 to get the real 3 angles per finger but it's not accurate currently, so you can better stick with 2 for now, this will make the 1nd and the 2nd joint angles the same per finger.

# Future Plans
Splay Calculation.

Orientation Calculation.

Using quaternions to calculate angles for better accuracy and avoiding gimble locks.

Either modding the OpenGloves driver to accept positional data or simulating a virual vive tracker and send positional data from it.
