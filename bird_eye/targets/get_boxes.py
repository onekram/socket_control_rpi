import cv2
import numpy as np
from ultralytics import YOLO
import logging
from frame import get_frame

logging.disable(logging.FATAL)
onnx_model = YOLO('targets/bird_eye_best_v3.onnx')

def get_result_yolo(frame):
    results = onnx_model(frame)
    boxes = results[0].boxes
    return boxes

def record_rtsp_stream(frame):
    boxes = get_result_yolo(frame)
    return boxes
