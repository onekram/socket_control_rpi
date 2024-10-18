import cv2
import numpy as np
from ultralytics import YOLO
import logging

logging.disable(logging.FATAL)
onnx_model = YOLO('targets/bird_eye_best_v3.onnx')

def get_result_yolo(frame):
    results = onnx_model(frame)
    boxes = results[0].boxes
    return boxes

def record_rtsp_stream(cap):
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

    # x_start, y_start = 300, 39
    # x_end, y_end = 1600, 1007
    # # Crop the frame
    # frame = frame[y_start:y_end, x_start:x_end]

    frame = cv2.resize(frame, (int(960 * 1.3), int(540 * 1.3)))
    boxes = get_result_yolo(frame)
    for i, box in enumerate(boxes):
        cls = int(box.cls)
        x, y, w, h = box.xywh[0]
        x, y, w, h = int(x), int(y), int(w), int(h)
        p = round(float(boxes.conf[i]), 3)
        l = onnx_model.names
        cv2.putText(frame, f"p={p}", (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 0), 2)
        cv2.rectangle(frame, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (255, 255, 255), 2)
    return boxes, frame
