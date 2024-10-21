from frame import get_frame
import cv2
import logging
from model import Model

logging.disable(logging.FATAL)

def main():
    url = "rtsp://Admin:rtf123@192.168.2.251:554/1/1"
    cap = cv2.VideoCapture(url)
    frame = get_frame(cap)

    model_targets = Model('bird_eye_best_v3.onnx')
    model_targets.draw_boxes(frame)

    # cv2.imshow('Corrected Frame', frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()

