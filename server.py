
import socket
import threading
import sys
import csv
import os
from concurrent.futures import ThreadPoolExecutor
from funtionalities import ls,delete,upld,download

port_no=33000         #port number on server where connection occurs
MSSGLEN=1024
MAX_WORKERS = 10  # Define the maximum number of threads in the pool 

# Initialize thread pool
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
client_threads=[]
client_tracker=[]

def loading_users():
    try:
         users_file = open('id_passwd.txt', 'r')
    except FileNotFoundError:
        print("Server is not able to authenticate user (filenotfound)")
        sys.exit()
    users = {}  # Create an empty dictionary to hold user-password pairs
    csv_file = csv.DictReader(users_file, delimiter=",")
    for user in csv_file:
        username = user['name']  # Get the username from the dictionary
        password = user['passwd']  # Get the password from the dictionary
        users[username] = password  # Set the username as the key and password as the value

    return users

def authenticating_user(current_users,name, password):
    if name==None or password==None:
        return False
    if name in current_users and current_users[name] == password:
        return True
    return False


def handle_client(client_socket,client_addr):
    try:
        resp=client_socket.recv(MSSGLEN).decode().strip().split(':')
        current_users=loading_users()
        if authenticating_user(current_users,resp[0],resp[1]):
            client_socket.send("SUCCESSFULL CONNECTION".encode())
            client_threads.append(threading.current_thread())
            client_tracker.append(resp[0])
            print(f"Authenticated user {resp[0]} from {client_addr}")
        else:
            client_socket.send("AUTHENTICATION FAILED".encode())
            print(f"Failed authentication for user {resp[0]} from {client_addr}")
            return
        while True:
            menu = "\nChoose an option:\n1. List files\n2. Upload file\n3. Download\n4. Delete file\n5. Quit\n"
            client_socket.send(menu.encode())

            choice = client_socket.recv(MSSGLEN).decode().strip()

            if choice == '1':
                files = ls(resp[0],client_socket)
            
            elif choice == '2':
                filename=client_socket.recv(MSSGLEN).decode().strip()
                client_socket.send("filename received".encode())
                user_folder = os.path.join("server_storage", resp[0])  # resp[0] assumed to be the username
                user_file = os.path.join(user_folder, filename)

                file_data =""
                while True:
                    chunk = client_socket.recv(MSSGLEN).decode()
                    if chunk == "EOF":
                        break  
                    file_data += chunk  

                upld(resp[0], filename, file_data)
                client_socket.send("File uploaded successfully".encode())


            elif choice=='3':
                filename=client_socket.recv(MSSGLEN).decode().strip()
                download(resp[0],filename,client_socket)

            elif choice == '4':
                filename=client_socket.recv(MSSGLEN).decode().strip()
                delete(resp[0],filename,client_socket)

            elif choice == '5':
                client_socket.send("Goodbye!".encode())
                break

            else:
                client_socket.send("Invalid option. Try again.".encode())
    finally:
        client_socket.close()

def main():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)         #setting up TCP stream
    
    #binding server to port and dynamic ip address (based on client i/p)
    server.bind(('',port_no))     
    server.listen(2)    #queue  
    print("Server started listening at {}::{}".format(*server.getsockname()))

    while True:
        client_socket, client_addr = server.accept()
        executor.submit(handle_client, client_socket, client_addr)  # Submit the handling of the client to the thread pool


if __name__ == "__main__":
    main()
