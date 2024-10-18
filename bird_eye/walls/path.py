import cv2
from typing import Tuple
class Path:
    def __init__(self, vertexes: list[Tuple[int, int]]):
        self.vertexes = vertexes

    def draw(self, frame):
        last = None
        for v in self.vertexes:
            cv2.circle(frame, v, 10, (0, 0, 255), -1)
            if last is not None:
                cv2.line(frame, last, v, (0, 0, 255), 2)
            last = v
