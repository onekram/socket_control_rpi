import socket
import time
from color import Color
from servokind import ServoKind

host = "192.168.2.99"
port = 2001

def send_command(s, command1):
    try:
        s.sendall(command1)
        print("Команда отправлена")
    except socket.error as e:
        print(f"Ошибка сокета: {e}")
        s.close()
        raise e

def create_connect():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Соединение с {host}:{port}")
        s.connect((host, port))
        print("Успех")
        time.sleep(1)
        return s
    except socket.error as e:
        print(f"Ошибка сокета, закрываем соединение: {e}")
        s.close()
        raise e

def turn_off_all(s):
    s.sendall(b'\xab\x40\x01\x00\xff')

def flash(s):
    ba = bytearray(b'\xab\x40\x02\x03\xff')
    turn_off = b'\xab\x40\x01\x00\xff'
    j = 1
    while True:
        j = (j + 1) % 8 + 1
        ba[3] = j
        for i in range(2, 10):
            ba[2] = i
            send_command(s, ba)
            time.sleep(0.3)

        j = (j + 1) % 8 + 1
        ba[3] = j
        for i in range(9, 1, -1):
            ba[2] = i
            send_command(s, ba)
            time.sleep(0.3)

    send_command(s, turn_off)


def play_color(s):
    ba = bytearray(b'\xab\x40\x0A\x03\xff')

    for i in range(10, 18):
        ba[2] = i
        ba[3] = i % 7 + 1
        s.sendall(ba)
        time.sleep(0.3)
    time.sleep(2)

def turn_off_specific(s, idx):
    ba = bytearray(b'\xab\x40\x00\x00\xff')
    ba[2] = idx + 10
    s.sendall(ba)

def snake(s):
    color1 = Color.YELLOW
    color2 = Color.RED
    for i in range(100):
        turn_off_specific(s, (i - 1) % 8)
        play_color_index(s, color1 if i % 2 else color2, i % 8)
        time.sleep(0.4)

def play_color_index(s: socket.socket, color: Color, idx: int):
    ba = bytearray(b'\xab\x40\x00\x00\xff')
    ba[2] = idx + 10
    ba[3] = color.value
    s.sendall(ba)

def turn_off_index(s: socket.socket, idx: int):
    play_color_index(s, Color.NO_COLOR, idx)

def move_servo(s: socket.socket, servo: ServoKind, angle: int):
    ba = bytearray(b'\xab\x01\x00\x00\xff')
    ba[2] = servo.value
    ba[3] = angle
    s.sendall(ba)

def hand(s: socket.socket):
    for i in range(1, 5):
        move_servo(s, ServoKind.GRAB, i * 20)
        time.sleep(2)

def start_position(s: socket.socket):
    move_servo(s, ServoKind.HAND, 87)
    move_servo(s, ServoKind.GRAB, 30)
    move_servo(s, ServoKind.SHOULDER, 180)
    move_servo(s, ServoKind.ELBOW, 100)

def trackline(s: socket.socket):
    ba = bytearray(b'\xab\x13\x02\x00\xff')
    s.sendall(ba)
    time.sleep(2)


def forward(s: socket.socket):
    ba = bytearray(b'\xab\x00\x01\x00\xff')
    s.sendall(ba)

def stop(s: socket.socket):
    ba = bytearray(b'\xab\x00\x00\x00\xff')
    s.sendall(ba)

def set_speed(s: socket.socket, value: int):
    ba1 = bytearray(b'\xab\x02\x01\x00\xff')
    ba2 = bytearray(b'\xab\x02\x02\x00\xff')

    ba1[3] = value
    ba2[3] = value
    s.sendall(ba1)
    s.sendall(ba2)

def forward_time(s: socket.socket):
    send_command(s, b'\xab\x00\x05\x04\xff')

def set_color(s: socket.socket, color: Color):
    for i in range(8):
        play_color_index(s, color, i)

def color_follow(s: socket.socket):
    send_command(s, b'\xab\x13\x09\x02\xff')

if __name__ == "__main__":
    s = create_connect()
    start_position(s)
