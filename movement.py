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

def back(s: socket):
    ba = bytearray(b'\xab\x00\x02\x00\xff')
    s.sendall(ba)

def spin_left(s: socket.socket):
    ba = bytearray(b'\xab\x00\x03\x00\xFF')
    send_command(s, ba)

def spin_right(s: socket.socket):
    ba = bytearray(b'\xab\x00\x04\x00\xFF')
    send_command(s, ba)

def turn_left_90(s: socket.socket, v):
    spin_left(s)
    time.sleep(-0.027 * v + 2.64)
    stop(s)

def turn_right_90(s: socket.socket, v):
    spin_right(s)
    time.sleep(-0.027 * v + 2.64)
    stop(s)

def forward_time(s: socket.socket, t: float):
    forward(s)
    time.sleep(t)
    stop(s)

def back_time(s: socket.socket, t: float):
    back(s)
    time.sleep(t)
    stop(s)

def turn_to_left(s: socket.socket, t: float):
    spin_left(s)
    time.sleep(t)
    stop(s)


def turn_to_right(s: socket.socket, t: float):
    spin_right(s)
    time.sleep(t)
    stop(s)

def forward_without_stop(s: socket.socket):
    forward(s)

def back_without_stop(s: socket.socket):
    back(s)

def turn_to_left_without_stop(s: socket.socket):
    spin_left(s)

def turn_to_right_without_stop(s: socket.socket):
    spin_right(s)

# скорость равна 70
def turn_left_corner(s: socket, corner):
    spin_left(s)
    time.sleep(corner * 0.73 / 90 + 0.02)
    stop(s)

# скорость = 70
def turn_right_corner(s: socket, corner):
    spin_left(s)
    time.sleep(corner * 0.73 / 90 + 0.02)
    stop(s)

# вперёд на определённую дистанцию в см
# скорость 70
def forward_dist(s: socket.socket, distance):
    k = 0.026316
    b = 0.105263
    forward(s)
    time.sleep(k * distance + b)
    stop(s)