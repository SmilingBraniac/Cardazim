import argparse
import sys


###########################################################
####################### YOUR CODE #########################
###########################################################
import socket
import struct
import threading
import time


def run_connection(connection : socket) -> None:
    """
    connection - a socket connected to the client
    handles a connection woth the client
    returns nothing
    """
    while True:
        client_message = ""
        while True:
            data = connection.recv(4096)  # why 4096?
            if not data:
                break
            message = struct.unpack(f"<{len(data)}s", data)
            client_message += message[0].decode()
        if client_message == "close":
            break
        if client_message:
            print(f"Recieved data: {client_message}")
    print("bye :(")
    connection.close()

def run_server(ip : str, port : int) -> None:
    """
    ip - a string of the server's ip adress
    port - an int of the server's port
    creates and handles the server
    returns nothing 
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.setsockopt(socket.SOCKET_SOL, socket.SO_REUSEADDR, 1)
    server.bind((ip, port))
    server.listen(5) # why 5?
    threads = [] #list of current threads
    user_addresses = [] # list of current user addresses
    while True:
        connection, address = server.accept()
        if address not in user_addresses:
            user_addresses.append(address)
            new_thread = threading.Thread(target=run_connection, args=(connection,))
            new_thread.start()
            threads.append(new_thread)
    server.close()


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    return parser.parse_args()


def main():
    """
    Implementation of CLI and receiving data from client.
    """
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port)
        print("Done.")
    except Exception as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

#python3 Cardazim/server.py 127.0.0.1 8000