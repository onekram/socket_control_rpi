from .graph import Graph

def detect_in_area(pos, area_cords):
    x, y = pos
    lu, ru, ld, rd = area_cords
    return lu[0] <= x <= ru[0] and lu[1] <= y <= ld[1]

def robot_position(pos, wall1, wall2, wall3):
    if detect_in_area(pos, get_corners(wall3)):
        return 3
    if detect_in_area(pos, get_corners(wall2)):
        return 2
    if detect_in_area(pos, get_corners(wall1)):
        return 1
    return -1

def get_corners(obj):
    x, y, w, h = obj.xywh[0]
    x, y, w, h = int(x), int(y), int(w), int(h)
    return (x - w // 2, y - h // 2), (x + w // 2, y - h // 2), (x - w // 2, y + h // 2), (x + w // 2, y + h // 2)

def get_middle(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2

    return min(x1, x2) + abs(x1 - x2) // 2, min(y1, y2) + abs(y1 - y2) // 2

def get_middle_from_corners(corners1, corners2):
    lu1, ru1, ld1, rd1 = corners1
    lu2, ru2, ld2, rd2 = corners2
    a = get_middle(lu1, lu2)
    c = get_middle(ru1, ru2)
    b = get_middle(a, c)
    e = get_middle(rd1, rd2)
    d = get_middle(c, e)
    g = get_middle(ld1, ld2)
    f = get_middle(g, e)
    h = get_middle(a, g)

    return [a, b, c, d, e, f, g, h]

def parse_graph(objs) -> Graph:
    wall1 = objs["wall1"]
    wall2 = objs["wall2"]
    wall3 = objs["wall3"]
    outer = get_middle_from_corners(get_corners(wall1), get_corners(wall2))
    inner = get_middle_from_corners(get_corners(wall3), get_corners(wall2))
    matrix = [
        [1, 7],
        [0, 2],
        [1, 3],
        [2, 4],
        [3, 5],
        [4, 6],
        [5, 7],
        [6, 0],
        [15, 9],
        [8, 10],
        [9, 11],
        [10, 12],
        [11, 13],
        [12, 14],
        [13, 15],
        [14, 8]
    ]

    if not "part_left" in objs:
        matrix[7].append(15)
        matrix[15].append(7)
    if not "part_up" in objs:
        matrix[1].append(9)
        matrix[9].append(1)
    if not "part_right" in objs:
        matrix[3].append(11)
        matrix[11].append(3)
    if not "part_left" in objs:
        matrix[5].append(13)
        matrix[13].append(5)
    return Graph(outer + inner, matrix)
