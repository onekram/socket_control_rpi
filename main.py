import logging
import time

import cv2

from color import Color
from functions import set_color
#from parse_objects_camera.ball_neural import follow_object_ball
#from parse_objects_camera.get_res_neural import get_result_yolo
from ultralytics import YOLO
from servo.hand import fall, put_down
#from parse_objects_camera.objectkind import ObjectKind
import functions as f
from movement import *
from servo import add_functions as sf

if __name__ == "__main__":
    s = f.create_connect()
    #set_color(s, Color.GREEN)
    sf.start(s)
    for i in range(1):
        set_speed(s, 70)
        forward_dist(s, 10)
        time.sleep(0.5)
        #set_speed(s, 50)
        #turn_left_angle(s,90)
        #time.sleep(0.5)
    #turn_left_corner(s, 90)
    #{0: 'ball', 1: 'basket', 2: 'blue_button', 3: 'cube', 4: 'green_button', 5: 'robot'}

