import time


from color import Color

import functions as f
from servo import hand, camera


def start(s):
    camera.start_position(s)
    hand.start_position(s)

if __name__ == "__main__":
    s = f.create_connect()
    camera.start_position(s)
    hand.start_position(s)
    #time.sleep(1)
    #hand.prepare(s)
    #time.sleep(1)
    #hand.catch(s)
    #time.sleep(1)
    #hand.hold(s)
    #time.sleep(1)
    #hand.put_down(s)
