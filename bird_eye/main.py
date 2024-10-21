import time

import walls
import cv2

from bird_eye.targets.follow_path import follow_by_path_wo_constants, follow_by_path_test
from bird_eye.walls.model import WallsModel
from color import Color
from frame import get_frame
import logging
from targets.follow_path import follow_by_path
from model import Model
from functions import create_connect
from servo import  add_functions as sf
from servo.hand import catch, prepare_bird_eye
from functions import set_color
logging.disable(logging.FATAL)

def main():
    url = "rtsp://Admin:rtf123@192.168.2.250:554/1/1"
    cap = cv2.VideoCapture(url)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    frame = get_frame(cap)

    s = create_connect()
    sf.start(s)
    set_color(s, Color.GREEN)
    prepare_bird_eye(s)

    model_walls = WallsModel('walls/walls.onnx')
    objs = model_walls.get_objs(frame)

    graph = walls.parse_graph(objs)
    path = graph.get_path(0, 4)

    model_targets = Model('targets/bird_eye_best_v3.onnx')
    model_targets.draw_boxes(frame)

    graph.draw(frame)
    path.draw(frame)
    print("Follow path processing")

    # cv2.imshow('Image', frame)
    # cv2.waitKey(1)

    # follow_by_path(s, model_targets, path, 1, objs["wall1"], cap)
    follow_by_path_test(model_targets, path, 1, cap)


if __name__ == "__main__":
    main()

