import socket
import time

from servokind import ServoKind
from servo_movement import move_servo

def start_position(s: socket.socket):
    move_servo(s, ServoKind.HAND, 87)
    move_servo(s, ServoKind.GRAB, 30)
    move_servo(s, ServoKind.SHOULDER, 150)
    move_servo(s, ServoKind.ELBOW, 100)

def catch(s: socket.socket):
    move_servo(s, ServoKind.GRAB, 20)
    time.sleep(0.1)
    move_servo(s, ServoKind.HAND, 90)
    move_servo(s, ServoKind.SHOULDER, 85)
    move_servo(s, ServoKind.ELBOW, 150)

def hold(s: socket.socket):
    move_servo(s, ServoKind.GRAB, 65)
    time.sleep(0.5)
    move_servo(s, ServoKind.HAND, 87)
    move_servo(s, ServoKind.SHOULDER, 160)
    move_servo(s, ServoKind.ELBOW, 100)
