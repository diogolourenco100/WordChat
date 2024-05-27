import os
import time
import socket
import platform
import pyfiglet
import threading
import queue
import signal
from blessed import Terminal
from modules.colora import green, red, black, blue, yellow, magenta, cyan, white

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
    print(cyan('-') * 50)
    print(cyan(banner_text))
    print(red('by Diogo S. Lourenco'))
    print(cyan('-') * 50)

def banner_welcome():
    banner_text = pyfiglet.figlet_format("WordChat", font="big")
    print(cyan('-') * 50)
    print()
    print(cyan("Welcome to"))
    print(cyan(banner_text))
    print(red('by Diogo S. Lourenco'))
    print(cyan('-') * 50)

def handle_receive(connection, recv_queue, color):
    while True:
        try:
            data = connection.recv(1024)
            if not data:
                print(red('Connection closed by the other side.'))
                break
            recv_queue.put(color(data.decode()))
        except Exception as e:
            if "10054" not in str(e) and "10053" not in str(e):
                print(f'ERROR: {e}')
            break

def handle_send(connection, username, send_queue, color):
    while True:
        message = send_queue.get()
        if message.lower() == '/clear':
            func_clear()
            print(f'\nUser {username} connected.\n')
            banner_wordchat()
        elif message.lower() == '/exit':
            print(red('\nClosing the chat...\n'))
            try:
                user = color(username)
                exit_command = red("/exit")
                connection.sendall(str.encode(white(f"\nThe user {user} used the {exit_command} command. Closing connection...\n")))
            except Exception as e:
                if "10054" not in str(e):
                    print(f'ERROR: {e}')
            finally:
                connection.close()
            break
        else:
            try:
                connection.sendall(str.encode(f'{color(username)} -> {message}'))
            except Exception as e:
                if "10054" not in str(e):
                    print(f'ERROR: {e}')
                break

def input_thread(send_queue, color_func):
    while True:
        message = input('')
        if message.strip():
            send_queue.put(message)
        else:
            print(red('Empty message cannot be sent.'))


def chat_screen(recv_queue):
    while True:
        message = recv_queue.get()
        print(message)

def server(port, username, color_func):
    HOST = '127.0.0.1'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, port))
    s.listen()

    print(yellow('\nHOST:     ') + cyan(HOST) + yellow('\nPORT:     ') + cyan(str(port)) + yellow('\nUSERNAME: ') + color_func(username))
    print(yellow('\nWaiting for connection...'))
    connection, address = s.accept()

    user_connected = yellow("\n-> User ") + f"{color_func(username)}" + yellow(" connected. <-\n")
    connection.sendall(str.encode(user_connected))

    recv_queue = queue.Queue()
    send_queue = queue.Queue()

    threading.Thread(target=handle_receive, args=(connection, recv_queue, color_func)).start()
    threading.Thread(target=handle_send, args=(connection, username, send_queue, color_func)).start()

    threading.Thread(target=chat_screen, args=(recv_queue,)).start()
    input_thread(send_queue, color_func)

def client(HOST, port, username, color_func):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))

    user_connected = yellow("\n-> User ") + f"{color_func(username)}" + yellow(" connected. <-\n")
    s.sendall(str.encode(user_connected))

    recv_queue = queue.Queue()
    send_queue = queue.Queue()

    threading.Thread(target=handle_receive, args=(s, recv_queue, color_func)).start()
    threading.Thread(target=handle_send, args=(s, username, send_queue, color_func)).start()

    threading.Thread(target=chat_screen, args=(recv_queue,)).start()
    input_thread(send_queue, color_func)

def menu_color():
    color_functions = {
        '1': green,
        '2': red,
        '3': black,
        '4': blue,
        '5': yellow,
        '6': magenta,
        '7': cyan,
        '8': white
    }

    print(f'\n[{green("1")}] - GREEN')
    print(f'[{red("2")}] - RED')
    print(f'[{black("3")}] - BLACK')
    print(f'[{blue("4")}] - BLUE')
    print(f'[{yellow("5")}] - YELLOW')
    print(f'[{magenta("6")}] - MAGENTA')
    print(f'[{cyan("7")}] - CYAN')
    print(f'[{white("8")}] - WHITE')

    color = input(yellow('\nCOLOR: '))

    if color in color_functions:
        return color_functions[color]
    else:
        print(red('Invalid option. Try again.'))
        return None

def start_server():
    try:
        port = int(input(yellow('\nPORT: ')))
        username = input(yellow('USERNAME: '))
        color_func = menu_color()
        
        if color_func is not None:
            return port, username, color_func
        else:
            return start_server()
    except ValueError:
        print(red('Invalid input! Please enter a valid integer value for the PORT.'))
        return start_server()

def start_client():
    try:
        host = input(yellow('\nHOST: '))
        port = int(input(yellow('PORT: ')))
        username = input(yellow('USERNAME: '))
        color_func = menu_color()

        if color_func is not None:
            return host, port, username, color_func
        else:
            return start_client()
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
        port, username, color_func = start_server()
        server(port, username, color_func)
    
    elif option == 2:
        host, port, username, color_func = start_client()
        client(host, port, username, color_func)

    elif option == 3:
        print(yellow('Exiting...'))
    
    else:
        print(red('Try again'))
        time.sleep(1)
        return menu()

signal.signal(signal.SIGINT, handle_exit)

if __name__ == "__main__":
    menu()
