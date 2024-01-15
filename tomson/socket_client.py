
import csv
import socket

import recv_data


class socket_client:
    # 서버 IP와 포트번호 설정
    HOST = '172.20.10.2'
    PORT = 60015

    # 소켓 생성 및 서버에 연결
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # 데이터 전송
    def socket_send(set_content_encode):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((socket_client.HOST, socket_client.PORT))
        client_socket.send(set_content_encode)

        client_socket.close()


    # 데이터 수신
    def socket_recv():
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((socket_client.HOST, socket_client.PORT))
        recv_data.recv_data_config = client_socket.recv(1024).decode()

        # 소켓 연결 종료
        client_socket.close()