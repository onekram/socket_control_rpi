import time
from socket import socket
from functions import set_speed, forward, stop


def forward_dist(s: socket, dist: int):
    forward(s)
    time.sleep(dist)
    stop(s)