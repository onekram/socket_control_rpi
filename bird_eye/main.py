import walls
import targets
import cv2
from frame import get_frame
import logging
logging.disable(logging.FATAL)

def main():
    url = "rtsp://Admin:rtf123@192.168.2.250:554/1/1"
    cap = cv2.VideoCapture(url)

    frame = get_frame(cap)

    objs = walls.record_rtsp_stream(frame)
    graph = walls.parse_graph(objs)
    path = walls.bfs_shortest_path(graph, 0, 4)

    targets.record_rtsp_stream(frame)

    walls.draw_graph(frame, graph)
    walls.draw_path(frame, graph, path)

    cv2.imshow('Corrected Frame', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()

