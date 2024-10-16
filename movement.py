import time
import socket
from functions import send_command

def set_speed(s: socket.socket, value: int):
    ba1 = bytearray(b'\xab\x02\x01\x00\xff')
    ba2 = bytearray(b'\xab\x02\x02\x00\xff')

    ba1[3] = value
    ba2[3] = value
    send_command(s, ba1)
    send_command(s, ba2)

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

def turn_left_90(s: socket.socket):
    spin_left(s)
    time.sleep(1.3)
    stop(s)

def spin_right(s: socket.socket):
    ba = bytearray(b'\xab\x00\x04\x00\xFF')
    send_command(s, ba)

def forward_time(s: socket.socket, t: float):
    forward(s)
    time.sleep(t)
    stop(s)

def turn_right_90(s: socket.socket):
    spin_right(s)
    time.sleep(1.3)
    stop(s)

def turn_to_left(s: socket.socket, t: float):
    spin_left(s)
    time.sleep(t)
    stop(s)

def turn_to_right(s: socket.socket, t: float):
    spin_right(s)
    time.sleep(t)
    stop(s)

def forward_time_without_stop(s: socket.socket, t: float):
    forward(s)
    time.sleep(t)

def turn_to_left_without_stop(s: socket.socket, t: float):
    spin_left(s)
    time.sleep(t)

def turn_to_right_without_stop(s: socket.socket, t: float):
    spin_right(s)
    time.sleep(t)
