import threading
import socket
import pyfiglet
import platform
import time
import os
from modules.colora import green, red, black, blue, yellow, magenta, cyan, white

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

def host_ipaddress():
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)

    return host_ip

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

def server(port, username, color_func):
    HOST = host_ipaddress()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, port))
    s.listen()

    print(yellow('\nHOST:     ') + cyan(HOST) + yellow('\nPORT:     ') + cyan(str(port)) + yellow('\nUSERNAME: ') + color_func(username))
    print(yellow('\nWaiting for connection...'))
    connection, address = s.accept()

    user_connected = yellow("\n-> User ") + f"{color_func(username)}" + yellow(" connected. <-\n")
    connection.sendall(str.encode(user_connected))

    thread1 = threading.Thread(target=receiveMessage, args=[client])
    thread1 = threading.Thread(target=sendMessage, args=[client])

def client(HOST, port, username, color_func):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))

    user_connected = yellow("\n-> User ") + f"{color_func(username)}" + yellow(" connected. <-\n")
    s.sendall(str.encode(user_connected))

def receiveMessage(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg)

        except Exception:
            pass
def sendMessage(client):
    pass

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