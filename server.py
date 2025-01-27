import socket
import threading
import sys
import csv
from concurrent.futures import ThreadPoolExecutor
from funtionalities import ls, upld, upldl, dwld, delete, preview

port_no = 33000  # Port number on server where connection occurs
MSSGLEN = 1024
MAX_WORKERS = 1  # Define the maximum number of threads in the pool

# Initialize thread pool
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
client_threads = []
client_tracker = set()
tracker_lock = threading.Lock()  # Lock for accessing client_tracker


def loading_users():
    try:
        users_file = open('id_passwd.txt', 'r')
    except FileNotFoundError:
        print("Server is not able to authenticate user (file not found)")
        sys.exit()
    users = {}  # Create an empty dictionary to hold user-password pairs
    csv_file = csv.DictReader(users_file, delimiter=",")
    for user in csv_file:
        username = user['name']  # Get the username from the dictionary
        password = user['passwd']  # Get the password from the dictionary
        users[username] = password  # Set the username as the key and password as the value

    return users


def authenticating_user(current_users, name, password):
    if name is None or password is None:
        return False
    if name in current_users and current_users[name] == password:
        return True
    return False


def handle_client(client_socket, client_addr):
    global client_tracker

    username = None  # Track the username of the connected client
    try:
        resp = client_socket.recv(MSSGLEN).decode().strip().split(':')
        current_users = loading_users()
        username = resp[0]

        with tracker_lock:
            if username in client_tracker:
                client_socket.send("User already logged in. Multiple sessions not allowed.".encode())
                print(f"Rejected login for {resp} from {client_addr} - already logged in.")
                return

        if authenticating_user(current_users, username, resp[1]):
            client_socket.send("SUCCESSFUL CONNECTION".encode())

            with tracker_lock:
                client_tracker.add(username)
            client_threads.append(threading.current_thread())
            print(f"Authenticated user {username} from {client_addr}")
        else:
            client_socket.send("AUTHENTICATION FAILED".encode())
            print(f"Failed authentication for user {username} from {client_addr}")
            return

        while True:
            menu = "\nChoose an option:\n1. List files\n2. Upload text file\n3. Large file upload\n4. Download File\n5. Preview File\n6. Delete File\n7.Quit"
            client_socket.send(menu.encode())

            choice = client_socket.recv(MSSGLEN).decode().strip()

            if choice == '1':
                ls(username, client_socket)

            elif choice == '2':
                filename = client_socket.recv(MSSGLEN).decode().strip()
                client_socket.send("filename received".encode())
                # Send confirmation to upload text in chunks
                upload_result = upld(username, filename, client_socket)
                if upload_result == "error":
                    continue

            elif choice == '3':
                filename = client_socket.recv(MSSGLEN).decode().strip()
                upload_result = upldl(username, filename, client_socket)
                if upload_result == "error":
                    continue  # Skip back

            elif choice == '4':
                filename = client_socket.recv(MSSGLEN).decode().strip()
                download_result = dwld(username, filename, client_socket)
                if download_result == "error":
                    continue

            elif choice == '5':  # Preview option
                filename = client_socket.recv(MSSGLEN).decode().strip()
                preview(username, filename, client_socket)
                continue

            elif choice == '6':  # Delete file
                filename = client_socket.recv(MSSGLEN).decode().strip()
                del_result = delete(username, filename, client_socket)
                if del_result == "error":
                    continue

            elif choice == '7':
                client_socket.send("Goodbye!".encode())
                break

            else:
                client_socket.send("Invalid option. Try again.".encode())
    except Exception as e:
        print(f"Error with client {client_addr}: {e}")
    finally:
        if username:
            with tracker_lock:
                client_tracker.discard(username)  # Remove the user safely
            print(f"User {username} disconnected.")
        client_socket.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Setting up TCP stream

    # Binding server to port and dynamic IP address (based on client input)
    server.bind(('', port_no))
    server.listen(2)  # Queue
    print("Server started listening at {}::{}".format(*server.getsockname()))

    while True:
        client_socket, client_addr = server.accept()
        executor.submit(handle_client, client_socket, client_addr)  # Submit the handling of the client to the thread pool


if __name__ == "__main__":
    main()
