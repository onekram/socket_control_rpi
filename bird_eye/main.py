from walls.parse_objects import  *
from walls.get_boxes import *
from bird_eye.walls.path import *

def main():
    url = "rtsp://Admin:rtf123@192.168.2.250:554/1/1"
    # url = "output.mp4"
    objs, frame = record_rtsp_stream(url)
    graph = parse_graph(objs)
    draw_graph(frame, graph)
    path = bfs_shortest_path(graph, 0, 4)
    draw_path(frame, graph, path)

    cv2.imshow('Corrected Frame', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

