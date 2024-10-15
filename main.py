
import functions as f
import camera
import hand
from movement import forward_dist
from servokind import ServoKind
if __name__ == "__main__":
    s = f.create_connect()
    f.set_speed(s, 50)
    forward_dist(s, 2.3)
