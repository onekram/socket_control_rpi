import logging
import time

import cv2

from color import Color
from functions import set_color
from parse_objects_camera.ball_neural import work_ball
from parse_objects_camera.cube_neural import work_cube

from parse_objects_camera.button_neural import follow_object_button
#from parse_objects_camera.get_res_neural import get_result_yolo
from ultralytics import YOLO

from parse_objects_camera.objectkind import ObjectKind
#from servo.hand import fall, put_down, prepare_bird_eye
#from parse_objects_camera.objectkind import ObjectKind
import functions as f
from movement import *
from servo import add_functions as sf
def first_point(s):
    set_speed(s, 50)
    turn_right_angle(s, 90)
    time.sleep(1)
    set_speed(s, 70)
    forward_dist(s, 35)
    time.sleep(1)
    set_speed(s, 50)
    turn_left_angle(s, 86)

def next_pos(onnx_model, s):
    time.sleep(0.5)
    set_speed(s, 50)
    turn_left_angle(s, 90)
    time.sleep(0.5)
    set_speed(s, 70)
    forward_dist(s, 60)
    time.sleep(0.5)
    set_speed(s, 50)
    turn_right_angle(s, 90)
    time.sleep(0.5)
    set_speed(s, 70)
    forward_dist(s, 70)
    time.sleep(0.5)
    set_speed(s, 50)
    turn_right_angle(s, 95)




#if w
def forward_point(onnx_model, s):
    set_speed(s, 70)
    forward_dist(s, 130)
    time.sleep(0.5)
    set_speed(s, 50)
    turn_right_angle(s, 95)
    time.sleep(0.5)
    set_speed(s, 70)
    forward_dist(s, 70)
    time.sleep(0.5)
    set_speed(s, 50)
    turn_left_angle(s, 10)
    res = work_ball(onnx_model, s)
    if not res:
        next_pos(onnx_model, s)


#if h
def right_point(onnx_model, s):
    set_speed(s, 50)
    turn_right_angle(s, 95)
    time.sleep(0.5)
    set_speed(s, 70)
    forward_dist(s, 110)

    time.sleep(0.5)
    set_speed(s, 50)
    turn_left_angle(s, 50)
    time.sleep(0.5)
    set_speed(s, 70)
    forward_dist(s, 50)
    time.sleep(0.5)
    set_speed(s, 50)
    turn_left_angle(s, 40)
    res = work_ball(onnx_model, s)
    print(res)

def to_button(s):
    set_speed(s, 50)
    turn_right_angle(s, 90)
    time.sleep(0.5)
    set_speed(s, 70)
    forward_dist(s, 100)
    time.sleep(0.5)
    set_speed(s, 50)
    turn_right_angle(s, 50)
    follow_object_button(onnx_model, s, ObjectKind.BLUE_BUTTON)
    follow_object_button(onnx_model, s, ObjectKind.GREEN_BUTTON)
    set_speed(s, 50)
    turn_right_angle(s, 30)
    #time.sleep(0.5)
    follow_object_button(onnx_model, s, ObjectKind.BLUE_BUTTON)
    follow_object_button(onnx_model, s, ObjectKind.GREEN_BUTTON)
    # res = work_cube(onnx_model, s)
    # if res: return
    # set_speed(s, 50)
    # turn_right_angle(s, 15)
    # work_cube(onnx_model, s)

def catch_cub(s):
    # prepare_bird_eye(s)

    time.sleep(0.5)
    set_speed(s, 70)
    forward_dist(s, 170)
    time.sleep(0.5)
    set_speed(s, 40)
    #turn_left_angle(s, 20)
    res = work_cube(onnx_model, s)
    if res: return
    set_speed(s, 50)
    turn_left_angle(s, 40)
    res = work_cube(onnx_model, s)
    if res: return
    set_speed(s, 50)
    turn_right_angle(s, 80)
    work_cube(onnx_model, s)







logging.disable(logging.FATAL)
s = f.create_connect()
set_color(s, Color.GREEN)
onnx_model = YOLO('parse_objects_camera/web_cam_model_v2.onnx')
sf.start(s)
cube = True
time.sleep(0.5)
first_point(s)
time.sleep(0.5)


#catch_cub(s)
to_button(s)
#right_point(onnx_model, s)
#forward_point(onnx_model, s)
#{0: 'ball', 1: 'basket', 2: 'blue_button', 3: 'cube', 4: 'green_button', 5: 'robot'}

