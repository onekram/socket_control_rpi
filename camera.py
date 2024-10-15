import socket
from servokind import ServoKind
from functions import move_servo

def start_position(s: socket.socket):
    move_servo(s, ServoKind.CAM_LR, 75)
    move_servo(s, ServoKind.CAM_UD, 75)
