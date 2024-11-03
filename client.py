import socket

def main():
    server_address = input("Enter server IP address ")  
    port_no = 33000  
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_address, port_no))
        print("Connected to server at {}:{}".format(server_address, port_no))

        username = input("Enter username: ")
        password = input("Enter password: ")

        credentials = f"{username}:{password}"
        client_socket.send(credentials.encode())
        resp = client_socket.recv(1024).decode()
        print("Server response:", resp)

    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
