import socket
from servokind import ServoKind
from functions import send_command
from servo.servo_movement import move_servo


def start_position(s: socket.socket):
    move_servo(s, ServoKind.CAM_LR, 75)
    move_servo(s, ServoKind.CAM_UD, 75)

def color_follow(s: socket.socket):
    ba = bytearray(b'\xab\x06\x01\x00\xff')
    send_command(s, ba)
