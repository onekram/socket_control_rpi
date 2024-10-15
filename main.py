import time

import functions as f
import camera
import hand
import movement as m
from servokind import ServoKind
if __name__ == "__main__":
    s = f.create_connect()
    hand.catch(s)
    time.sleep(3)
    hand.hold(s)
