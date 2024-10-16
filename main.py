import time

<<<<<<< Updated upstream
=======
from camera import start_position
from color import Color
>>>>>>> Stashed changes
import functions as f
from servo import hand, camera

if __name__ == "__main__":
    s = f.create_connect()
<<<<<<< Updated upstream
    # follow_object(s)
    camera.start_position(s)
    hand.start_position(s)
    # time.sleep(2)
    # hand.catch(s)
    # time.sleep(2)
    # hand.hold(s)
    # camera.start_position(s)
=======
    start_position(s)
    #follow_object(s)
>>>>>>> Stashed changes
