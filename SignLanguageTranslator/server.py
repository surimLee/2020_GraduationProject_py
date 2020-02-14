from socket import *
import socket
import os  # 환경변수나 디렉터리, 파일등의 OS 자원을 제어하기 위함
import time

# 데이터 파일 저장경로
src = "./temp"

# 접속할 서버 주소입니다. 테스트를 위해 루프백(loopback) 인터페이스 주소 즉 localhost를 사용합니다.
HOST = '127.0.0.1'

# 클라이언트 접속을 대기하는 포트 번호입니다.
PORT = 9999


def filename():
    dte = time.localtime()
    year = dte.tm_year
    mon = dte.tm_mon
    day = dte.tm_mday
    hour = dte.tm_hour
    minn = dte.tm_min
    sec = dte.tm_sec
    dataName = src + str(day) + '_' + str(hour) + '_' + str(minn) + '_' + str(sec)
    return dataName


# 소켓 객체를 생성합니다.
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 포트 사용중이라 연결할 수 없다는
# WinError 10048 에러 해결를 위해 필요합니다.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind 함수는 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용됩니다.
# HOST는 hostname, ip address, 빈 문자열 ""이 될 수 있습니다.
# 빈 문자열이면 모든 네트워크 인터페이스로부터의 접속을 허용합니다.
# PORT는 1-65535 사이의 숫자를 사용할 수 있습니다.
# server_socket.bind((HOST, PORT))
server_socket.bind(("", PORT))

# 서버가 하나의 클라이언트의 접속을 허용하도록 합니다.
server_socket.listen(1)

file_receive_cnt = 0
print ("TCPServer Waiting for client...")

# accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓을 리턴합니다.
client_socket, address = server_socket.accept()

# 연결 요청 성공. 접속한 클라이언트의 주소입니다.
print("I got a connection from ", address)

data = None

# 무한루프를 돌면서 데이터 수신
while True:

    # 클라이언트가 보낸 메시지를 수신하기 위해 대기합니다.
    data = client_socket.recv(1024)

    # 빈 문자열을 수신하면 루프를 중지합니다.
    if not data:
        break


    # 수신받은 문자열을 출력합니다.
    print('Received from', address, data.decode())

    # 받은 문자열을 다시 클라이언트로 전송해줍니다.(에코)
    client_socket.sendall(data)


# 소켓을 닫습니다.
client_socket.close()
server_socket.close()
