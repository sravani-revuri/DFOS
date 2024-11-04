import socket
import os  # listdir(), getcwd(), chdir(), mkdir()


def ls(username):
    user_folder = os.path.join("server_storage", username)

    if not os.path.isdir(user_folder):
        os.makedirs(user_folder)
    
    try:
        files = os.listdir(user_folder)
        return files if files else ["No files found."]
    except Exception as e:
        return [f"Error accessing files: {str(e)}"]
