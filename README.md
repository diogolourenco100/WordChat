# WordChat v1.1 (Beta)

WordChat is an anonymized chat application developed for real-time communication between users. This is version 1.1 (Beta) of WordChat.

## Installation

To use WordChat, follow the steps below:

1. Make sure you have Python installed on your system. WordChat was developed in Python 3.

2. Clone or download the WordChat repository to your computer.

    ```bash
    git clone https://github.com/diogolourenco100/WordChat.git
    ```

3. Navigate to the WordChat directory.

    ```bash
    cd WordChat
    ```

4. Install the necessary dependencies.

    ```bash
    pip install -r requirements.txt
    ```

5. Run WordChat.

    ```bash
    python wordchat.py
    ```

## Usage

WordChat offers two main options: Host Server and Join a Server.

### Host Server

- Select the `Host Server` option in the menu.
- Choose a port for the server.
- Enter a username.
- Choose a color for your identification.
- Wait for other users to connect.

### Join a Server

- Select the `Join a Server` option in the menu.
- Enter the server's IP address.
- Choose the server's port.
- Enter a username.
- Choose a color for your identification.
- Connect to the server.

## Features

- Real-time communication.
- Customized user identification with colors.
- Option to clear the screen with ```/clear```.
- Option to exit the chat with ```/exit```.
- **Anti-spam feature:** Prevents users from sending empty messages.

## Notes

- WordChat is in Beta version. If you encounter any issues, please report them so we can fix them.
- Please note that WordChat is a developing application and may undergo changes.

Enjoy WordChat and have fun chatting with others in an anonymized way!

## Possible updates

- **Proxy** - The system will be anonymized by hiding users' IP addresses using Proxys.
- **Criptography** - Proxies will be encrypted to ensure maximum anonymity of users.
- **Group mode** - Multiple connections on one host.
+ **Speclist** - Normal users can use the ``/speclist`` command to see only the usernames of logged in users.
- **Admin panel** - The host can have certain functions, such as the whitelist function, where it will accept or reject a connection, ``/kick`` and ``/ban`` function on IP's of unwanted users, see all IP's connected with ``/speclist``, give ``/mute`` to some user for so many seconds, etc.
+ **Blacklist** - The user IPs banned by the host will be saved in a file on the host's machine, where if any of the IPs try to enter, they will be automatically denied by the system itself.

### Have a suggestion? Send me a message on my Discord: `GTgotinha#3137`.

---

## ⚠️ Please note that the purpose of WordChat is to be anonymous, however this function ***has not yet been assigned,*** so I ask you to be patient.
