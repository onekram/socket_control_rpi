import logging
import time

from ultralytics import YOLO
import cv2
from servo.hand import *
from parse_objects_camera.objectkind import ObjectKind
import functions as f
from movement import *
from servo import functions as sf
import cv2



DELAY_SECONDS = 0.1

logging.disable(logging.FATAL)
onnx_model = YOLO('better_small.onnx')
MIN_SIZE = 300


# print(onnx_model.names)
def get_result_yolo(frame, tp: ObjectKind):
    results = onnx_model(frame)

    boxes = results[0].boxes

    # максимальная вероятность
    # отбираем объект по типу, если несколько возвращаем с максимальной вероятностью
    max_confidence = 0
    ind = -1
    for i in range(len(boxes)):
        if boxes.cls[i] == tp.value and int(boxes.xywh[i][3]) * int(boxes.xywh[i][2]) >= MIN_SIZE:
            if boxes.conf[i] > max_confidence:
                max_confidence = boxes.conf[i]
                ind = i
    if ind == -1:
        return None
    return boxes[ind]

def hand_manip():
    prepare(s)
    time.sleep(1)
    forward_time(s, 1.5)
    time.sleep(1)
    catch(s)
    time.sleep(1)
    hold(s)
    time.sleep(5)
    put_down(s)

def turn_to_catch_position(cap):
    d_x = 100
    while True:  # Бесконечный цикл
        ret, frame = cap.read()  # Считываем кадр с камеры
        if ret:
            res = get_result_yolo(frame, ObjectKind.CUBE)
            if res is not None:
                x, y, w, h = res.xywh[0]
                x, y, w, h = int(x), int(y), int(w), int(h)
                cv2.putText(frame, f"x={x}, y = {y}, size={w * h}", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 0), 2)
                cv2.rectangle(frame, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (255, 255, 255), 2)
                set_speed(s, 30)
                if x < d_x - 50:
                    turn_to_left_without_stop(s)
                elif x > d_x + 50:
                    turn_to_right_without_stop(s)
                else:
                    stop(s)
                    break

            else:
                stop(s)
            cv2.imshow("Image", frame)
    return



def follow_object_cube():
    d_x = 250
    obj_size = 15000
    cap = cv2.VideoCapture("http://192.168.2.99:8080/?action=stream")  # Открываем видеопоток с камеры
    cap.set(3, 320)  # Устанавливаем ширину изображения в 320 пикселей
    cap.set(4, 320)  # Устанавливаем высоту изображения в 320 пикселей
    border = 100
    while True:  # Бесконечный цикл
        ret, frame = cap.read()  # Считываем кадр с камеры
        if not ret:
            print("Error: Could not read frame.")
            break
        res = get_result_yolo(frame, ObjectKind.CUBE)
        if res is not None:
             x, y, w, h = res.xywh[0]
             x, y, w, h = int(x), int(y), int(w), int(h)
             cv2.putText(frame, f"x={x}, y = {y}, size={w * h}", (x, y),
                         cv2.FONT_HERSHEY_SIMPLEX,
                         1, (0, 0, 0), 2)
             cv2.rectangle(frame, (x - w//2, y - h //2), (x + w//2, y + h//2), (255, 255, 255), 2)
             if x < d_x - border:
                 set_speed(s, 30)
                 turn_to_left_without_stop(s)
             elif x > d_x + border:
                 set_speed(s, 30)
                 turn_to_right_without_stop(s)
             else:
                 if w * h < obj_size:
                     set_speed(s, 40)
                     forward_time_without_stop(s)
                 else:
                     stop(s)
                     break
        else:
            stop(s)
        cv2.imshow("Image", frame)
        cv2.waitKey(1)
    turn_to_catch_position(cap)
    hand_manip()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    s = f.create_connect()
    set_speed(s, 30)

    sf.start(s)
    follow_object_cube()
