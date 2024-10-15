import time
import socket
from functions import set_speed, send_command

def stop(s: socket.socket):
    ba = bytearray(b'\xab\x00\x00\x00\xff')
    s.sendall(ba)

def forward(s: socket):
    ba = bytearray(b'\xab\x00\x01\x00\xff')
    s.sendall(ba)

def forward_dist(s: socket, dist: int):
    forward(s)
    time.sleep(dist)
    stop(s)

def spin_left(s: socket.socket):
    ba = bytearray(b'\xab\x00\x03\x00\xFF')
    send_command(s, ba)

def turn_to_left(s: socket.socket):
    spin_left(s)
    time.sleep(1.3)
    stop(s)

def spin_right(s: socket.socket):
    ba = bytearray(b'\xab\x00\x04\x00\xFF')
    send_command(s, ba)

def turn_to_right(s: socket.socket):
    spin_right(s)
    time.sleep(1.3)
    stop(s)
