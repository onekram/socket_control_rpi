import socket
from servokind import ServoKind
from functions import move_servo

def start_position(s: socket.socket):
    move_servo(s, ServoKind.HAND, 87)
    move_servo(s, ServoKind.GRAB, 30)
    move_servo(s, ServoKind.SHOULDER, 150)
    move_servo(s, ServoKind.ELBOW, 100)

def hold_position(s: socket.socket):
    move_servo(s, ServoKind.HAND, 87)
    move_servo(s, ServoKind.GRAB, 65)
    move_servo(s, ServoKind.SHOULDER, 160)
    move_servo(s, ServoKind.ELBOW, 100)

def test_position(s: socket.socket):
    move_servo(s, ServoKind.HAND, 87)
    move_servo(s, ServoKind.GRAB, 30)
    move_servo(s, ServoKind.SHOULDER, 120)
    move_servo(s, ServoKind.ELBOW, 110)
