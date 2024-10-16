from ultralytics import YOLO
import cv2
import numpy as np
from objectkind import ObjectKind
import functions as f
from movement import *

# Load the exported ONNX model

# Run inference
onnx_model = YOLO('best.onnx')


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
        if boxes.cls[i] == tp.value:
            if boxes.conf[i] > max_confidence:
                max_confidence = boxes.conf[i]
                ind = i
    # print(ind)
    if ind == -1:
        return None
    return boxes[ind]


# минимальный размер контуров пятна
BLOBSIZE = 100


def check_size(w, h):
    if w * h > BLOBSIZE:
        return True
    else:
        return False


def follow_object_neyro(type_object: ObjectKind):
    # type_objects={0: 'ball', 1: 'blue_button', 2: 'cube', 3: 'green_basket', 4: 'green_button', 5: 'red_basket', 6: 'robot'}
    d_x = 150
    time_sleep = 0.1
    cub_size = 12000

    cap = cv2.VideoCapture("http://192.168.2.99:8080/?action=stream")  # Открываем видеопоток с камеры
    cap.set(3, 320)  # Устанавливаем ширину изображения в 320 пикселей
    cap.set(4, 320)  # Устанавливаем высоту изображения в 320 пикселей
    while True:  # Бесконечный цикл
        ret, frame = cap.read()  # Считываем кадр с камеры
        res = get_result_yolo(frame, type_object)
        cv2.imshow("Image", frame)
        if res is not None:

            x, y, w, h = res.xywh[0]
            center_x = (x + w) // 2
            if center_x < d_x - 30:
                turn_to_left(s, time_sleep)
            elif center_x > d_x + 30:
                turn_to_right(s, time_sleep)
            else:
                if w * h < cub_size:
                    forward_time(s, time_sleep)
                else:
                    pass

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    s = f.create_connect()
    follow_object_neyro(ObjectKind.CUBE)
