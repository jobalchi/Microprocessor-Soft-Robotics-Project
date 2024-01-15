import sys
from tomson_controller import Ui_MainWindow  # 수정부분
import socket
# from temi_GUI_main_2 import Ui_MainWindow  # 수정부분
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import qApp
from PyQt5 import uic
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import sys


from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPalette
from PyQt5.uic import loadUi

import sys
import socket_client
import datetime
import recv_data

import threading
import pickle



QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class MainWindow:

    def __init__(self):
        super().__init__()

        self.main_win = QMainWindow()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self.main_win)

        self.ui.stackedWidget.setCurrentWidget(self.ui.start_p)

        # start_p
        self.ui.tomson_start_button.clicked.connect(self.A_or_M_choice)

        # A_or_M_p
        self.ui.set_button.clicked.connect(self.set_choice)
        self.ui.A_C_button.clicked.connect(self.A_C_choice)
        self.ui.M_C_button.clicked.connect(self.M_C_choice)

        self.ui.A_or_M_back_to_start.clicked.connect(self.back_to_start)

        # set_p
        self.ui.in_motor_start_button.clicked.connect(self.in_motor_start)
        self.ui.in_motor_stop_button.clicked.connect(self.in_motor_stop)

        self.ui.in_motor_slider.valueChanged.connect(self.in_motor_slider_value)

        self.ui.out_motor_start_button.clicked.connect(self.out_motor_start)
        self.ui.out_motor_stop_button.clicked.connect(self.out_motor_stop)

        self.ui.out_motor_slider.valueChanged.connect(self.out_motor_slider_value)

        self.ui.set_p_back_to_A_or_M.clicked.connect(self.back_to_A_or_M)

        # A_C_p
        self.ui.go_button.clicked.connect(self.A_C_go)
        self.ui.stop_button.clicked.connect(self.A_C_stop)

        self.ui.A_C_p_back_to_A_or_M.clicked.connect(self.back_to_A_or_M)

        # M_C_p
        self.ui.front_button.clicked.connect(self.M_C_front)
        self.ui.left_button.clicked.connect(self.M_C_left)
        self.ui.right_button.clicked.connect(self.M_C_right)

        self.ui.M_C_p_back_to_A_or_M.clicked.connect(self.back_to_A_or_M)

    # start_p
    def set_choice(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.set_p)

    def A_or_M_choice(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.A_or_M_p)

    # A_or_M_p
    def A_C_choice(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.A_C_p)

    def M_C_choice(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.M_C_p)

    # set_p
    def in_motor_start(self):
        print("in_motor_start")
        data = ["in_motor", "start"]
        client_send(data)
        time.sleep(0.2)

    def in_motor_stop(self):
        print("in_motor_stop")
        data = ["in_motor", "stop"]
        client_send(data)
        time.sleep(0.2)

    def in_motor_slider_value(self,in_motor_value):
        print("Slider 값 변경:", in_motor_value)
        data = ["in_motor_value", in_motor_value]
        client_send(data)
        time.sleep(0.2)

    def out_motor_start(self):
        print("out_motor_start")
        data = ["out_motor", "start"]
        client_send(data)
        time.sleep(0.2)

    def out_motor_stop(self):
        print("out_motor_stop")
        data = ["out_motor", "stop"]
        client_send(data)
        time.sleep(0.2)

    def out_motor_slider_value(self,out_motor_value):
        print("out_motor_value",out_motor_value)
        data = ["out_motor_value", out_motor_value]
        client_send(data)
        time.sleep(0.2)


    # A_C_p
    def A_C_go(self):
        print("go")
        data = ["A_C", "go"]
        client_send(data)
        time.sleep(0.2)

    def A_C_stop(self):
        print("stop")
        data = ["A_C", "stop"]
        client_send(data)
        time.sleep(0.2)

    # M_C_p
    def M_C_front(self):
        print("front")
        data = ["M_C", "front"]
        client_send(data)
        time.sleep(0.2)

    def M_C_left(self):
        print("left")
        data = ["M_C", "left"]
        client_send(data)
        time.sleep(0.2)

    def M_C_right(self):
        print("right")
        data = ["M_C", "right"]
        client_send(data)
        time.sleep(0.2)

    # back_button
    def back_to_start(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.start_p)

    def back_to_A_or_M(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.A_or_M_p)

    def show(self):
        self.main_win.show()

def client_send(set_content):
    host = '172.20.10.2'  # 서버의 호스트
    port = 60015  # 서버의 포트

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"{host}:{port}에 연결되었습니다.")

    message = pickle.dumps(set_content)
    client_socket.send(message)
    print(f"{host}:{port}에게 데이터를 전송하였습니다.")

    client_socket.close()
    print(f"{host}:{port}와의 연결이 종료되었습니다.")

app = QApplication(sys.argv)
main_win = MainWindow()
main_win.show()
# t1 = threading.Thread(target=socket_recv_data)
# t1.start()
sys.exit(app.exec_())