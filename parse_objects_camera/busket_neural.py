import logging
import time

import cv2

from parse_objects_camera.ball_neural import work_ball
from parse_objects_camera.cube_neural import work_cube
from parse_objects_camera.get_res_neural import get_result_yolo
from ultralytics import YOLO
from servo.hand import fall, put_down
from parse_objects_camera.objectkind import ObjectKind
import functions as f
from movement import *
from servo import add_functions as sf
from cube_neural import follow_object_cube
from constants import *




def draw_info(frame, x, y, w, h):
    cv2.putText(frame, f"x={x}, y = {y}, size={w * h}", (x - w // 2, y - h // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (139, 0, 255), 2)
    cv2.rectangle(frame, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (139, 0, 255), 2)

def turn_to_put_hand_position(onnx_model, cap, s, type_basket):
    d_x = 130
    while True:
        ret, frame = cap.read()
        if ret:
            res = get_result_yolo(onnx_model, frame, type_basket)
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


def follow_object_basket(onnx_model, type_basket):
    d_x = 250
    obj_size = 100000
    cnt_not_obj = 0
    cap = cv2.VideoCapture(f"http://{HOST}:8080/?action=stream")  # Открываем видеопоток с камеры
    cap.set(3, 320)  # Устанавливаем ширину изображения в 320 пикселей
    cap.set(4, 320)  # Устанавливаем высоту изображения в 320 пикселей
    border = 100
    while True:  # Бесконечный цикл
        ret, frame = cap.read()  # Считываем кадр с камеры
        if not ret:
            print("Error: Could not read frame.")
            break
        res = get_result_yolo(onnx_model, frame, type_basket)
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
                 # старая версия
                 # 260 + 40 * (w * h < obj_size)
                 # новая версия
                 if y < 280:
                     set_speed(s, SPEED_FORWARD)
                     forward_without_stop(s)
                 else:
                     stop(s)
                     break

        else:
            stop(s)
            cnt_not_obj += 1
        if cnt_not_obj > CNT_FRAME_NOT_OBJ:
            cap.release()
            return
        if DRAW:
            cv2.imshow("Image", frame)
            cv2.waitKey(1)
    turn_to_put_hand_position(onnx_model, cap, s, type_basket)
    put_down(s)
    cap.release()
    if DRAW:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    logging.disable(logging.FATAL)
    first_onnx_model = YOLO('web_cam_model_v2.onnx')
    s = f.create_connect()

    sf.start(s)
    work_ball(first_onnx_model, s)
    follow_object_basket(first_onnx_model, ObjectKind.RED_BASKET)
