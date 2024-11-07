# client.py
import socket

server_address = input("Enter the server IP address: ")
port_no = 33000
MSSGLEN = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((server_address, port_no))
    # Authenticate
    username = input("Username: ")
    password = input("Password: ")
    client_socket.send(f"{username}:{password}".encode())
    auth_response = client_socket.recv(MSSGLEN).decode()
    print(auth_response)

    if "SUCCESSFUL" in auth_response:
        while True:
            menu = client_socket.recv(MSSGLEN).decode()
            print(menu)

            choice = input("Enter your choice: ")
            client_socket.send(choice.encode())

            if choice == '1':
                response = client_socket.recv(MSSGLEN).decode()
                if response=="finished":
                    break
                print(response)
            elif choice =='4':
                filename= input("Enter file name to delete: ")
                client_socket.send(filename.encode())
                response = client_socket.recv(MSSGLEN).decode()
                print(response)
            elif choice == '5':
                response = client_socket.recv(MSSGLEN).decode()
                print(response)
                print("Exiting.")
                break
