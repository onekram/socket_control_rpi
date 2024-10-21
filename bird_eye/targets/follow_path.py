import socket
import time

import numpy as np

from frame import get_frame
from functions import create_connect
from typing import Tuple
from movement import turn_left_angle, turn_right_angle, set_speed, forward_dist
from servo import add_functions as sf
from bird_eye.walls.path import *
from bird_eye.walls.graph import *
from model import  Model
from bird_eye.walls.parse_objects import get_corners

def get_distance(point1 : Tuple[int, int], point2 : Tuple[int, int], wall_obj) -> float:
    v = (point2[0] - point1[0], point2[1] - point1[0])
    dist = np.linalg.norm(v)
    return correct_distance(dist, wall_obj)

def correct_distance(distance : float, wall_obj) -> int:
    x, y, w, h = wall_obj.xywh[0]
    cm_in_pixels = w / 400
    print(distance)
    return int(abs(distance * cm_in_pixels))


def angle_between_vectors(point_start : Tuple[int, int], point_end_1 : Tuple[int, int], point_end_2 :  Tuple[int, int]) -> float:
    vector_1 : Tuple[float, float] = (point_end_1[0] - point_start[0], point_end_1[1] - point_start[1])
    vector_2 : Tuple[float, float] = (point_end_2[0] - point_start[0], point_end_2[1] - point_start[1])

    angle1 : float = np.arctan2(vector_1[0], vector_1[1])
    angle2 : float = np.arctan2(vector_2[0], vector_2[1])

    return angle1 - angle2

def find_box_center(boxes, target_class_id : int) -> Tuple[int, int]:
    for box in range(len(boxes)):
        if boxes.cls[box] == target_class_id:
            x1, y1, x2, y2 = boxes[box].xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            return (center_x, center_y)

def robot_body_cords(model_targets : Model, color : bool) -> Tuple[int, int]:
    color_class_name = "green_robot" if color else "red_robot"
    color_id = model_targets.class_id_by_name(color_class_name)
    print(color_id)
    desired_robot_body_center = find_box_center(model_targets.boxes, color_id)
    return desired_robot_body_center


def robot_grabber_cords(model_targets: Model, robot_cords : Tuple[int, int]) -> Tuple[int, int]:
    grabber_class_name = "grabber"
    grabber_id = model_targets.class_id_by_name(grabber_class_name)

    nearest_box = None
    min_distance = float('inf')
    boxes = model_targets.boxes
    for box in range(len(model_targets.boxes)):
        if boxes.cls[box] == grabber_id:
            x1, y1, x2, y2 = boxes[box].xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            center_x : float = (x1 + x2) // 2
            center_y : float = (y1 + y2) // 2

            distance : float = np.sqrt((center_x - robot_cords[0]) ** 2 + (center_y - robot_cords[1]) ** 2)

            if distance < min_distance:
                min_distance = distance
                nearest_box = boxes[box]
    nearest_box_center = (int(nearest_box.xywh[0][0]), int(nearest_box.xywh[0][1]))
    return nearest_box_center

def rotate_by_angle(s: socket.socket, angle : float) -> None:
    set_speed(s, 50)
    if angle < 0:
        turn_left_angle(s, int(abs(angle) / np.pi * 180))
    else:
        turn_right_angle(s, int(abs(angle) / np.pi * 180))

def robot_to_point_wo_constants(s: socket.socket, model_targets : Model, point_cords: Tuple[int, int], wall_obj, cap, color : bool) -> None:
    time.sleep(1.5)

    frame = get_frame(cap)
    model_targets.get_boxes(frame)

    robot_cords = robot_body_cords(model_targets, color)
    grabber_cords = robot_grabber_cords(model_targets, robot_cords)

    distance = get_distance(robot_cords, point_cords, wall_obj)

    while distance > 15:
        angle = angle_between_vectors(robot_cords, grabber_cords, point_cords)
        while angle > np.pi / 36:
            rotate_by_angle(s, angle)
            time.sleep(1.5)
            frame = get_frame(cap)
            model_targets.get_boxes(frame)
            angle = angle_between_vectors(robot_cords, grabber_cords, point_cords)

        forward_dist(s, distance)
        time.sleep(1.5)
        frame = get_frame(cap)
        model_targets.get_boxes(frame)
        distance = get_distance(robot_cords, point_cords, wall_obj)


def follow_by_path_wo_constants(s : socket.socket, model_targets : Model, path : Path, color : bool, wall_obj, cap) -> None:
    for vertex in path.vertexes:
        robot_to_point_wo_constants(s, model_targets, vertex, wall_obj, cap, color)

def robot_to_point(s: socket.socket, robot_cords: Tuple[int, int], grabber_cords: Tuple[int, int], point_cords: Tuple[int, int], wall_obj) -> None:
    v = (point_cords[0] - robot_cords[0], point_cords[1] - robot_cords[1])
    dist = np.linalg.norm(v)

    angle = angle_between_vectors(robot_cords, grabber_cords, point_cords)
    rotate_by_angle(s, angle)
    time.sleep(0.5)
    forward_dist(s, correct_distance(dist, wall_obj))
    time.sleep(0.5)


def follow_by_path(s : socket.socket, model_targets : Model, path : Path, color : bool, wall_obj, cap) -> None:
    for vertex in path.vertexes:
        frame = get_frame(cap)
        model_targets.get_boxes(frame)
        robot_cords = robot_body_cords(model_targets, color)
        grabber_cords = robot_grabber_cords(model_targets, robot_cords)
        robot_to_point(s, robot_cords, grabber_cords, vertex, wall_obj)
