import socket
import numpy as np
from functions import create_connect
from typing import Tuple
from movement import turn_left_angle, turn_right_angle, set_speed, forward_dist
from servo import add_functions as sf
from bird_eye.walls.path import *
from bird_eye.walls.graph import *
from model import  Model

#FIVE_DEGREES = np.pi / 36

def angle_between_vectors(point_start : Tuple[int, int], point_end_1 : Tuple[int, int], point_end_2 :  Tuple[int, int]) -> float:
    vector_1 : Tuple[float, float] = (point_end_1[0] - point_start[0], point_end_1[1] - point_start[1])
    vector_2 : Tuple[float, float] = (point_end_2[0] - point_start[0], point_end_2[1] - point_start[1])

    angle1 : float = np.arctan2(vector_1[0], vector_1[1])
    angle2 : float = np.arctan2(vector_2[0], vector_2[1])

    return angle1 - angle2

def find_box_center(boxes : list, target_class_id : int) -> Tuple[int, int]:
    for box in boxes:
        if box['class_id'] == target_class_id:
            x1, y1, x2, y2 = box['box']
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            return center_x, center_y

def robot_body_cords(model_targets : Model, color : bool) -> Tuple[int, int]:
    color_class_name = "green_robot" if color else "red_robot"
    color_id = model_targets.class_id_by_name(color_class_name)
    desired_robot_body_center = find_box_center(model_targets.boxes, color_id)
    return desired_robot_body_center


def robot_grabber_cords(model_targets: Model, robot_cords : Tuple[int, int]) -> Tuple[int, int]:
    grabber_class_name = "grabber"
    grabber_id = model_targets.class_id_by_name(grabber_class_name)

    nearest_box = None
    min_distance = float('inf')

    for box in model_targets.boxes:
        if box['class_id'] == grabber_id:
            x1, y1, x2, y2 = box['box']
            center_x : float = (x1 + x2) // 2
            center_y : float = (y1 + y2) // 2

            distance : float = np.sqrt((center_x - robot_cords[0]) ** 2 + (center_y - robot_cords[1]) ** 2)

            if distance < min_distance:
                min_distance = distance
                nearest_box = box

    return nearest_box

def rotate_by_angle(s: socket.socket, angle : float) -> None:
    set_speed(s, 50)
    if angle > 0:
        turn_left_angle(s, abs(angle) / np.pi * 180)
    else:
        turn_right_angle(s, abs(angle) / np.pi * 180)

def robot_to_point(s: socket.socket, robot_cords: Tuple[int, int], grabber_cords: Tuple[int, int], point_cords: Tuple[int, int]) -> None:
    v = (point_cords[0] - robot_cords[0], point_cords[1] - robot_cords[1])
    dist = np.linalg.norm(v)
    angle = angle_between_vectors(robot_cords, grabber_cords, point_cords)
    rotate_by_angle(s, angle)
    forward_dist(s, dist)


def follow_by_path(s : socket.socket, model_targets : Model, path : Path, color : bool) -> None:
    for vertex in path.vertexes:
        #model_targets.update()
        robot_cords = robot_body_cords(model_targets, color)
        grabber_cords = robot_grabber_cords(model_targets, robot_cords)
        robot_to_point(s, robot_cords, grabber_cords, vertex)




