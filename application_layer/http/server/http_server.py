'''
João Pedro Melquiades Gomes
Universidade Federal de Campina Grande
-------------------------------------------------------------
Simple server in python to provide a HTTP service to a client
'''
import socket

# Host and Port
HOST = '192.168.0.4'
PORT = 8000

def main():
    '''
    Main function
    '''
    # Creating a TCP connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configuring Socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f'Listen to port {PORT} ...')

    while True:
        print('Waiting for client to connect...')
        connection_socket, addr = server_socket.accept()

        print(f'Client {addr[0]} connected from port {addr[1]}')

        try:
            message = connection_socket.recv(1024).decode()
            filename = message.split()[1]
            print(f'Client requested the following file: {filename}')

            f = open(filename[1:], 'rb')

            resp_data = f.readlines()
            # Sending header
            resp_header = 'HTTP/1.1 200 OK\n\n'
            connection_socket.send(resp_header.encode())

            # sending response
            for line in resp_data:
                connection_socket.send(line)
            connection_socket.send('\r\n'.encode())

        except IOError:
            resp_header = 'HTTP/1.1 404 Not Found\n\n'
            connection_socket.send(resp_header.encode())

            file404 = open('404_not_found.html', 'rb')
            resp_data = file404.readlines()

            for line in resp_data:
                connection_socket.send(line)
            connection_socket.send('\r\n'.encode())

        connection_socket.close()

if __name__ == '__main__':
    main()
