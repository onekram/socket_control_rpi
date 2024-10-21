from bird_eye.walls.model import WallsModel
from bird_eye.walls.parse_objects import robot_position, get_corners
import cv2
from frame import get_frame
from model import Model


# 0 - h, 1 - v
def h_or_v_walls(objs) -> int:
    return "part_up" in objs

# 0 - outside, 1 - inside bot, 2 - inside top
def cube_pos(objs, mp) -> int:
    x, y, _, _ = mp["cube"][0].xywh[0]
    obj_pos = robot_position((x, y), objs["wall1"], objs["wall2"], objs["wall3"])

    if obj_pos == 1:
        return 0
    elif y < 447:
        return 1
    else:
        return 2

def parse_generation() -> list:
    gen = []

    url1 = "rtsp://Admin:rtf123@192.168.2.250:554/1/1"
    cap = cv2.VideoCapture(url1)
    frame_ = get_frame(cap)

    model_walls_ = WallsModel('bird_eye/walls/walls.onnx')
    wall_objs = model_walls_.get_objs(frame_)
    model_bird_eye = Model('bird_eye/targets/bird_eye_best_v3.onnx')

    mp = model_bird_eye.get_map(frame_)

    gen.append(h_or_v_walls(wall_objs))
    gen.append(cube_pos(wall_objs, mp))

    return gen

if __name__ == "__main__":
    parse_generation()
