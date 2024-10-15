import socket
from servokind import ServoKind
from functions import send_command

def move_servo(s: socket.socket, servo: ServoKind, angle: int):
    ba = bytearray(b'\xab\x01\x00\x00\xff')
    ba[2] = servo.value
    ba[3] = angle
    send_command(s, ba)