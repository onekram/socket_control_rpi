
import functions as f
import camera
import hand
from servokind import ServoKind
if __name__ == "__main__":
    s = f.create_connect()
    camera.start_position(s)
