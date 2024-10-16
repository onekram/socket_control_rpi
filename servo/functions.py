from servo import camera, hand


def start(s):
    camera.start_position(s)
    hand.start_position(s)
