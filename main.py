import time

import functions as f
import camera
import hand
import movement as m
from hand import put_down
from servokind import ServoKind
if __name__ == "__main__":
    s = f.create_connect()

    hand.start_position(s)
