from ultralytics import YOLO
from frame import get_frame
import cv2


class Model:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)
        self.frame = None
        self.boxes = None

    def get_boxes(self, frame):
        if self.frame is frame:
            return self.boxes

        results = self.model(frame)
        self.boxes = results[0].boxes
        self.frame = frame
        return self.boxes

    def draw_boxes(self, frame):
        boxes = self.get_boxes(frame)

        for box in boxes:
            name = self.model.names[int(box.cls)]
            x, y, w, h = box.xywh[0]
            x, y, w, h = int(x), int(y), int(w), int(h)
            p = round(float(box.conf), 3)
            cv2.putText(frame, f"{name} | {p}", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 0), 2)
            cv2.rectangle(frame, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (255, 255, 255), 2)

    def class_id_by_name(self, class_name : str):
        names = self.names()
        reverse_names = {}
        for i in range(len(names)):
            reverse_names[names[i]] = i
        #print(names[0])
        #print(names)
        return reverse_names[class_name]


    def update(self, url : str):
        cap = cv2.VideoCapture(url)
        frame = get_frame(cap)
        self.get_boxes(frame)


    def names(self):
        return self.model.names