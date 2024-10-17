import cv2
import numpy as np
from ultralytics import YOLO
import logging

from parse_objects import *

logging.disable(logging.FATAL)
onnx_model = YOLO('walls.onnx')

def get_result_yolo(frame):
    results = onnx_model(frame)
    boxes = results[0].boxes
    return boxes

def check_correct(boxes):
    l = onnx_model.names
    types = dict()
    for box in boxes:
        cls = int(box.cls)
        name = l[cls]
        if name in types:
            types[name].append(box)
        else:
            types[name] = [box]

    if not "wall3" in types or not "wall2" in types or not "wall1" in types:
        return None

    for name, list_box in types.items():
        list_box.sort(key=lambda b: round(float(b.conf), 3), reverse=True)


    wall3 = types["wall3"][0]
    x_3, y_3, w_3, h_3 = wall3.xywh[0]
    wall2 = types["wall2"][0]
    wall1 = types["wall1"][0]

    res = dict()
    res["wall1"] = wall1
    res["wall2"] = wall2
    res["wall3"] = wall3

    for part in types["part"]:
        x, y, w, h = part.xywh[0]
        if y - h//2 > y_3 + h_3//2:
            res["part_d"] = part
        if y + h//2 < y_3 - h_3//2:
            res["part_up"] = part
        if x + w//2 < x_3 - w_3//2:
            res["part_left"] = part
        if x - w//2 > x_3 + w_3//2:
            res["part_right"] = part
    return res

def get_from_cap(cap, draw=False):
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


    camera_matrix = np.array([[1182.719, 0, 927.03],
                               [0, 1186.236, 609.52],
                               [0, 0, 1]], dtype=np.float32)
    dist_coeffs = np.array([-0.5, 0.3, 0, 0, 0], dtype=np.float32)

    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (frame_width, frame_height), 1, (frame_width, frame_height))
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        return

    frame = cv2.undistort(frame, camera_matrix, dist_coeffs, None, new_camera_matrix)

    x, y, w, h = roi
    frame = frame[y:y+h, x:x+w]

    # x_start, y_start = 200, 10
    # x_end, y_end = 1500, 1007
    # frame = frame[y_start:y_end, x_start:x_end]

    frame = cv2.resize(frame, (int(960 * 1.3), int(540 * 1.3)))

    boxes = get_result_yolo(frame)
    boxes = check_correct(boxes)
    if draw:
        for name, box in boxes.items():
            x, y, w, h = box.xywh[0]
            x, y, w, h = int(x), int(y), int(w), int(h)
            p = round(float(box.conf), 3)

            cv2.putText(frame, f"({x - w // 2}, {y - h // 2})", (x - w // 2, y - h // 2),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4, (0, 0, 255), 2)

            cv2.putText(frame, f"({x + w // 2}, {y - h // 2})", (x + w // 2, y - h // 2),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4, (0, 0, 255), 2)

            cv2.putText(frame, f"({x - w // 2}, {y + h // 2})", (x - w // 2, y + h // 2),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4, (0, 0, 255), 2)

            cv2.putText(frame, f"({x + w // 2}, {y + h // 2})", (x + w // 2, y + h // 2),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4, (0, 0, 255), 2)

            cv2.putText(frame, f"{name}", (x, y - h//2 + 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4, (0, 255, 0), 2)

            cv2.rectangle(frame, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (255, 255, 255), 1)
    return boxes, frame


def record_rtsp_stream(rtsp_url, draw=False):
    cap = cv2.VideoCapture(rtsp_url)
    for i in range(3):
        objs, frame = get_from_cap(cap, draw)
        if objs is not None:
            for i, v in enumerate(parse(objs)):
                cv2.circle(frame, v, 10, (0, 255, 0), -1)
                cv2.putText(frame, f"{i}", v,
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 120, 120), 2)
            if draw:
                cv2.imshow('Corrected Frame', frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            cap.release()
            return objs

    raise RuntimeError("Bad frame bird eye")


if __name__ == "__main__":
    url = "rtsp://Admin:rtf123@192.168.2.250:554/1/1"
    record_rtsp_stream(url, True)

