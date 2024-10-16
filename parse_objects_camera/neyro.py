import logging

from ultralytics import YOLO
import cv2
from parse_objects_camera.objectkind import ObjectKind
import functions as f
from movement import *
import os
import cv2


# Run inference

logging.disable(logging.FATAL)
onnx_model = YOLO('better_small.onnx')
MIN_SIZE = 300


# print(onnx_model.names)
def get_result_yolo(frame, tp: ObjectKind):
    results = onnx_model(frame)

    #results[0].show()
    boxes = results[0].boxes
    coords = boxes.xywh
    classes = boxes.cls
    confidence = boxes.conf

    # максимальная вероятность
    # отбираем объект по типу, если несколько возвращаем с максимальной вероятностью
    max_confidence = 0
    ind = -1
    for i in range(len(boxes)):

        if boxes.cls[i] == tp.value and int(boxes.xywh[i][3]) * int(boxes.xywh[i][2]) >= MIN_SIZE:
            if boxes.conf[i] > max_confidence:
                max_confidence = boxes.conf[i]
                ind = i
    # print(ind)
    if ind == -1:
        return None
    return boxes[ind]




def follow_object_cube():
    # type_objects={0: 'ball', 1: 'blue_button', 2: 'cube', 3: 'green_basket', 4: 'green_button', 5: 'red_basket', 6: 'robot'}
    d_x = 250
    obj_size = 15000
    cap = cv2.VideoCapture("http://192.168.2.99:8080/?action=stream")  # Открываем видеопоток с камеры
    cap.set(3, 320)  # Устанавливаем ширину изображения в 320 пикселей
    cap.set(4, 320)  # Устанавливаем высоту изображения в 320 пикселей
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
                 cv2.rectangle(frame, (x - w//2, y - h //2), (x + w//2, y + h//2), (255, 255, 255), 2)
                 if x < d_x - 100:
                     turn_to_left_without_stop(s)
                 elif x > d_x + 100:
                     turn_to_right_without_stop(s)
                 else:
                     if w * h < obj_size:
                         forward_time_without_stop(s)
                     else:
                         stop(s)

            else:
                stop(s)
            cv2.imshow("Image", frame)
            k = cv2.waitKey(1)
            if k == 27:
                break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    s = f.create_connect()
    set_speed(s, 40)
    follow_object_cube()
