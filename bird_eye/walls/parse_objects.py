
class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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


def parse(objs):
    wall1 = objs["wall1"]
    wall2 = objs["wall2"]
    wall3 = objs["wall3"]

    outer = get_middle_from_corners(get_corners(wall1), get_corners(wall2))
    inner = get_middle_from_corners(get_corners(wall3), get_corners(wall2))

    return outer + inner






