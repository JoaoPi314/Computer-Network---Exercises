import socket
import ssl
import os
import base64

clear = lambda: os.system('clear')



mail_server = ('smtp.gmail.com', 587)
CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
USERNAME = 'username@gmail.com'
PASSWORD = '123456'

class InvalidChoice(Exception):
    pass
class NoResponseFromServer(Exception):
    pass

def error_handler(expected_code, error_message):
    try:
        server_response = CLIENT_SOCKET.recv(1024)
        if server_response[:3] != expected_code:
            raise NoResponseFromServer
    except NoResponseFromServer:
        print(error_message)
        return False

    return True

def login():
    global USERNAME
    global PASSWORD

    USERNAME = input('Enter your email: ')
    PASSWORD = input ('Enter your password: ')


def send_mail(content):
    global CLIENT_SOCKET
    global USERNAME
    global PASSWORD

    CLIENT_SOCKET.connect(mail_server)

    # Trying to contact

    if not error_handler(b'220', 'Server not responding with 220...'):
        return
    
    print('Server is ready to interact... Please continue')

    # Making contact
    CLIENT_SOCKET.send('HELO User\r\n'.encode())

    if not error_handler(b'250', 'Server not responding with 250...'):
        return
    
    print('Server is listening to you... Next step: TLS connection')

    # Creating SSL connection
    CLIENT_SOCKET.send(('STARTTLS\r\n'.encode()))
    server_response = CLIENT_SOCKET.recv(1024)
    print(f'STARTTLS Response was: {server_response.decode()}')
    CLIENT_SOCKET = ssl.wrap_socket(CLIENT_SOCKET)

    auth_str = ("\x00"+USERNAME +"\x00"+PASSWORD).encode()
    auth_str =  base64.b64encode(auth_str)
    auth_message = "AUTH PLAIN ".encode() + auth_str + "\r\n".encode()
    CLIENT_SOCKET.send(auth_message)


    if not error_handler(b'235', 'Invalid username or password. Try to login again and check if your account allows unsafe login methods...'):
        return
    
    print('Authentication success... Telling the server that you is about to send a mail')

    mailFrom_message = f'MAIL FROM: <{USERNAME}> \r\n'
    CLIENT_SOCKET.send(mailFrom_message.encode())

    if not error_handler(b'250', 'Server not responding with 250...'):
        return
  
    recipient = input('Ok, we are almost there. Now, who will receive your mail?')

    rcptTo_message = f'RCPT TO: <{recipient}> \r\n'
    CLIENT_SOCKET.send(rcptTo_message.encode())

    if not error_handler(b'250', 'Server not responding with 250...'):
        return
    
    print('Okay, wait a little bit while I send your message... Oh, I just forgot, I need to tell the server that I will send data now')

    data_request = 'DATA \r\n'
    CLIENT_SOCKET.send(data_request.encode())

    if not error_handler(b'354', 'Server not responding with 354...'):
        return

    print('I promisse that now I will send your message. The next message will be the confirmation')

    CLIENT_SOCKET.send(content)

    final_data = '\r\n.\r\n'
    CLIENT_SOCKET.send(final_data.encode())


    if not error_handler(b'250', 'Server not responding with 250...'):
        return

    print('Now let me say Bye to the server. We need to be polite after all')

    CLIENT_SOCKET.send('QUIT \r\n'.encode())
    
    if not error_handler(b'221', 'Server not responding with 221...'):
        return
    
    CLIENT_SOCKET.close()


def menu_loop():
    while True:
        clear()
        print('''
        *****************************************
        WELCOME TO THE PMAIL - POOR MAIL
        
        Choose an option:

        1. Login/ Change user 
        2. Send mail
        3. Quit
        
        *****************************************
        ''')

        try:
            choice = input('Choose an option: ' )
            if choice not in ['1', '2', '3']:
                raise InvalidChoice
        
        except InvalidChoice:
            print('Choose a valid option...')
            continue

        match(choice):
            case '1':
                login()
            case '2':
                try:
                    file_name = input('Enter file with the text to be sent: ')
                    with open(file_name, 'rb') as f:
                        send_mail(f.read())
                except IOError:
                    print('File doesn\'t exist')
                    continue
            case '3':
                break
        input('Type anything to continue...')


def main():
    menu_loop()


if __name__ == '__main__':
    main()