import RPi.GPIO as GPIO
import time
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
import keyboard
import socket
import threading
import pickle

motor_A1 = 24
motor_A2 = 25

motor_B1 = 20
motor_B2 = 21

GPIO.setmode(GPIO.BCM)

GPIO.setup(motor_A1, GPIO.OUT)
GPIO.setup(motor_A2, GPIO.OUT)

GPIO.setup(motor_B1, GPIO.OUT)
GPIO.setup(motor_B2, GPIO.OUT)

# pB = GPIO.PWM(motor_B1,100)
# pB.start(0)
# pB.ChangeDutyCycle(duty)


# motor_A -- LOW off, HIGH on
# GPIO.output(motor_A1,GPIO.HIGH)s
# time.sleep(1)
# GPIO.output(motor_A1,GPIO.HIGH)

# motor_B -- LOW on, HIGH off
# GPIO.output(motor_B1,GPIO.HIGH)
# time.sleep(1)
# GPIO.output(motor_B1,GPIO.HIGH)

# relay_front_left_add = 5
# relay_front_left_sub = 6
# relay_front_right_add = 26
# relay_front_right_sub = 16
# relay_back_1_add = 17
# relay_back_1_sub = 27
# relay_back_2_add = 22
# relay_back_2_sub = 23

relay_front_left_add = 5
relay_front_right_add = 6
relay_back_1_add = 26
relay_back_2_add = 16

relay_front_left_sub = 17
relay_front_right_sub = 27
relay_back_1_sub = 22
relay_back_2_sub = 23

relay_valve = [relay_front_left_add, relay_front_right_add, relay_back_1_add, relay_back_2_add,
               relay_front_left_sub, relay_front_right_sub, relay_back_1_sub, relay_back_2_sub]

relay_valve_len = len(relay_valve)

GPIO.setup(relay_front_left_add, GPIO.OUT)
GPIO.setup(relay_front_left_sub, GPIO.OUT)
GPIO.setup(relay_front_right_add, GPIO.OUT)
GPIO.setup(relay_front_right_sub, GPIO.OUT)
GPIO.setup(relay_back_1_add, GPIO.OUT)
GPIO.setup(relay_back_1_sub, GPIO.OUT)
GPIO.setup(relay_back_2_add, GPIO.OUT)
GPIO.setup(relay_back_2_sub, GPIO.OUT)

GPIO.setup(relay_valve, GPIO.OUT)
global data
global list_data
global A_duty
global B_duty

data = "None"

list_data = ["None", "None"]

A_duty = 20
B_duty = 20

pA = GPIO.PWM(motor_A1, 100)
pA.start(0)

pB = GPIO.PWM(motor_B1, 100)
pB.start(0)


# GPIO.output(relay_valve[7], False) # relay_back_2_sub
# time.sleep(3)


def back_cycle():
    GPIO.output(relay_valve[3], True)  # relay_back_2_add
    time.sleep(3)
    GPIO.output(relay_valve[3], False)  # relay_back_2_add -- stop

    GPIO.output(relay_valve[2], True)  # relay_back_1_add
    time.sleep(3)
    GPIO.output(relay_valve[2], False)  # relay_back_1_add -- stop

    GPIO.output(relay_valve[7], True)  # relay_back_2_sub
    time.sleep(5)
    GPIO.output(relay_valve[7], False)  # relay_back_2_sub -- stop

    GPIO.output(relay_valve[6], True)  # relay_back_1_sub
    time.sleep(5)
    GPIO.output(relay_valve[6], False)  # relay_back_1_sub -- stop


def front_cycle():
    GPIO.output(relay_valve[0], True)  # relay_front_left_add
    time.sleep(1)
    GPIO.output(relay_valve[0], False)  # relay_front_left_add -- stop

    GPIO.output(relay_valve[1], True)  # relay_front_right_add
    time.sleep(1)
    GPIO.output(relay_valve[1], False)  # relay_front_right_add -- stop

    GPIO.output(relay_valve[4], True)  # relay_front_left_sub
    time.sleep(1)
    GPIO.output(relay_valve[4], False)  # relay_front_left_sub -- stop

    GPIO.output(relay_valve[5], True)  # relay_front_right_sub
    time.sleep(1)
    GPIO.output(relay_valve[5], False)  # relay_front_right_sub -- stop


def front_left_cycle():
    GPIO.output(relay_valve[0], True)  # relay_front_left_add
    time.sleep(1.5)
    GPIO.output(relay_valve[0], False)  # relay_front_left_add -- stop

    GPIO.output(relay_valve[4], True)  # relay_front_left_sub
    time.sleep(1)
    GPIO.output(relay_valve[4], False)  # relay_front_left_sub -- stop


def front_right_cycle():
    GPIO.output(relay_valve[1], True)  # relay_front_right_add
    time.sleep(1.5)
    GPIO.output(relay_valve[1], False)  # relay_front_right_add -- stop

    GPIO.output(relay_valve[5], True)  # relay_front_right_sub
    time.sleep(1)
    GPIO.output(relay_valve[5], False)  # relay_front_right_sub -- stop


def go_2():
    back_cycle()
    front_cycle()


def in_motor():
    global list_data
    global data
    global A_duty

    if list_data[1] == "start":
        print("ok")
        print(A_duty)

        pA.ChangeDutyCycle(A_duty)

    elif list_data[1] == "stop":
        pA.ChangeDutyCycle(0)


def in_motor_value():
    global list_data
    global A_duty
    print("A_duty")
    print(A_duty)
    A_duty = int(list_data[1])
    pA.ChangeDutyCycle(A_duty)


def out_motor():
    global list_data
    global data
    global B_duty

    if list_data[1] == "start":
        pB.ChangeDutyCycle(B_duty)

    elif list_data[1] == "stop":
        pB.ChangeDutyCycle(0)


def out_motor_value():
    global list_data
    global B_duty
    print("B_duty")
    print(B_duty)
    B_duty = int(list_data[1])
    pB.ChangeDutyCycle(B_duty)


def A_C():
    global list_data
    global data

    if list_data[1] == "go":
        while True:
            back_cycle()
            front_left_cycle()
            front_right_cycle()

            if list_data[1] == "stop":
                break
    elif list_data[1] == "stop":
        list_data[0] = "None"
        list_data[1] = "None"


def M_C():
    global list_data
    global data

    if list_data[1] == "front":
        back_cycle()

    elif list_data[1] == "left":
        front_left_cycle()

    elif list_data[1] == "right":
        front_right_cycle()


def start_server():
    global list_data
    global data
    host = '192.168.54.155'
    port = 60013

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("client connect")

    client_socket, addr = server_socket.accept()
    print(f"{addr}connect.")

    while True:

        client_socket, addr = server_socket.accept()
        print(f"{addr}connect.")

        data = b""

        while True:
            packet = client_socket.recv(1024)
            if not packet:
                break
            data += packet
        list_data = pickle.loads(data)

        print(list_data[0])
        print(list_data[1])

        client_socket.close()
        print("close")


def tomsson_controller():
    global data
    global list_data

    while True:
        if list_data[0] == "in_motor":
            in_motor()
            list_data[0] = "None"
            list_data[1] = "None"

        if list_data[0] == "out_motor":
            out_motor()
            list_data[0] = "None"
            list_data[1] = "None"

        if list_data[0] == "in_motor_value":
            in_motor_value()
            list_data[0] = "None"
            list_data[1] = "None"

        if list_data[0] == "out_motor_value":
            out_motor_value()
            list_data[0] = "None"
            list_data[1] = "None"

        if list_data[0] == "A_C":
            A_C()
            list_data[0] = "None"
            list_data[1] = "None"

        if list_data[0] == "M_C":
            M_C()
            list_data[0] = "None"
            list_data[1] = "None"

        #        if data == "front":


#            back_cycle()
#            data = "stop"

#        if data == "left":
#            front_left_cycle()
#            data = "stop"

#        if data == "right":
#            front_right_cycle()
#            data = "stop"

#        if data == "stop":
#            GPIO.output(motor_A1,GPIO.LOW)
#            GPIO.output(motor_B1,GPIO.LOW)

t1 = threading.Thread(target=start_server)
t1.start()

t2 = threading.Thread(target=tomsson_controller)
t2.start()



