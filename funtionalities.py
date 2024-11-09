import socket,time
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

<<<<<<< Updated upstream
=======
def upld(username,filename,data):
    user_folder=os.path.join("server_storage",username)
    if not os.path.isdir(user_folder):
        os.makedirs(user_folder)
    user_file=os.path.join(user_folder,filename)
    if os.path.exists(user_file):
        return False  # Indicate the file exists
   
    with open(user_file, "w") as file:
        file.write(data)
        return True
    
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
def download(username,filename,client_socket):
    # set  the path to the users folder
   # print("seaarch")
    user_folder=os.path.join("server_storage",username)
    #print(user_folder)
    #check the users directory exists
    if not os.path.isdir(user_folder):
        os.makedirs(user_folder)

   
    user_file=os.path.join(user_folder,filename)

    try:
        #check if the file is there?
        if not os.path.isfile(user_file):
            client_socket.send("file not exist")
        else:
            client_socket.send("file found".encode())

            #open the file in reading mode

            with open(user_file,"rb") as file:
                while chunk:=file.read(1024):
                    print(chunk)
                    client_socket.send(chunk)
                    time.sleep(0.1)
            client_socket.send(b"EOF")
           

    except Exception as e:
<<<<<<< Updated upstream
        client_socket.send(f"Erro during file download :{str(e)}".encode)
=======
        client_socket.send(f"Erro during file download :{str(e)}".encode)
>>>>>>> Stashed changes
