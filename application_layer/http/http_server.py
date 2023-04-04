from socket import *
import time

# Host and Port
HOST = '192.168.100.22'
PORT = 8000

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Configuring Socket
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(1)

    print(f'Listen to port {PORT} ...')

    while True:
        print('Waiting for client to connect...')
        
        connectionSocket, addr = serverSocket.accept()

        print(f'Client {addr[0]} connected from port {addr[1]}')

        try:
            message = connectionSocket.recv(1024).decode()
            
            filename = message.split()[1]
            print(f'Client requested the following file: {filename}')

            f = open(filename[1:], 'rb')

            outputdata = f.readlines()
            
            # Sending header
            respHeader = 'HTTP/1.1 200 OK\n\n'
            connectionSocket.send(respHeader.encode())

            # sending response
            for i, line in enumerate(outputdata, len(outputdata)):
                connectionSocket.send(line)
            
            connectionSocket.send('\r\n'.encode())

        except IOError:
            respHeader = 'HTTP/1.1 404 Not Found\n\n'
            connectionSocket.send(respHeader.encode())

            file404 = open('404_not_found.html', 'rb')
            
            respData = file404.readlines()

            for line in respData:
                connectionSocket.send(line)
            
            connectionSocket.send('\r\n'.encode())

        connectionSocket.close()

if __name__ == '__main__':
    main()