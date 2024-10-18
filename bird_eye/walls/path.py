import math
from collections import deque
import cv2
from torch.cuda import graph

from bird_eye.walls.parse_objects import Graph

def bfs_shortest_path(graph: Graph, start, goal):
    visited = set()
    queue = deque([start])
    if start == goal:
        return [start]
    back = [0] * graph.size()
    find = False
    while queue:
        cur = queue.popleft()
        neighbors = graph.neighbours(cur)
        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
                back[neighbor] = cur

                if neighbor == goal:
                    find = True
                    break
        visited.add(cur)
    if find:
        path = []
        cur = goal
        while cur != start:
            path.append(cur)
            cur = back[cur]
        path.append(start)
        return path[::-1]
    return None

def draw_path(frame, graph: Graph, path: list[int]):
    last = None
    for idx in path:
        v = graph[idx]
        cv2.circle(frame, v, 10, (0, 0, 255), -1)
        if last is not None:
            cv2.line(frame, last, v, (0, 0, 255), 2)
        last = v

def calculate_angle(v1, v2):
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    magnitude_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
    magnitude_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)
    cos_theta = dot_product / (magnitude_v1 * magnitude_v2)
    return math.acos(cos_theta)

def move_robot(start, goal):
    direction = (goal[0] - start[0], goal[1] - start[1])
    return direction

def direction_of_robot_view(grab_of_robot, tail_of_robot):
    current_direction = (grab_of_robot[0] - tail_of_robot[0], grab_of_robot[1] - tail_of_robot[1])
    return current_direction

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def control_robot(path: list[int], graph: Graph, current_direction: tuple[int]):
    """
    Управление роботом по заданному маршруту с использованием библиотеки go.

    path: список вершин, по которым робот должен пройти
    coordinates: словарь с координатами вершин
    current_direction: текущее направление робота в виде вектора (например, (1, 0))
    proximity_threshold: порог для определения "близости" робота к цели
    """

    for i in range(len(path) - 1):
        start = path[i]
        goal = path[i + 1]

        start = graph[path[0]]
        goal = graph[path[-1]]

        distance_to_goal = calculate_distance(start, goal)

        if distance_to_goal <= 50:
            print(f"Робот уже находится достаточно близко к {goal}. Пропускаем этот шаг.")
            go.stop(robot)
            continue

        target_direction = move_robot(start, goal)

        angle = calculate_angle(current_direction, target_direction)

        while angle > 5:
            cross_product = current_direction[0] * target_direction[1] - current_direction[1] * target_direction[0]
            if cross_product > 0:
                go.spin_left(robot)
                print(f"Поворачиваем налево")
            else:
                go.spin_right(robot)
                print(f"Поворачиваем направо")

            current_direction = target_direction
            angle = calculate_angle(current_direction, target_direction)

        go.forward(robot)
        print(f"Двигаемся вперёд из {start} в {goal}.")
