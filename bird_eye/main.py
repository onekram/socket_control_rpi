import walls
import targets
import cv2
from frame import get_frame
import logging
from model import Model
logging.disable(logging.FATAL)

def main():
    url = "rtsp://Admin:rtf123@192.168.2.250:554/1/1"
    cap = cv2.VideoCapture(url)

    frame = get_frame(cap)

    model_walls = Model('walls/walls.onnx')
    boxes_walls = model_walls.get_boxes(frame)
    objs = walls.check_correct(boxes_walls, model_walls.names())

    graph = walls.parse_graph(objs)
    path = walls.bfs_shortest_path(graph, 0, 4)


    model_targets = Model('targets/bird_eye_best_v3.onnx')
    model_targets.draw_boxes(frame)

    walls.draw_graph(frame, graph)
    walls.draw_path(frame, graph, path)

    cv2.imshow('Corrected Frame', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()

