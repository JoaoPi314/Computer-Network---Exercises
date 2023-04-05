'''
João Pedro Melquiades Gomes
Universidade Federal de Campina Grande
-------------------------------------------------------------
Simple client in python to provide a HTTP service to a client
'''

import socket
import sys

def main():
    '''
    Main function
    '''
    # Creating a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connecting to a server
    client_socket.connect((sys.argv[1], int(sys.argv[2])))
    # Making request
    file_name = input('What file you want to request from server?')
    request = f'GET /{file_name} HTTP/1.1\r\nHost:192.168.0.4\r\n\r\n'

    client_socket.send(request.encode())

    response = client_socket.recv(1024)
    response_file = b''

    # reading data
    while not response.endswith(b'\r\n'):
        response_file += response
        response = client_socket.recv(1024)
    
    # Removing header from file
    response_file = response_file.split(b'\r\n\r\n')[1:]

    client_socket.close()

        
    # Writing file with response
    with open(f'{file_name}', 'wb') as f:
        for line in response_file:
            f.write(line)

if __name__ == '__main__':
    main()
