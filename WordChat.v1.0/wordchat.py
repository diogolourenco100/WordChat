import os
import time
import socket
import platform
import pyfiglet
import threading
import queue
import signal
from blessed import Terminal
from modules.colora import green, cyan, red, yellow

term = Terminal()

def func_clear():
    os_name = platform.system()
    try:
        if os_name == "Windows":
            os.system('cls')
        else:
            os.system('clear')
    except Exception as e:
        pass
        try:
            if os_name == "Windows":
                os.system('clear')
            else:
                os.system('cls')
        except Exception as e:
            print(f'ERROR: {e}')

def banner_wordchat():
    banner_text = pyfiglet.figlet_format("WordChat", font="big")
    print(cyan('-')*50)
    print(cyan(banner_text))
    print(red('by Diogo S. Lourenco'))
    print(cyan('-')*50)

def banner_welcome():
    banner_text = pyfiglet.figlet_format("WordChat", font="big")
    print(cyan('-')*50)
    print()
    print(cyan("Welcome to"))
    print(cyan(banner_text))
    print(red('by Diogo S. Lourenco'))
    print(cyan('-')*50)

def handle_receive(connection, recv_queue):
    while True:
        try:
            data = connection.recv(1024)
            if not data:
                print(red('Connection closed by the other side.'))
                break
            recv_queue.put(yellow(data.decode()))
        except Exception as e:
            print(f'ERROR: {e}')
            break

def handle_send(connection, username, send_queue):
    while True:
        message = send_queue.get()
        if message.lower() == '/clear':
            func_clear()
            banner_wordchat()
        elif message.lower() == '/exit':
            print(red('Closing the chat...'))
            connection.close()
            break
        else:
            connection.sendall(str.encode(f'{username}: {message}'))

def input_thread(send_queue):
    while True:
        message = input(cyan('& '))
        send_queue.put(message)

def chat_screen(recv_queue):
    while True:
        message = recv_queue.get()
        print(message)

def server(port, username):
    HOST = '127.0.0.1'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, port))
    s.listen()

    print(yellow('\nHOST:     ') + cyan(HOST) + yellow('\nPORT:     ') + cyan(str(port)) + yellow('\nUSERNAME: ') + green(username))
    print(yellow('\nWaiting connection...'))
    connection, address = s.accept()

    user_connected = f'\nUser {username} connected.\n'
    connection.sendall(str.encode(user_connected))

    recv_queue = queue.Queue()
    send_queue = queue.Queue()

    threading.Thread(target=handle_receive, args=(connection, recv_queue)).start()
    threading.Thread(target=handle_send, args=(connection, username, send_queue)).start()

    threading.Thread(target=chat_screen, args=(recv_queue,)).start()
    input_thread(send_queue)

def client(HOST, PORT, username):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    user_connected = f'\nUser {username} connected.\n'
    s.sendall(str.encode(user_connected))

    recv_queue = queue.Queue()
    send_queue = queue.Queue()

    threading.Thread(target=handle_receive, args=(s, recv_queue)).start()
    threading.Thread(target=handle_send, args=(s, username, send_queue)).start()

    threading.Thread(target=chat_screen, args=(recv_queue,)).start()
    input_thread(send_queue)

def start_server():
    try:
        port = int(input(yellow('\nPORT: ')))
        username = input(yellow('USERNAME: '))
        return port, username
    except ValueError:
        print(red('Invalid input! Please enter a valid integer value for the PORT.'))
        return start_server()

def start_client():
    try:
        host = input(yellow('\nHOST: '))
        port = int(input(yellow('PORT: ')))
        username = input(yellow('USERNAME: '))
        return host, port, username
    except ValueError:
        print(red('Invalid input! Please enter a valid integer value for the PORT.'))
        return start_client()

def handle_exit(signal, frame):
    print(red('\nInterrupt received, closing connection...'))
    os._exit(0)

def menu():
    func_clear()
    banner_welcome()
    print(green('\n[1]') + yellow(' - Host server\n') + green('[2]') + yellow(' - Join a server\n') + green('[') + red('3') + green(']') + yellow(' - Exit\n'))

    option = int(input('$ '))

    if option == 1:
        port, username = start_server()
        server(port, username)
    
    elif option == 2:
        host, port, username = start_client()
        client(host, port, username)

    elif option == 3:
        print(yellow('Exiting...'))
    
    else:
        print(red('Try again'))
        time.sleep(1)
        return menu()

signal.signal(signal.SIGINT, handle_exit)
menu()
