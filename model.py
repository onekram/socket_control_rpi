from ultralytics import YOLO
from frame import get_frame
import cv2


class Model:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)
        self.boxes = None

    def get_boxes(self, frame):
        results = self.model(frame) # todo: try verifying which frame is being gotten
        self.boxes = results[0].boxes
        # self.frame = frame
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
        for i in range(len(names)):
            if names[i] == class_name:
                return i
        #print(names[0])
        #print(names)


    def update(self, url : str):
        cap = cv2.VideoCapture(url)
        frame = get_frame(cap)
        self.get_boxes(frame)


    def names(self):
        return self.model.names

    def get_map(self, frame):
        boxes = self.get_boxes(frame)
        res = dict()
        for box in boxes:
            cls = int(box.cls)
            name = self.names()[cls]
            if name in res:
                res[name].append(box)
            else:
                res[name] = [box]

        for name, list_box in res.items():
            list_box.sort(key=lambda b: round(float(b.conf), 3), reverse=True)
        return res
