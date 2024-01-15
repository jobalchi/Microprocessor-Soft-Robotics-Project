import socket


def start_server():
    host = '192.168.54.155'  # 서버를 시작할 호스트
    port = 60000  # 서버를 시작할 포트

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"서버가 {host}:{port}에서 시작되었습니다.")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"{addr}에서 연결이 수립되었습니다.")

        data = client_socket.recv(1024)
        print(f"받은 데이터: {data.decode()}")

        client_socket.send(data)
        print(f"{addr}에게 데이터를 전송하였습니다.")

        client_socket.close()
        print(f"{addr}와의 연결이 종료되었습니다.")


if __name__ == "__main__":
    start_server()
