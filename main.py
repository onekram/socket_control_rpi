import time
from color import Color
import functions as f
import camera
import hand
import movement as m
from hand import put_down
from servokind import ServoKind
from object_camera import follow_object

if __name__ == "__main__":
    s = f.create_connect()
    follow_object(s)
