import walls
import targets
import cv2

def main():
    url = "rtsp://Admin:rtf123@192.168.2.250:554/1/1"
    cap = cv2.VideoCapture(url)

    objs, frame = walls.record_rtsp_stream(cap)
    graph = walls.parse_graph(objs)
    walls.draw_graph(frame, graph)
    path = walls.bfs_shortest_path(graph, 0, 4)
    walls.draw_path(frame, graph, path)

    cv2.imshow('Corrected Frame', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

