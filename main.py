import functions as f
from servokind import ServoKind
import hand
if __name__ == "__main__":
    s = f.create_connect()
    f.move_servo(s, ServoKind.CAM_UD, 70)