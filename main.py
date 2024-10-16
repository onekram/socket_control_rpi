import time


from color import Color

import functions as f
from photos_maker import photo_maker
from servo import hand, camera


if __name__ == "__main__":
    s = f.create_connect()
    camera.start_position(s)
    hand.prepare(s)
    photo_maker()
    #time.sleep(1)
    #hand.prepare(s)
    #time.sleep(1)
    #hand.catch(s)
    #time.sleep(1)
    #hand.hold(s)
    #time.sleep(1)
    #hand.put_down(s)
