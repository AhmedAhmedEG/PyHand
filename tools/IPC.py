# win32Pipe
# https://stackoverflow.com/questions/48542644/python-and-windows-named-pipes
from itertools import cycle

import numpy as np
import pywintypes
import struct
import time
import win32con
import win32file
import win32pipe

from Calculations import scale


def encode(curls, splays, joys, bools):
    """ Struct format is from: https://github.com/LucidVR/opengloves-driver/wiki/Driver-Input#opengloves-input-methods
    const std::array<std::array<float, 4>, 5> flexion; // Between 0 and 1
    const std::array<float, 5> splay; // Between -1 and 1
    const float joyX; // Between -1 and 1
    const float joyY; // Between -1 and 1
    const bool joyButton; // 0
    const bool trgButton; // 1
    const bool aButton;   // 2
    const bool bButton;   // 3
    const bool grab;      // 4
    const bool pinch;     // 5
    const bool menu;      // 6
    const bool calibrate; // 7
    
    const float trgValue; // between 0 - 1 
    """
    if splays is None:
        splays = [scale(np.mean(f), 0, 1, -1, 1) for f in zip(curls[0::4], curls[1::4], curls[2::4], curls[3::4])]

    if joys is None:
        joys = [0.0] * 2

    if bools is None:
        bools = [False] * 8

    # https://tuttlem.github.io/2016/04/06/packing-data-with-python.html
    packed_curls = struct.pack('@20f', *curls)
    packed_splays = struct.pack('@5f', *splays)
    packed_joys = struct.pack('@2f', *joys)
    packed_bools = struct.pack('@8?', *bools)
    packed_trg = struct.pack('@f', (curls[4] + curls[5] + curls[6] + curls[7]) / 4)

    return packed_curls + packed_splays + packed_joys + packed_bools + packed_trg


class NamedPipe:
    def __init__(self, right_hand=True):
        if right_hand:
            # OpenGloves /named-pipe-communication-manager/src/DeviceProvider.cpp#L77
            self.pipe_name = r'\\.\pipe\vrapplication\input\glove\v2\right'

        else:
            self.pipe_name = r'\\.\pipe\vrapplication\input\glove\v2\left'

        while True:

            try:
                # https://github.com/LucidVR/opengloves-driver/blob/develop/overlay/main.cpp#L128
                open_mode = win32con.GENERIC_READ | win32con.GENERIC_WRITE

                self.pipe = win32file.CreateFile(self.pipe_name,
                                                 open_mode,
                                                 0,  # no sharing
                                                 None,  # default security
                                                 win32con.OPEN_EXISTING,
                                                 0,  # win32con.FILE_FLAG_OVERLAPPED,
                                                 None)

                win32pipe.SetNamedPipeHandleState(self.pipe,
                                                  win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_READMODE_BYTE | win32pipe.PIPE_WAIT,
                                                  None,
                                                  None)
                break

            except pywintypes.error:
                print("Pipe busy")
                time.sleep(0.1)

    def send(self, curls, splays=None, joys=None, bools=None):
        encoded = encode(curls, splays, joys, bools)
        win32file.WriteFile(self.pipe, encoded)


if __name__ == "__main__":
    ipc_right = NamedPipe()
    ipc_left = NamedPipe(right_hand=False)

    try:
        values = np.arange(-1, 1, 0.1)
        for i1 in cycle(values):

            for i2 in values:

                for i3 in values:

                    for i4 in values:

                        for i5 in values:
                            curls = [i1, i1, i1, i1, i2, i2, i2, i2, i3, i3, i3, i3, i4, i4, i4, i4, i5, i5, i5, i5]
                            splays = [i1, i2, i3, i4, i5]

                            ipc_left.send(curls, splays=splays)
                            ipc_right.send(curls, splays=splays)

                            time.sleep(0.01)

                            print(f"Wrote {splays} to IPC")


    except KeyboardInterrupt:
        print("Quitting")
        quit()
