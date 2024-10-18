from ultralytics import YOLO

def check_correct(boxes, names):
    types = dict()
    for box in boxes:
        cls = int(box.cls)
        name = names[cls]
        if name in types:
            types[name].append(box)
        else:
            types[name] = [box]

    if not "wall3" in types or not "wall2" in types or not "wall1" in types:
        return None

    for name, list_box in types.items():
        list_box.sort(key=lambda b: round(float(b.conf), 3), reverse=True)


    wall3 = types["wall3"][0]
    x_3, y_3, w_3, h_3 = wall3.xywh[0]
    wall2 = types["wall2"][0]
    wall1 = types["wall1"][0]

    res = dict()
    res["wall1"] = wall1
    res["wall2"] = wall2
    res["wall3"] = wall3

    for part in types["part"]:
        x, y, w, h = part.xywh[0]
        if y - h//2 > y_3 + h_3//2:
            res["part_down"] = part
        if y + h//2 < y_3 - h_3//2:
            res["part_up"] = part
        if x + w//2 < x_3 - w_3//2:
            res["part_left"] = part
        if x - w//2 > x_3 + w_3//2:
            res["part_right"] = part
    return res

# def record_rtsp_stream(frame):
#     for i in range(3):
#         objs = get_from_cap(frame)
#         if objs is not None:
#             return objs
#
#     raise RuntimeError("Bad frame bird eye")
