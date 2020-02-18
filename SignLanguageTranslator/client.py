import socket
import numpy
import time


# 서버의 주소입니다. hostname 또는 ip address를 사용할 수 있습니다.
HOST = '127.0.0.1'
# 서버에서 지정해 놓은 포트 번호입니다.
PORT = 9999


# 소켓 객체를 생성합니다.
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# 지정한 HOST와 PORT를 사용하여 서버에 접속합니다.
client_socket.connect((HOST, PORT))

while True:

        # 테스트를 위해 임의로 생성한 파일에서 데이터 읽고
        csv_data = numpy.loadtxt('test_data.txt', dtype='int')

        # 라인 수만큼 테스트 테스트
        for line in range(10):

            # 한 줄 씩 읽어서
            print(csv_data[line])

            # 전송을 위해 string으로 캐스팅 - server에서 파싱 예정
            temp_data = str(csv_data[line])

            # 메시지를 전송합니다.
            client_socket.sendall(temp_data.encode())
            time.sleep(1)  # 1초 쉬고 다음라인으로

        break

# 소켓을 닫습니다.
client_socket.close()