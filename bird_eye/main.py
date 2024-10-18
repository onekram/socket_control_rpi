import walls
import cv2

from bird_eye.walls.model import WallsModel
from frame import get_frame
import logging
from model import Model
logging.disable(logging.FATAL)

def main():
    url = "rtsp://Admin:rtf123@192.168.2.250:554/1/1"
    cap = cv2.VideoCapture(url)

    frame = get_frame(cap)

    model_walls = WallsModel('walls/walls.onnx')
    objs = model_walls.get_objs(frame)

    graph = walls.parse_graph(objs)
    path = graph.get_path(0, 4)

    model_targets = Model('targets/bird_eye_best_v3.onnx')
    model_targets.draw_boxes(frame)

    graph.draw(frame)
    path.draw(frame)

    cv2.imshow('Corrected Frame', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()

