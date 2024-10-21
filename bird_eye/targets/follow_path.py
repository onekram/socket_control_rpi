import socket
import time

import cv2
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

#FIVE_DEGREES = np.pi / 36

def correct_distance(distance : int, wall_obj) -> int:
    x, y, w, h = wall_obj.xywh[0]
    x, y, w, h = int(x), int(y), int(w), int(h)
    cm_in_pixels = float(w / 400)
    print(distance, cm_in_pixels)
    print(f"дистаниция {int(abs(distance / cm_in_pixels))}")
    return abs(int(distance / cm_in_pixels))


def angle_between_vectors(point_start : Tuple[int, int], point_end_1 : Tuple[int, int], point_end_2 :  Tuple[int, int]) -> float:
    vector_1 : Tuple[float, float] = (point_end_1[0] - point_start[0], point_end_1[1] - point_start[1])
    vector_2 : Tuple[float, float] = (point_end_2[0] - point_start[0], point_end_2[1] - point_start[1])

    angle1 : float = np.arctan2(vector_1[0], vector_1[1])
    angle2 : float = np.arctan2(vector_2[0], vector_2[1])

    return angle1 - angle2

def find_box_center(boxes, target_class_id : int) -> Tuple[int, int]:
    for box in range(len(boxes)):
        if boxes.cls[box] == target_class_id:
            x, y, w, h = boxes[box].xywh[0]
            return int(x), int(y)

def robot_body_cords(model_targets : Model, color : bool) -> Tuple[int, int]:
    color_id = 5 if color else 7
    #color_id = model_targets.class_id_by_name(color_class_name)
    desired_robot_body_center = find_box_center(model_targets.boxes, color_id)
    return desired_robot_body_center


def robot_grabber_cords(model_targets: Model, robot_cords : Tuple[int, int]) -> Tuple[int, int]:
    #grabber_class_name = "grabber"
    if robot_cords is None:
        raise RuntimeError("Робот не найден")
    grabber_id = 2

    nearest_box = None
    min_distance = float('inf')
    boxes = model_targets.boxes
    for box in range(len(model_targets.boxes)):
        if boxes.cls[box] == grabber_id:
            x, y, w, h = boxes[box].xywh[0]
            x, y, w, h = int(x), int(y), int(w), int(h)
            distance : float = np.sqrt((x - robot_cords[0]) ** 2 + (y - robot_cords[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                nearest_box = (x, y)
    return nearest_box

def rotate_by_angle(s: socket.socket, angle : float) -> None:
    set_speed(s, 50)
    print(f"угол {int(abs(angle) / np.pi * 180)}")
    if angle < 0:
        turn_left_angle(s, int(abs(angle) / np.pi * 180))
    else:
        turn_right_angle(s, int(abs(angle) / np.pi * 180))

def robot_to_point(s: socket.socket, robot_cords: Tuple[int, int], grabber_cords: Tuple[int, int], point_cords: Tuple[int, int], wall_obj) -> None:
    v = (point_cords[0] - robot_cords[0], point_cords[1] - robot_cords[1])
    print(v)
    dist = np.linalg.norm(v)

    angle = angle_between_vectors(robot_cords, grabber_cords, point_cords)
    rotate_by_angle(s, angle)
    time.sleep(5)
    forward_dist(s, correct_distance(dist, wall_obj))
    time.sleep(5)


def follow_by_path(s : socket.socket, model_targets : Model, path : Path, color : bool, wall_obj, cap) -> None:
    i = 0

    for vertex in path.vertexes[1:]:
        frame = get_frame(cap)

        model_targets.get_boxes(frame)


        robot_cords = robot_body_cords(model_targets, color)
        grabber_cords = robot_grabber_cords(model_targets, robot_cords)
        print("grabber_cords")
        print(grabber_cords)
        robot_to_point(s, robot_cords, grabber_cords, vertex, wall_obj)

def get_distance(point1 : Tuple[int, int], point2 : Tuple[int, int], wall_obj) -> float:
    v = (point2[0] - point1[0], point2[1] - point1[0])
    dist = np.linalg.norm(v)
    return correct_distance(dist, wall_obj)

def robot_to_point_wo_constants(s: socket.socket, model_targets : Model, point_cords: Tuple[int, int], wall_obj, cap, color : bool) -> None:
    #time.sleep(1.5)
    for i in range(45):
        frame = get_frame(cap)
    model_targets.get_boxes(frame)

    robot_cords = robot_body_cords(model_targets, color)
    grabber_cords = robot_grabber_cords(model_targets, robot_cords)

    angle = angle_between_vectors(robot_cords, grabber_cords, point_cords)
    distance = get_distance(robot_cords, point_cords, wall_obj)
    while distance > 15:
        while angle > np.pi / 36:
            rotate_by_angle(s, angle)
            for i in range(35):
                frame = get_frame(cap)
            model_targets.get_boxes(frame)
            cv2.putText(frame, f"{robot_cords, grabber_cords}", robot_cords, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.circle(frame, robot_cords, 10, (0, 0, 0), 2)
            cv2.imshow("", frame)
            cv2.waitKey(1)
            robot_cords = robot_body_cords(model_targets, color)
            grabber_cords = robot_grabber_cords(model_targets, robot_cords)
            angle = angle_between_vectors(robot_cords, grabber_cords, point_cords)

        forward_dist(s, distance)
        for i in range(35):
            frame = get_frame(cap)
        robot_cords = robot_body_cords(model_targets, color)
        grabber_cords = robot_grabber_cords(model_targets, robot_cords)
        distance = get_distance(robot_cords, point_cords, wall_obj)

        cv2.putText(frame, f"{robot_cords, grabber_cords}", robot_cords, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.imshow("", frame)
        cv2.waitKey(1)
        #time.sleep(1.5)

def test_func_find_point(model_targets : Model, point_cords: Tuple[int, int], cap, color : bool) -> None:
    frame = get_frame(cap)
    model_targets.get_boxes(frame)

    start_time = time.time()
    waiting = 5
    while True:
        if time.time() - start_time > waiting:
            start_time = time.time()
            frame = get_frame(cap)
            model_targets.get_boxes(frame)
            robot_cords = robot_body_cords(model_targets, color)
            grabber_cords = robot_grabber_cords(model_targets, robot_cords)
            angle = angle_between_vectors(robot_cords, grabber_cords, point_cords)
            cv2.putText(frame, f"{robot_cords, grabber_cords}", robot_cords, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.circle(frame, robot_cords, 10, (0, 0, 0), 2)
            cv2.imshow("", frame)
            cv2.waitKey(1)

            print(f"Angle between for turning to target {angle}")
            print(f"Robot cords {robot_cords}")
            print(f"Grabber cords {grabber_cords}")
        else:
            for _ in range(10):
                cap.grab()

def follow_by_path_test(model_targets : Model, path : Path, color : bool, cap) -> None:
    for vertex in path.vertexes[1:]:
        test_func_find_point(model_targets, vertex, cap, color)
        print("Вершина пройдена")

def follow_by_path_wo_constants(s : socket.socket, model_targets : Model, path : Path, color : bool, wall_obj, cap) -> None:
    for vertex in path.vertexes[1:]:
        robot_to_point_wo_constants(s, model_targets, vertex, wall_obj, cap, color)
        print("Вершина пройдена")


