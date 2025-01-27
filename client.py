import socket
import os
import time  # For adding delay if needed
import sys

server_address = '127.0.0.1'  # Server IP
#server_address = input("enter ip address of serv ")
port_no = 33000
MSSGLEN = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_address, port_no))
        
        # Authentication
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
                    if response == "finished":
                        break
                    print(response)

                elif choice == '2':  # Upload text file in chunks
                    filename = input("Enter filename to upload: ")
                    filepath = input("Enter path of text file to upload: ").strip()

                    if not os.path.isfile(filepath):
                        print(f"Error: File '{filepath}' does not exist.")
                        sys.exit("Terminating program due to missing file.")

                    try:
                        client_socket.send(filename.encode())  # Send filename to server
                        response = client_socket.recv(MSSGLEN).decode()
                        if response == "filename received":
                            with open(filepath, "r") as file:
                                while True:
                                    file_data = file.read(MSSGLEN)
                                    if not file_data:
                                        break
                                    client_socket.send(file_data.encode())
                                    time.sleep(0.01)  # Small delay
                            client_socket.send("EOF".encode())
                            upload_response = client_socket.recv(MSSGLEN).decode()      
                            print(upload_response)
                    except Exception as e:
                        print(f"Error while uploading text file: {e}")
                        sys.exit("Terminating program due to upload error.")

                elif choice == '3':  # Large file (binary) upload
                    filename = input("Enter filename to upload: ")
                    filepath = input("Enter path of file to upload: ").strip()

                    if not os.path.isfile(filepath):
                        print(f"Error: File '{filepath}' does not exist.")
                        sys.exit("Terminating program due to missing file.")

                    try:
                        client_socket.send(filename.encode())  # Send filename to server
                        response = client_socket.recv(MSSGLEN).decode()
                        if response == "filename received":
                            with open(filepath, "rb") as file:
                                while True:
                                    file_data = file.read(MSSGLEN)
                                    if not file_data:
                                        break
                                    client_socket.send(file_data)
                                    time.sleep(0.01)  # Small delay
                            client_socket.send(b"EOF")
                            upload_response = client_socket.recv(MSSGLEN).decode()
                            print(upload_response)
                    except Exception as e:
                        print(f"Error while uploading binary file: {e}")
                        sys.exit("Terminating program due to upload error.")
                
                
                elif choice == '4':  # Download file
                    filename = input("Enter filename to download: ")
                    client_socket.send(filename.encode())  # Send filename request to server
                    resp = client_socket.recv(MSSGLEN).decode()
    
                    if resp == "fine":
        # Specify the local path where the file will be saved
                        local_path = os.path.join("client_storage", username)
                        local_path = os.path.join(local_path, filename)

        # Ensure the directory exists
                        os.makedirs(os.path.dirname(local_path), exist_ok=True)

                        try:
                            with open(local_path, "wb") as file:  # Open file in binary write mode
                                while True:
                                    chunk = client_socket.recv(MSSGLEN) 
                                    if chunk == b"EOF":  # End of file transfer
                                        print("Download completed.")
                                        break
                                    file.write(chunk)  # Write the received chunk to the file
                                print(f"File '{filename}' downloaded successfully and saved at {local_path}.")
        
                        except KeyboardInterrupt:
                            print("\nDownload interrupted by user (Ctrl+C). Deleting incomplete file.")
            # Close and delete the partially downloaded file
                            if not file.closed:
                                file.close()
                            if os.path.exists(local_path):
                                os.remove(local_path)
                                break

                        except Exception as e:
                            print(f"Error during file download: {e}")
            # Close and delete the partially downloaded file
                            if not file.closed:
                                file.close()
                            if os.path.exists(local_path):
                                os.remove(local_path)
                                break
                    else:
                        print(resp)

                
                elif choice == '5':  # Preview file
                    filename = input("Enter file name to preview: ")
                    client_socket.sendall(filename.encode())

                # Receive initial response (whether file was found or not)
                    response = client_socket.recv(MSSGLEN).decode()
                    print(response)

                    if "cannot be viewed" in response or "File not found" in response:
                    # Display restriction message and return to menu without further steps
                        continue

                    if "file found" in response:
                        preview_data = b""

                    # Receive preview data
                        while True:
                            chunk = client_socket.recv(MSSGLEN)
                            if chunk == b"EOF":
                                break
                            preview_data += chunk

                        print("Preview of the file content (up to 1024 bytes):")
                        if(filename[-4:]==".txt"):
                            print(preview_data.decode(errors="ignore"))  # Display preview content
                        else:
                            print(preview_data.hex())
                    
                    # Confirm preview is complete
                        final_message = client_socket.recv(MSSGLEN).decode()
                        print(final_message)
                        time.sleep(0.01)

                elif choice == '6':
                    filename = input("Enter filename to delete: ")
                    client_socket.send(filename.encode())  # Send filename request to server
                    resp =client_socket.recv(MSSGLEN).decode()
                    if resp== "fine":
                        print(f"file '{filename}' will be deleted")
                        resp =client_socket.recv(MSSGLEN).decode()
                        print(resp)
                        time.sleep(0.01)
                    else:
                        print(resp)
                        time.sleep(0.01)

                elif choice == '7':  # Quit
                    response = client_socket.recv(MSSGLEN).decode()
                    print(response)
                    break

                else:
                    response = client_socket.recv(MSSGLEN).decode()
                    print(response)
        else:
            print(auth_response)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nClient interrupted (Ctrl+C). Closing connection and exiting.")
    finally:
        print("Client socket closed. Goodbye!")

    
