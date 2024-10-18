import cv2
url = "rtsp://Admin:rtf123@192.168.2.250:554/1/1"


class GlobalState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalState, cls).__new__(cls)
            cls._instance.objs = None
            cls._instance.cap = "Initial Value 3"
        return cls._instance


objs = None
cap = None