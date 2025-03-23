# Distributed File Orchestration and Synchronization  

## File Transfer Server-Client Application  

This project is a **multi-client file transfer system** implemented using **Python and TCP sockets**. It allows users to **authenticate, upload, download, preview, delete, and list files** on a remote server. The system ensures that each user can log in from only **one session at a time**.  

---

## 🚀 Features  

1) **User Authentication**: Ensures only registered users can access the system.  

2) **File Operations**: Supports listing, uploading, downloading, previewing, and deleting files.  

3) **Thread-Safe Multi-Client Support**: Uses a **thread pool** to handle multiple clients efficiently.  

4) **Chunked File Transfers**: Supports large file uploads/downloads in **chunks** to handle network constraints.  

5) **Session Control**: Prevents **multiple logins** from the same user.  

---

## 🛠 How to Run  

### 1️⃣ Start the Server  

Open a terminal and run:  

```bash
python server.py
```
The server will start listening on **port 33000** for incoming connections.  

### 2️⃣ Start the Client  

On a client machine, open a terminal and run:  

```bash
python client.py
```

To run the server on another system , un-comment  line no 7 from client.py
#server_address = input("enter ip address of serv ")
and input the ip address of server system
