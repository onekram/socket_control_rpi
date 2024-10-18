import logging
import time

import cv2
from parse_objects_camera.get_res_neural import get_result_yolo
from ultralytics import YOLO
from servo.hand import fall
from parse_objects_camera.objectkind import ObjectKind
import functions as f
from movement import *
from servo import add_functions as sf


DRAW = True

DELAY_SECONDS = 0.1
SPEED_FORWARD = 45
SPEED_TURN = 30

def hand_fall(s):
    fall(s)
    time.sleep(2)
    sf.start(s)
    #turn_to_put_hand_position(cap, type_button)
    #time.sleep(1)
    #fall(s)
    #time.sleep(2)
    #sf.start(s)


def draw_info(frame, x, y, w, h):
    cv2.putText(frame, f"x={x}, y = {y}, size={w * h}", (x - w // 2, y - h // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (139, 0, 255), 2)
    cv2.rectangle(frame, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (139, 0, 255), 2)


def turn_to_fall_hand_position(onnx_model, cap, s, type_button):
    d_x = 100
    while True:
        ret, frame = cap.read()
        if ret:
            res = get_result_yolo(onnx_model, frame, type_button)
            if res is not None:
                x, y, w, h = res.xywh[0]
                x, y, w, h = int(x), int(y), int(w), int(h)
                if DRAW:
                    draw_info(frame, x, y, w, h)
                set_speed(s, SPEED_TURN)
                if x < d_x - 50:
                    turn_to_left_without_stop(s)
                elif x > d_x + 50:
                    turn_to_right_without_stop(s)
                else:
                    stop(s)
                    break
            else:
                stop(s)
            if DRAW:
                cv2.imshow("Button_tracking", frame)
                cv2.waitKey(1)

def follow_object_button(onnx_model, s, type_button):
    d_x = 250
    obj_size = 34000
    cap = cv2.VideoCapture("http://192.168.2.99:8080/?action=stream")  # Открываем видеопоток с камеры
    cap.set(3, 480)  # Устанавливаем ширину изображения в 320 пикселей
    cap.set(4, 320)  # Устанавливаем высоту изображения в 320 пикселей
    border = 100
    while True:  # Бесконечный цикл
        ret, frame = cap.read()  # Считываем кадр с камеры
        if not ret:
            print("Error: Could not read frame.")
            break
        res = get_result_yolo(onnx_model, frame, type_button)
        if res is not None:
             x, y, w, h = res.xywh[0]
             x, y, w, h = int(x), int(y), int(w), int(h)
             if DRAW:
                 draw_info(frame, x, y, w, h)
             if x < d_x - border:
                 set_speed(s, SPEED_TURN)
                 turn_to_left_without_stop(s)
             elif x > d_x + border:
                 set_speed(s,  SPEED_TURN)
                 turn_to_right_without_stop(s)
             else:
                 if w * h < obj_size:
                     set_speed(s, SPEED_FORWARD)
                     forward_time_without_stop(s)
                 else:
                     stop(s)
                     break
        else:
            stop(s)
        if DRAW:
            cv2.imshow("Button_tracking", frame)
            cv2.waitKey(1)
    turn_to_fall_hand_position(onnx_model, cap, s, type_button)
    hand_fall(s)
    cap.release()
    if DRAW:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    logging.disable(logging.FATAL)
    onnx_model = YOLO('web_cam_model_v2.onnx')
    s = f.create_connect()

    sf.start(s)
    follow_object_button(onnx_model, s, ObjectKind.BLUE_BUTTON)
