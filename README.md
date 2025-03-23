# Distributed File Orchestration and Synchronization  

## File Transfer Server-Client Application  

This project is a **multi-client file transfer system** implemented using **Python and TCP sockets**. It allows users to **authenticate, upload, download, preview, delete, and list files** on a remote server. The system ensures that each user can log in from only **one session at a time**.  

---

## 🚀 Features  

✅ **User Authentication**: Ensures only registered users can access the system.  

✅ **File Operations**: Supports listing, uploading, downloading, previewing, and deleting files.  

✅ **Thread-Safe Multi-Client Support**: Uses a **thread pool** to handle multiple clients efficiently.  

✅ **Chunked File Transfers**: Supports large file uploads/downloads in **chunks** to handle network constraints.  

✅ **Session Control**: Prevents **multiple logins** from the same user.  

---

## 🛠 How to Run
➤ **Start the Server** 
Open a terminal and run:

```bash
python server.py
```
The server will start listening on port 33000 for incoming connections.

➤ **Start the Client**
Open another terminal on the same machine and run:

```bash
python client.py
```
The client will prompt for a username and password to authenticate.
Once authenticated, users can choose various file operations.

To run on different machines, open client.py and uncomment line 7,
run the files with the same commands as mentioned above. Enter the server's IP address when prompted, then proceed with authentication.


