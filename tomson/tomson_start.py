import socket


def start_client_send():
    host = '192.168.54.155'  # 서버의 호스트
    port = 60001  # 서버의 포트

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"{host}:{port}에 연결되었습니다.")

    message = 'go!'
    client_socket.send(message.encode())
    print(f"{host}:{port}에게 데이터를 전송하였습니다.")

    client_socket.close()
    print(f"{host}:{port}와의 연결이 종료되었습니다.")


if __name__ == "__main__":
    start_client_send()
