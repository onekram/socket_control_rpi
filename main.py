import time

import functions as f
from servo import hand, camera

if __name__ == "__main__":
    s = f.create_connect()
    # follow_object(s)
    camera.start_position(s)
    hand.start_position(s)
    # time.sleep(2)
    # hand.catch(s)
    # time.sleep(2)
    # hand.hold(s)
    # camera.start_position(s)