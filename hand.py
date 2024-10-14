import socket
from servokind import ServoKind
from functions import move_servo

def start_position(s: socket.socket):
    move_servo(s, ServoKind.HAND, 87)
    move_servo(s, ServoKind.GRAB, 30)
    move_servo(s, ServoKind.SHOULDER, 180)
    move_servo(s, ServoKind.ELBOW, 100)
