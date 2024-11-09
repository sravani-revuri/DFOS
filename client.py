


# client.py
import socket

server_address = '127.0.0.1'#input("Enter the server IP address: ")
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
            
            elif choice =='2':
                filename=input("Enter filename to upload:")
                filepath=input("enter path of file to upload:").strip()
                client_socket.send(filename.encode())
                response = client_socket.recv(MSSGLEN).decode()
                
                if response == "filename received":
                    with open(filepath, "rb") as file:
                        while True:
                            file_data = file.read(MSSGLEN)
                            if not file_data:
                                break
                            client_socket.send(file_data)
            
                client_socket.send("EOF".encode())
                upload_response = client_socket.recv(MSSGLEN).decode()
                print(upload_response)  # Print confirmation message

            elif choice=='3':
                filename=input("Enter file name to download:")
                client_socket.send(filename.encode())
                response=client_socket.recv(MSSGLEN).decode()
               # print(response)
                if "file found" in response:
                    with open(f"download_{filename}","wb") as file:
                        while True:
                            #print("file found")
                            data=client_socket.recv(MSSGLEN)
                            print(data)
                            if data==b"EOF":
                                break
                            file.write(data)
                    print(f"File '{filename}' downloaded successfully.")
                else:
                    print("file not found on the server")


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