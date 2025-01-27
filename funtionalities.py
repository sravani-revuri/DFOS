import os
import time
MSSGLEN = 1024  # Assuming MSSGLEN is defined globally for consistency

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
                client_socket.send((file_name + "\n").encode())  # Send each file name with a newline character
            client_socket.send("finished".encode())  # Send finished after listing
    except Exception as e:
        client_socket.send(f"Error accessing files: {str(e)}".encode())

def upld(username, filename, client_socket):
    user_folder = os.path.join("server_storage", username)
    if not os.path.isdir(user_folder):
        os.makedirs(user_folder)
    
    user_file = os.path.join(user_folder, filename)
    try:
        with open(user_file, "w") as file:
            while True:
                chunk = client_socket.recv(MSSGLEN).decode()
                if chunk == "EOF":
                    break
                file.write(chunk)
        client_socket.send("File uploaded successfully.".encode())
        return "success"
    except Exception as e:
        client_socket.send(f"Error during upload: {str(e)}".encode())
        os.remove(user_file)
        return 'error'
    
def upldl(username, filename, client_socket):
    user_folder = os.path.join("server_storage", username)
    if not os.path.isdir(user_folder):
        os.makedirs(user_folder)
        
    user_file = os.path.join(user_folder, filename)
    client_socket.send("filename received".encode())  # Confirmation to start receiving file data

    try:
        with open(user_file, "wb") as file:
            while True:
                chunk = client_socket.recv(MSSGLEN)
                if chunk == b"EOF":  # End of file upload
                    break
                if not chunk:  # Detect client disconnection
                    raise ConnectionError("Client disconnected unexpectedly.")
                file.write(chunk)

        client_socket.send("File uploaded successfully.".encode())
        return "success"

    except ConnectionError as e:
        print(f"ConnectionError: {e}")
        if os.path.exists(user_file):
            os.remove(user_file)  # Delete partially uploaded file
        return "error"

    except Exception as e:
        print(f"Error during file upload: {e}")
        if os.path.exists(user_file):
            os.remove(user_file)  # Delete partially uploaded file
        client_socket.send(f"Error during upload: {str(e)}".encode())
        return "error"


def dwld(username, filename, client_socket):

    user_folder = os.path.join("server_storage", username)
    
    if not os.path.isdir(user_folder):
        client_socket.send("Error: Directory does not exist.".encode())
        return "error"

    user_file = os.path.join(user_folder, filename)
    if not os.path.isfile(user_file):
        client_socket.send(f"Error: File '{filename}' does not exist.".encode())
        return "error"
    client_socket.send("fine".encode())

    try:
        with open(user_file, "rb") as file:  # Open the file in binary read mode
            while True:
                chunk = file.read(MSSGLEN)
                if not chunk:  # End of file
                    break
                client_socket.send(chunk)  # Send the current chunk
                time.sleep(0.01)
            client_socket.send(b"EOF")  # Send EOF to signal end of file transfer
        return "success"
    except Exception as e:
        client_socket.send(f"Error during download: {str(e)}".encode())
        return "error"


def delete(username, filename, client_socket):
    user_folder = os.path.join("server_storage", username)
    
    if not os.path.isdir(user_folder):
        client_socket.send("Error: User directory does not exist.".encode())
        return "error"

    user_file = os.path.join(user_folder, filename)
    if not os.path.isfile(user_file):
        client_socket.send(f"Error: File '{filename}' does not exist.".encode())
        return "error"
    
    # Send initial response before attempting deletion
    client_socket.send("File exists; preparing to delete.".encode())
    
    try:
        os.remove(user_file)
        client_socket.send("File deleted successfully.".encode())
        return "success"
    except Exception as e:
        client_socket.send(f"Error during deletion: {str(e)}".encode())
        return "error"

def preview(username, filename, client_socket):
    user_folder = os.path.join("server_storage", username)
    if not os.path.isdir(user_folder):
        os.makedirs(user_folder)

    user_file = os.path.join(user_folder, filename)

    restricted_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mp4'}

    try:
            if not os.path.isfile(user_file):
                client_socket.sendall("File not found.".encode())
            else:
                # Check file extension
                _, file_extension = os.path.splitext(filename)
                if file_extension.lower() in restricted_extensions:
                    client_socket.sendall("video or images cannot be viewed.".encode())
                else:
                    client_socket.sendall("file found".encode())
                    with open(user_file, "rb") as file:
                        preview_data = file.read(1024)  # Read the first 1024 bytes
                        client_socket.sendall(preview_data)
                    client_socket.sendall(b"EOF")
                    time.sleep(0.1)
                    client_socket.sendall("Preview complete.".encode())

    except Exception as e:
            client_socket.sendall(f"Error previewing file: {str(e)}".encode())