import socket
import os  # listdir(), getcwd(), chdir(), mkdir()

def ls(username, client_socket):
    user_folder = os.path.join("server_storage", username)

    if not os.path.isdir(user_folder):
        os.makedirs(user_folder)

    try:
        files = os.listdir(user_folder)
        if not files:
            client_socket.send("No files found.".encode())
        else:
            for file_name in files:
                client_socket.send((file_name).encode())
    except Exception as e:
        client_socket.send(f"Error accessing files: {str(e)}".encode())

def delete(username,filename,client_socket):
    user_folder=os.path.join("server_storage",username)
    if not os.path.isdir(user_folder):
        os.makedirs(user_folder)
    user_file=os.path.join(user_folder,filename)
    try:
        if not os.path.isfile(user_file):
            client_socket.send(f"File with name {filename} does not exist on server".encode())
        else:
            os.remove(user_file)
            client_socket.send(f"successfully deleted file {filename} on server check using list file command".encode())
    except Exception as e:
        client_socket.send(f"Error accessing files: {str(e)}".encode())

