import argparse
import sys


###########################################################
####################### YOUR CODE #########################
###########################################################
import socket
import struct
import time

def run_server(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    while True:
        connection, address = server.accept()
        client_message = ""
        while True:
            data = connection.recv(4096)
            if not data:
                break
            message = struct.unpack(f"<{len(data)}s", data)
            client_message += message[0].decode()
        if client_message == 'close':
            break
        print(f"Received data: {client_message}")
    connection.close()
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
