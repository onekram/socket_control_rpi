import logging
import time

import cv2
from parse_objects_camera.get_res_neural import get_result_yolo
from ultralytics import YOLO
from servo.hand import *
from parse_objects_camera.objectkind import ObjectKind
import functions as f
from movement import *
from servo import add_functions as sf
from servo import hand
from constants import *


def hand_manip(s):
    prepare(s)
    time.sleep(1)
    #set_speed(s, SPEED_FORWARD)
    #forward_time(s, 0.1)
    time.sleep(1)
    catch_ball(s)
    time.sleep(1)
    hold(s)

def draw_info(frame, x, y, w, h):
    cv2.putText(frame, f"x={x}, y = {y}, size={w * h}", (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 0), 2)
    cv2.rectangle(frame, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (255, 255, 255), 2)

def turn_to_catch_position(onnx_model, cap, s):
    d_x = 80
    while True:
        ret, frame = cap.read()
        if ret:
            res = get_result_yolo(onnx_model, frame, ObjectKind.BALL)
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
                cv2.imshow("Image", frame)
                cv2.waitKey(1)

def follow_object_ball(onnx_model, s):
    start_position_before_follow_ball(s)
    d_x = 200
    obj_size = 14500
    cap = cv2.VideoCapture(f"http://{HOST}:8080/?action=stream")  # Открываем видеопоток с камеры
    cap.set(3, 320)  # Устанавливаем ширину изображения в 320 пикселей
    cap.set(4, 320)  # Устанавливаем высоту изображения в 320 пикселей
    border = 100
    while True:  # Бесконечный цикл
        ret, frame = cap.read()  # Считываем кадр с камеры
        if not ret:
            print("Error: Could not read frame.")
            break
        res = get_result_yolo(onnx_model, frame, ObjectKind.BALL)
        if res is not None:
             x, y, w, h = res.xywh[0]
             x, y, w, h = int(x), int(y), int(w), int(h)
             if DRAW:
                 draw_info(frame, x, y, w, h)
             if x < d_x - border:
                 set_speed(s, SPEED_TURN)
                 turn_to_left_without_stop(s)
             elif x > d_x + border:
                 set_speed(s, SPEED_TURN)
                 turn_to_right_without_stop(s)
             else:
                 if w * h < obj_size:
                     set_speed(s, SPEED_FORWARD)
                     forward_without_stop(s)
                 else:
                     stop(s)
                     break
        else:
            stop(s)
        if DRAW:
            cv2.imshow("Image", frame)
            cv2.waitKey(1)
    turn_to_catch_position(onnx_model, cap, s)
    hand_manip(s)
    cap.release()
    if DRAW:
        cv2.destroyAllWindows()

# полный цикл работы с мячиком
def work_ball(onnx_model, s):
    sf.start(s)

    follow_object_ball(onnx_model, s)
    while True:
        set_speed(s, SPEED_BACK)
        back_time(s, 1.5)
        time.sleep(2)
        cap = cv2.VideoCapture(f"http://{HOST}:8080/?action=stream")  # Открываем видеопоток с камеры
        cap.set(3, 320)  # Устанавливаем ширину изображения в 320 пикселей
        cap.set(4, 320)  # Устанавливаем высоту изображения в 320 пикселей
        ret, frame = cap.read()  # Считываем кадр с камеры
        if not ret:
            print("Error: Could not read frame.")
            return None
        res = get_result_yolo(onnx_model, frame, ObjectKind.BALL)
        cap.release()
        if DRAW:
            cv2.destroyAllWindows()
        if res is not None:
            x, y, w, h = res.xywh[0]
            x, y, w, h = int(x), int(y), int(w), int(h)
            if x < 100 and y < 50:
                return 0
        else:
            return 0
        follow_object_ball(onnx_model, s)


if __name__ == "__main__":
    logging.disable(logging.FATAL)
    onnx_model = YOLO('web_cam_model_v2.onnx')
    s = f.create_connect()
    #sf.start(s)
    work_ball(onnx_model, s)
    #follow_object_ball(onnx_model, s)
    time.sleep(2)
    hand.put_down(s)
