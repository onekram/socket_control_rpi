from ultralytics import YOLO
from parse_objects_camera.objectkind import ObjectKind
MIN_SIZE = 300

# функция обращения к нейросети и возвращение объекта по типу
def get_result_yolo(onnx_model, frame, tp: ObjectKind):
    results = onnx_model(frame)
    boxes = results[0].boxes
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