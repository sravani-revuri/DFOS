import socket
import threading
import sys
import csv

port_no=33000         #port number on server where connection occurs
MSSGLEN=1024

client_threads=[]

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
            print(f"Authenticated user {resp[0]} from {client_addr}")
        else:
            client_socket.send("AUTHENTICATION FAILED".encode())
            print(f"Failed authentication for user {resp[0]} from {client_addr}")
    finally:
        client_socket.close()

def main():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)         #setting up TCP stream
    
    #binding server to port and dynamic ip address (based on client i/p)
    server.bind(('',port_no))     
    server.listen(2)    #queue  
    print("Server started listening at {}::{}".format(*server.getsockname()))

    while True:
        client_socket,client_addr=server.accept()
        thread=threading.Thread(target=handle_client,args=(client_socket,client_addr))
        thread.start()


if __name__ == "__main__":
    main()