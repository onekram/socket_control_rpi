import functions
import socket
import numpy as np
from typing import Tuple
from movement import turn_to_left, turn_to_right


def rotate_by_angle(s: socket.socket, angle : float) -> None:
    if angle < 0:
        turn_to_right(socket, abs(angle)) #????
    else:
        turn_to_left(socket, abs(angle)) #????


def angle_between_vectors(point_start : Tuple[float, float], point_end_1 : Tuple[float, float], point_end_2 :  Tuple[float, float]) -> float:
    vector_1 : Tuple[float, float] = (point_end_1[0] - point_start[0], point_end_1[1] - point_start[1])
    vector_2 : Tuple[float, float] = (point_end_2[0] - point_start[0], point_end_2[1] - point_start[1])

    angle1 : float = np.atan2(vector_1[0], vector_1[1])
    angle2 : float = np.atan2(vector_2[0], vector_2[1])

    return angle1 - angle2

def robot_to_point(s: socket.socket, robot_coords: Tuple[float, float], grab_coords: Tuple[float, float], point_coords: Tuple[float, float]):
    dist = np.linalg.norm(point_coords - robot_coords)
    angle = angle_between_vectors(robot_coords, grab_coords, point_coords)
    rotate_by_angle(angle)
    #go_forward_by_dist(dist)
