import time


from color import Color

import functions as f
from servo import hand, camera

if __name__ == "__main__":
    s = f.create_connect()
    camera.start_position(s)
    hand.start_position(s)
