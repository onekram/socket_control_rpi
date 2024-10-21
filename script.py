from bird_eye.walls.model import WallsModel
import cv2
from frame import get_frame
from model import Model


# h - 0, v - 1
def h_or_v_walls(model_walls: WallsModel, frame) -> bool:
    objs = model_walls.get_objs(frame)
    return "part_up" in objs


def parse_generation() -> list:
    gen = []

    url1 = "rtsp://Admin:rtf123@192.168.2.250:554/1/1"
    cap = cv2.VideoCapture(url1)
    frame_ = get_frame(cap)

    model_walls_ = WallsModel('bird_eye/walls/walls.onnx')
    model_bird_eye = Model('bird_eye/targets/bird_eye_best_v3.onnx')

    map = model_bird_eye.get_map(frame_)

    # for name, value in map.items():
    #     print('------------------------------------------------')
    #     print(name)
    #     print(value)
    #     print('------------------------------------------------')
    # gen.append(h_or_v_walls(model_walls_, frame_))

    for cube in map["cube"]:
        x, y, _, _ = cube.xywh[0]
        x, y = int(x), int(y)
        print(x, y)

if __name__ == "__main__":
    parse_generation()
