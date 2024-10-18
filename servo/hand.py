import socket
import time

from servokind import ServoKind
from servo.servo_movement import move_servo

def start_position(s: socket.socket):
    move_servo(s, ServoKind.HAND, 10)
    move_servo(s, ServoKind.GRAB, 70)
    move_servo(s, ServoKind.SHOULDER, 170)
    move_servo(s, ServoKind.ELBOW, 170)

def prepare(s: socket.socket): # приготовится к захвату
    move_servo(s, ServoKind.GRAB, 20)
    time.sleep(0.3)
    move_servo(s, ServoKind.HAND, 95)
    move_servo(s, ServoKind.SHOULDER, 80)
    move_servo(s, ServoKind.ELBOW, 170)

def catch(s: socket.socket):
    move_servo(s, ServoKind.GRAB, 70)
    time.sleep(0.3)
    move_servo(s, ServoKind.HAND, 95)
    move_servo(s, ServoKind.SHOULDER, 80)
    move_servo(s, ServoKind.ELBOW, 180)

def hold(s: socket.socket): # захватить и поднять
    move_servo(s, ServoKind.GRAB, 70)
    time.sleep(0.3)
    move_servo(s, ServoKind.SHOULDER, 170)
    move_servo(s, ServoKind.ELBOW, 125)
    time.sleep(0.3)
    move_servo(s, ServoKind.HAND, 10)


def put_down(s: socket.socket): # отпустить объект
    move_servo(s, ServoKind.HAND, 95)
    time.sleep(0.5)
    move_servo(s, ServoKind.GRAB, 20)
    move_servo(s, ServoKind.SHOULDER, 175)
    move_servo(s, ServoKind.ELBOW, 115)

def fall(s: socket.socket):
    #move_servo(s, ServoKind.GRAB, 20)
    #move_servo(s, ServoKind.HAND, 95)
    move_servo(s, ServoKind.SHOULDER, 80)
    move_servo(s, ServoKind.ELBOW, 170)



def catch_ball(s: socket.socket):
    move_servo(s, ServoKind.GRAB, 70)
    time.sleep(0.3)
    move_servo(s, ServoKind.HAND, 95)
    move_servo(s, ServoKind.SHOULDER, 80)
    move_servo(s, ServoKind.ELBOW, 180)

def start_position_before_follow_ball(s: socket.socket):
    move_servo(s, ServoKind.HAND, 10)
    move_servo(s, ServoKind.GRAB, 70)
    move_servo(s, ServoKind.SHOULDER, 170)
    move_servo(s, ServoKind.ELBOW, 120)